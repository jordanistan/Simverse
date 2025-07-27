import docker
import os

# --- Docker Client Initialization ---
_client = None

def get_docker_client():
    """Initializes and returns a Docker client, reusing if already created."""
    global _client
    if _client is not None:
        return _client

    # Check for a remote Docker host URL from environment variables
    remote_host_url = os.environ.get('DOCKER_HOST_URL')
    if remote_host_url:
        try:
            print(f"\n--- Attempting to connect to remote Docker host: {remote_host_url} ---")
            _client = docker.DockerClient(base_url=remote_host_url)
            _client.ping()
            print(f"\n--- Docker client initialized successfully for remote host: {remote_host_url}. ---")
            return _client
        except docker.errors.DockerException as e:
            print(f"\n--- Failed to connect to remote Docker host: {remote_host_url} ---")
            print(f"Error details: {e}")
            # Fall through to try local connection methods

    # If remote fails or is not set, try standard local methods
    try:
        # First, try the standard method, which respects DOCKER_HOST etc.
        _client = docker.from_env()
        _client.ping()
        print("\n--- Docker client initialized successfully from environment. ---")
        return _client
    except docker.errors.DockerException as e:
        print("\n--- Could not connect to Docker from environment. Trying default socket... ---")
        print(f"Initial error: {e}")

    # If from_env fails, try connecting to the default Unix socket directly
    try:
        _client = docker.DockerClient(base_url='unix://var/run/docker.sock')
        _client.ping()
        print("\n--- Docker client initialized successfully via default socket. ---")
    except docker.errors.DockerException as e:
        print("\n--- Docker is not running or accessible. ---")
        print("Could not connect to Docker. Please ensure Docker Desktop is running.")
        print(f"Error details: {e}")
        print("If Docker is running, your environment may not be configured correctly.")
        _client = None

    return _client

def get_all_containers():
    """Fetches a list of all containers from the Docker daemon."""
    client = get_docker_client()
    if not client:
        return []
    try:
        return client.containers.list(all=True)
    except docker.errors.APIError as e:
        print(f"Error fetching containers: {e}")
        return []

def get_container_stats(container_id):
    """Fetches real-time stats for a specific container."""
    client = get_docker_client()
    if not client:
        return None
    try:
        container = client.containers.get(container_id)
        stats = container.stats(stream=False) # Get a single snapshot of stats
        return stats
    except (docker.errors.NotFound, docker.errors.APIError) as e:
        print(f"Error fetching stats for container {container_id}: {e}")
        return None

def get_container_logs(container_id, tail=100):
    """Fetches logs for a specific container."""
    client = get_docker_client()
    if not client:
        return False, "Docker client not available"
    try:
        container = client.containers.get(container_id)
        logs = container.logs(tail=tail).decode('utf-8')
        return True, logs
    except docker.errors.NotFound:
        return False, f"Container {container_id} not found"
    except Exception as e:
        return False, f"Error fetching logs: {e}"

def control_container(container_id, action):
    """Performs an action (start, stop, restart) on a container."""
    client = get_docker_client()
    if not client:
        return False, "Docker client not available"
    try:
        container = client.containers.get(container_id)
        if action == "start":
            container.start()
            return True, f"Container {container_id} started."
        elif action == "stop":
            container.stop()
            return True, f"Container {container_id} stopped."
        elif action == "restart":
            container.restart()
            return True, f"Container {container_id} restarted."
        else:
            return False, f"Unknown action: {action}"
    except (docker.errors.NotFound, docker.errors.APIError) as e:
        return False, f"Error performing '{action}' on container {container_id}: {e}"

def create_agent(name, image="hello-world"):
    """Creates and starts a new Docker container (agent)."""
    client = get_docker_client()
    if not client:
        return False, "Docker client not available"
    try:
        print(f"Attempting to create agent '{name}' from image '{image}'...")
        # Ensure the image is available locally
        try:
            client.images.get(image)
            print(f"Image '{image}' found locally.")
        except docker.errors.ImageNotFound:
            print(f"Image '{image}' not found locally. Pulling from Docker Hub...")
            client.images.pull(image)
            print(f"Successfully pulled image '{image}'.")

        container = client.containers.run(
            image,
            detach=True,
            name=name,
            labels={"source": "echosim"}
        )
        print(f"Successfully created and started container {container.id} ({name})")
        return True, container.id
    except docker.errors.APIError as e:
        print(f"Error creating container: {e}")
        return False, str(e)
    except Exception as e:
        print(f"An unexpected error occurred during agent creation: {e}")
        return False, str(e)