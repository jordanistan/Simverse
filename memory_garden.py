# memory_garden.py

import db
import docker_bridge as docker


def retire_agent(agent_id):
    """Retires an agent, stopping its container and marking it as inactive.

    This function moves an Echo to the Memory Garden.

    Args:
        agent_id (str): The ID of the agent to retire.

    Returns:
        A tuple (success, message).
    """
    print(f"MemoryGarden: Retiring agent {agent_id}...")

    # 1. Stop the container
    success, message = docker.control_container(agent_id, 'stop')
    if not success:
        # If stopping fails, we might still want to mark it as inactive
        print(f"Warning: Could not stop container {agent_id}: {message}")
        # We'll proceed to deactivate it in the DB anyway

    # 2. Mark as inactive in the database
    try:
        db.deactivate_agent(agent_id)
        print(f"MemoryGarden: Agent {agent_id} has been enshrined in the Memory Garden.")
        return True, f"Agent {agent_id} retired successfully."
    except Exception as e:
        error_message = f"MemoryGarden: Error deactivating agent {agent_id} in DB: {e}"
        print(error_message)
        return False, error_message


def get_retired_agents():
    """Fetches all retired agents from the Memory Garden.

    Returns:
        A list of agent data dictionaries.
    """
    try:
        return db.get_memory_garden_agents()
    except Exception as e:
        print(f"MemoryGarden: Error fetching retired agents: {e}")
        return []