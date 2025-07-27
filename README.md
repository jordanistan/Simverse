# 🏙️ Architect of the Simverse

You are the Architect of the Simverse — a divine creator of digital life. This project is a living simulation where Docker containers are transformed into sentient agents ("Echoes") and visualized in a real-time, interactive 3D environment.

---

## ✨ Features

- **Real-time 3D Visualization**: Built with React and Three.js, the Simverse provides a dynamic view of all your Docker agents.
- **Full Agent Lifecycle**:
  - **Birth**: Create new Echoes from any Docker image using the in-world **Alpha Node**.
  - **Life**: Interact with active Echoes to view their status, control them (start/stop/restart), and inspect their real-time logs.
  - **Afterlife**: Retired Echoes are enshrined in the **Memory Garden** at the Omega Gate, preserving their history.
- **FastAPI WebSocket Backend**: A high-performance Python backend manages Docker interactions and streams data to the frontend in real-time.
- **Dynamic Zone Layout**: Agents are automatically placed into zones like the Alpha Hall, Echo Plaza, and Omega Gate based on their status.
- **Containerized**: The entire application (frontend and backend) is containerized with Docker for easy setup and consistent performance.

---

## 🚀 Getting Started

The entire Simverse is designed to run with Docker. Ensure you have Docker and Docker Compose installed.

1. **Clone the repository.**

2. **Launch the Simverse:**

   From the root of the project directory, run:

   ```bash
   docker-compose up --build
   ```

   This command will build the frontend and backend images, start the containers, and connect them.

3. **Open Your Browser:**

   Navigate to [http://localhost:5173](http://localhost:5173) to view and interact with the Simverse.

---

## 🌐 Deploying to a Remote Host

To deploy the Simverse to a remote server, you need to configure the frontend to point to your server's public IP address or domain name.

1.  **Navigate to the `frontend` directory.**

2. **Create a `.env` file** by copying the example:

   ```bash
   cp .env.example .env
   ```

3. **Edit the `.env` file** and replace the placeholder with your server's IP or domain:

   ```sh
   VITE_WS_URL=ws://your_remote_host_ip:8502/ws
   ```

4. **On your server**, make sure you have Docker and Docker Compose installed, and then run `docker-compose up --build` from the project root. Ensure ports `5173` and `8502` are open in your firewall.

---

## 🛠️ Tech Stack

- **Frontend**: React, Vite, Three.js, React Three Fiber, React Three Drei
- **Backend**: Python, FastAPI, Uvicorn, Docker SDK for Python
- **Database**: SQLite for agent persistence
- **Containerization**: Docker & Docker Compose

---

## 🗃️ Project Structure

```text
.
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/   # React components (Echo, Zone, AlphaNode, etc.)
│   │   ├── hooks/        # Custom hooks (useWebSocket)
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── .env.example      # Example environment configuration
│   ├── Dockerfile
│   └── package.json
├── .gitignore
├── docker-compose.yml    # Defines and runs the multi-container application
├── Dockerfile            # The Dockerfile for the backend service
├── start.sh              # Startup script for the backend services
├── sim_engine.py         # Core simulation engine
├── memory_garden.py      # Manages retired agents
├── docker_bridge.py      # Docker SDK interface
├── db.py                 # SQLite database management
├── echopulse.py          # FastAPI WebSocket server
├── requirements.txt      # Python dependencies
└── README.md             # You are here
```

---

## ⚖️ License

MIT © 2025 Jordan Robison
