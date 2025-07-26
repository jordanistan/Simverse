# --- Zone Definitions ---
ZONES = {
    "ALPHA_HALL": {
        "name": "Alpha Hall",
        "description": "The birthplace of new Echoes, where potential takes form.",
        "emoji": "✨"
    },
    "ECHO_PLAZA": {
        "name": "Echo Plaza",
        "description": "The bustling hub where active Echoes live and interact.",
        "emoji": "🏙️"
    },
    "DOCKER_CORE": {
        "name": "Docker Core",
        "description": "The inner sanctum where the fundamental forces of the Simverse are at work.",
        "emoji": "⚙️"
    },
    "OMEGA_GATE": {
        "name": "Omega Gate",
        "description": "The final gateway, where Echoes prepare to fade into memory.",
        "emoji": "🚪"
    },
    "THE_VOID": {
        "name": "The Void",
        "description": "An uncharted space between defined zones.",
        "emoji": "🌌"
    }
}

def assign_zone(agent_status):
    """Assigns an Echo to a zone based on its container status."""
    if agent_status in ['created']:
        return "ALPHA_HALL"
    elif agent_status in ['running', 'up']:
        return "ECHO_PLAZA"
    elif agent_status in ['restarting', 'paused']:
        return "DOCKER_CORE"
    elif agent_status in ['exited', 'dead', 'stopped']:
        return "OMEGA_GATE"
    else:
        # Default case for any unknown statuses
        return "THE_VOID"