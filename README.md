# 🏙️ EchoSimWorld

Welcome to EchoSimWorld — a living simulation where Docker containers are transformed into sentient agents ("Echoes") and visualized in a real-time, interactive environment.

---

## ✨ Features

- **Real-time Visualization**: Built with Streamlit, EchoSimWorld provides a dynamic view of all your Docker agents.
- **Full Agent Lifecycle**: Create new Echoes from any Docker image and interact with them to view their status and control them (start/stop/restart).
- **FastAPI WebSocket Backend**: A high-performance Python backend manages Docker interactions and streams data to the frontend in real-time.
- **Containerized**: The entire application is containerized with Docker for easy setup and consistent performance.
- **Remote Monitoring**: Configure EchoSimWorld to monitor a remote Docker host, perfect for managing homelabs or servers.

---

## 🚀 Getting Started

The entire application is designed to run within a single Docker container. Ensure you have Docker installed.

1.  **Clone the repository.**

2.  **Build the Docker image:**
    From the root of the project directory, run:
    ```bash
    docker build -t echosimworld:latest .
    ```

3.  **Run the application (Local Monitoring):**
    This command runs EchoSimWorld and connects it to your local Docker daemon by mounting the Docker socket.
    ```bash
    docker run -d -p 8501:8501 -p 8502:8502 -v /var/run/docker.sock:/var/run/docker.sock --name echosim echosimworld:latest
    ```

4.  **Open Your Browser:**
    Navigate to [http://localhost:8501](http://localhost:8501) to view and interact with the simulation.

---

## 🌐 Monitoring a Remote Host

To configure EchoSimWorld to monitor a remote Docker instance (like a homelab server), set the `DOCKER_HOST_URL` environment variable when running the container.

```bash
# Replace YOUR_REMOTE_HOST_IP with the IP address of your server
docker run -d -p 8501:8501 -p 8502:8502 \
  -e DOCKER_HOST_URL="tcp://YOUR_REMOTE_HOST_IP:2375" \
  --name echosim echosimworld:latest
```

This assumes the remote Docker daemon is configured to listen on TCP port 2375. Once running, you can access the UI from any machine on your network by navigating to `http://<machine_ip_running_container>:8501`.

---

## 🛠️ Tech Stack

-   **Frontend**: Streamlit
-   **Backend**: Python, FastAPI, Uvicorn, Docker SDK for Python
-   **Database**: SQLite for agent persistence
-   **Containerization**: Docker

---

## 🗃️ Project Structure

```text
.
├── .venv/                # Python virtual environment
├── .gitignore
├── Dockerfile            # Defines the application container
├── README.md             # You are here
├── requirements.txt      # Python dependencies
├── start.sh              # Startup script for backend and frontend
├── ui.py                 # Streamlit frontend application
├── echopulse.py          # FastAPI WebSocket backend
├── sim_engine.py         # Core simulation engine
├── docker_bridge.py      # Docker SDK interface
└── db.py                 # SQLite database management
```

---

## ⚖️ License

MIT © 2025 Jordan Robison
