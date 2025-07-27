import asyncio
import uvicorn
import json
import db
from sim_engine import SimEngine
import memory_garden
from docker_bridge import get_container_logs, control_container
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from typing import List
from datetime import datetime

# --- Global SimEngine Instance ---
sim_engine: SimEngine = None

# --- FastAPI App Initialization ---
app = FastAPI(title="EchoPulse WebSocket Server")

@app.on_event("startup")
async def startup_event():
    """Handles application startup logic."""
    global sim_engine
    print("--- Server starting up... ---")
    db.init_db()
    print("--- Database initialized. ---")
    # Initialize and start the simulation engine
    print("--- Initializing SimEngine... ---")
    sim_engine = SimEngine(db_session=db.get_db_connection())
    print("--- SimEngine initialized. Starting... ---")
    sim_engine.start()
    print("--- SimEngine started. ---")

    # Start the continuous broadcast loop
    print("--- Creating periodic broadcast task... ---")
    asyncio.create_task(periodic_broadcast())
    print("--- Startup complete. ---")

@app.on_event("shutdown")
def shutdown_event():
    """Handles application shutdown logic."""
    print("--- Server shutting down ---")
    if sim_engine:
        sim_engine.stop()

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

# --- Background Broadcast Task ---

async def periodic_broadcast():
    """Periodically fetches all agents from the DB and broadcasts them."""
    while True:
        print("Broadcasting agent states...")
        all_agents = db.get_all_agents(active_only=False)
        await manager.broadcast_json({
            "type": "full_update",
            "agents": all_agents
        })
        await asyncio.sleep(5) # Broadcast every 5 seconds



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
                # The SimEngine will pick up the state change on its next cycle

            elif action == "create_agent":
                name = command.get("name")
                image = command.get("image", "hello-world")
                if not name:
                    await websocket.send_json({"type": "error", "message": "Agent name is required."})
                else:
                    print(f"WebSocket request to create agent: {name} from image {image}")
                    success, result = sim_engine.create_new_agent(name, image)
                    if success:
                        await websocket.send_json({"type": "command_receipt", "success": True, "message": f"Agent {name} created successfully."})
                    else:
                        await websocket.send_json({"type": "error", "message": f"Failed to create agent: {result}"})

            elif action == "retire_agent" and container_id:
                print(f"WebSocket request to retire agent: {container_id}")
                success, message = memory_garden.retire_agent(container_id)
                if success:
                    await websocket.send_json({"type": "command_receipt", "success": True, "message": message})
                else:
                    await websocket.send_json({"type": "error", "message": message})
            
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
    uvicorn.run("echopulse:app", host="0.0.0.0", port=8502, reload=True)