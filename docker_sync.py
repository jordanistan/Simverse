import docker_bridge
import db
import zones

def determine_mood(status):
    """Determines an Echo's mood based on its container status."""
    if status in ['running', 'up']:
        return 'serene' # Calmly operating
    elif status == 'restarting':
        return 'agitated' # In a state of flux
    elif status in ['paused']:
        return 'asleep' # In stasis
    elif status in ['exited', 'dead', 'stopped']:
        return 'silent' # No longer active
    elif status in ['created']:
        return 'dreaming' # Waiting to be born
    else:
        return 'inscrutable' # An unknown state

def sync_agents_with_docker():
    """Syncs the agent database with the current state of Docker containers."""
    print("Starting Docker sync...")
    containers = docker_bridge.get_all_containers()
    db_agents = db.get_all_agents(active_only=True)

    container_ids = {c.id for c in containers}
    # db_agents is a list of dicts, so we iterate directly
    db_agent_ids = {a['id'] for a in db_agents}

    # Add or update agents for all existing containers
    for container in containers:
        agent_data = {
            'id': container.id,
            'name': container.name,
            'status': container.status,
        }
        agent_data['mood'] = determine_mood(agent_data['status'])
        agent_data['zone'] = zones.assign_zone(agent_data['status'])
        db.add_or_update_agent(agent_data)

    # Deactivate agents for containers that no longer exist
    stale_agent_ids = db_agent_ids - container_ids
    for agent_id in stale_agent_ids:
        db.deactivate_agent(agent_id)
        print(f"Deactivated stale agent: {agent_id}")

    print("Docker sync finished.")

if __name__ == '__main__':
    # Initialize the database in case it hasn't been
    db.init_db()
    # Run the sync process
    sync_agents_with_docker()