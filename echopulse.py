import asyncio
import uvicorn
import json
import db
import docker_sync
from docker_bridge import control_container
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

            if action and container_id:
                print(f"Received command: {action} on {container_id[:12]}")
                success, message = control_container(container_id, action)
                print(message)
                # Immediately send a command confirmation back to the specific client
                await websocket.send_json({"type": "command_receipt", "success": success, "message": message})
                # Trigger an immediate sync and broadcast to all clients
                asyncio.create_task(sync_and_broadcast(once=True))

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