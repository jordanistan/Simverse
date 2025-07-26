import docker

# --- Docker Client Initialization ---
try:
    client = docker.from_env()
except docker.errors.DockerException:
    print("\n--- Docker is not running or accessible. ---")
    print("Please start Docker and restart the application.")
    client = None

def get_all_containers():
    """Fetches a list of all containers from the Docker daemon."""
    if not client:
        return []
    try:
        return client.containers.list(all=True)
    except docker.errors.APIError as e:
        print(f"Error fetching containers: {e}")
        return []

def get_container_stats(container_id):
    """Fetches real-time stats for a specific container."""
    if not client:
        return None
    try:
        container = client.containers.get(container_id)
        stats = container.stats(stream=False) # Get a single snapshot of stats
        return stats
    except (docker.errors.NotFound, docker.errors.APIError) as e:
        print(f"Error fetching stats for container {container_id}: {e}")
        return None

def control_container(container_id, action):
    """Performs an action (start, stop, restart) on a container."""
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