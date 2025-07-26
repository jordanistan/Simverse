import asyncio
import uvicorn
import json
import db
import docker_sync
from docker_bridge import get_docker_client, get_all_containers, get_container_stats, control_container, get_container_logs, create_agent
from contextlib import asynccontextmanager
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from typing import List
from datetime import datetime


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manages the application's lifespan events for startup and shutdown."""
    print("--- Server starting up ---")
    db.init_db()
    # Start the continuous sync loop
    asyncio.create_task(sync_and_broadcast())
    yield
    print("--- Server shutting down ---")

# --- FastAPI App Initialization ---
app = FastAPI(title="EchoPulse WebSocket Server", lifespan=lifespan)

# --- Connection Manager ---

class ConnectionManager:
    """Manages active WebSocket connections."""
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        print(f"New connection: {websocket.client}. Total connections: {len(self.active_connections)}")

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
        print(f"Connection closed: {websocket.client}. Total connections: {len(self.active_connections)}")

    async def broadcast_json(self, data: dict):
        """Broadcasts JSON data to all connected clients."""
        # Custom JSON encoder to handle datetime objects
        def json_encoder(obj):
            if isinstance(obj, datetime):
                return obj.isoformat()
            raise TypeError(f"Object of type {type(obj)} is not JSON serializable")
        
        message = json.dumps(data, default=json_encoder)
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

# --- Background Sync Task ---

async def sync_and_broadcast(once=False):
    """Syncs with Docker and broadcasts the agent list, either once or in a loop."""
    print("Running sync and broadcast...")
    docker_sync.sync_agents_with_docker()
    active_agents = db.get_all_agents(active_only=True)
    inactive_agents = db.get_memory_garden_agents()
    await manager.broadcast_json({
        "type": "full_update",
        "agents": active_agents + inactive_agents # Send a single list for easier frontend processing
    })
    print("Broadcast complete.")

    if not once:
        await asyncio.sleep(5)
        asyncio.create_task(sync_and_broadcast()) # Schedule the next run



# --- WebSocket Endpoint ---

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            # This loop is now primarily for receiving commands.
            # Broadcasting is handled by the global sync_and_broadcast task.
            data = await websocket.receive_text()
            command = json.loads(data)
            
            action = command.get("action")
            container_id = command.get("container_id")

            if action == 'get_logs' and container_id:
                print(f"Fetching logs for {container_id[:12]}...")
                success, logs = get_container_logs(container_id)
                log_data = {
                    "type": "logs",
                    "container_id": container_id,
                    "success": success,
                    "logs": logs
                }
                await websocket.send_text(json.dumps(log_data))
                print(f"Sent logs for {container_id[:12]} to client.")

            elif action in ['start', 'stop', 'restart'] and container_id:
                print(f"Received command: {action} on {container_id[:12]}")
                success, message = control_container(container_id, action)
                print(message)
                # Immediately send a command confirmation back to the specific client
                await websocket.send_json({"type": "command_receipt", "success": success, "message": message})
                # Trigger an immediate sync and broadcast to all clients
                asyncio.create_task(sync_and_broadcast(once=True))

            elif action == "create_agent":
                name = command.get("name")
                image = command.get("image", "hello-world") # Default to hello-world if not provided
                if not name:
                    await websocket.send_json({"type": "error", "message": "Agent name is required."})
                else:
                    print(f"WebSocket request to create agent: {name} from image {image}")
                    success, result = create_agent(name, image)
                    if success:
                        print("Agent creation successful, running sync and broadcasting...")
                        await websocket.send_json({"type": "command_receipt", "success": True, "message": f"Agent {name} created successfully."})
                        # Trigger an immediate sync and broadcast to all clients
                        asyncio.create_task(sync_and_broadcast(once=True))
                    else:
                        await websocket.send_json({"type": "error", "message": f"Failed to create agent: {result}"})
            
            else:
                print(f"Received unknown command or missing data: {command}")

    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except json.JSONDecodeError:
        print("Received non-JSON message, ignoring.")
    except Exception as e:
        print(f"An error occurred in websocket_endpoint: {e}")
        manager.disconnect(websocket)

# --- Main Entry Point ---

if __name__ == "__main__":
    print("Starting EchoPulse server on ws://localhost:8502/ws")
    uvicorn.run(app, host="0.0.0.0", port=8502)