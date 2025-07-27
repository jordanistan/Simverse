# EchoSimWorld

**EchoSimWorld** is a simulation environment for managing autonomous agents, called "Echoes," which are represented as Docker containers. The platform provides a real-time 3D visualization for observing and interacting with these agents.

## Architecture

The application is containerized into a single Docker image using a multi-stage build. This single container serves both:

- **FastAPI Backend:** A WebSocket server (`echopulse.py`) that manages the simulation, communicates with the Docker daemon, and streams updates to the frontend.
- **React Frontend:** A 3D user interface built with React and Three.js for visualizing the simulation.

This unified architecture simplifies deployment and management.

## Getting Started

### Prerequisites

- Docker Engine

### Build and Run

1. **Build the Docker Image:**

    The project uses a multi-stage `Dockerfile` that first builds the React frontend and then copies the static assets into the final Python image. To build the image, run the following command from the project root:

    ```bash
    docker build -t echosimworld:latest .
    ```

2. **Run the Docker Container:**

    The application can connect to either a local or a remote Docker daemon.

    - **To connect to a local Docker daemon:**

        ```bash
        docker run -d -p 8502:8502 --name echosim -v /var/run/docker.sock:/var/run/docker.sock echosimworld:latest
        ```

    - **To connect to a remote Docker daemon:**

        You must expose your remote Docker daemon on a TCP port (e.g., 2375) and set the `DOCKER_HOST_URL` environment variable when running the container:

        ```bash
        docker run -d -p 8502:8502 --name echosim -e DOCKER_HOST_URL="tcp://<your-remote-docker-ip>:2375" echosimworld:latest
        ```

3. **Access the Application:**

    Once the container is running, open your browser and navigate to:

    [http://localhost:8502](http://localhost:8502)

---

## 🛠️ Tech Stack

- **Frontend**: React, Three.js, Vite
- **Backend**: Python, FastAPI, Uvicorn, Docker SDK
- **Database**: SQLite
- **Containerization**: Docker (Multi-stage build)

---

## 🗃️ Project Structure

```text
.
├── frontend/             # React frontend source code
├── .gitignore
├── Dockerfile            # Multi-stage Dockerfile
├── README.md             # You are here
├── requirements.txt      # Python dependencies
├── start.sh              # Container startup script
├── echopulse.py          # FastAPI WebSocket backend
├── sim_engine.py         # Core simulation engine
├── docker_bridge.py      # Docker SDK interface
└── db.py                 # SQLite database management
```

---

## ⚖️ License

MIT © 2025 Jordan Robison
