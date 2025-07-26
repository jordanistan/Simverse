import sqlite3
import json
from datetime import datetime

DATABASE_FILE = "simverse.db"

def get_db_connection():
    """Establishes a connection to the SQLite database."""
    conn = sqlite3.connect(DATABASE_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initializes the database and creates the agents table if it doesn't exist."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS agents (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                status TEXT,
                mood TEXT,
                zone TEXT,
                created_at TIMESTAMP,
                updated_at TIMESTAMP,
                is_active BOOLEAN DEFAULT TRUE,
                thought_log TEXT
            )
        """)
        conn.commit()
    print("Database initialized.")

def add_or_update_agent(agent_data):
    """Adds a new agent or updates an existing one (UPSERT)."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        now = datetime.utcnow()
        thought_log = json.dumps(agent_data.get("thought_log", []))
        zone = agent_data.get("zone", "THE_VOID") # Zone is a simple string

        cursor.execute("""
            INSERT INTO agents (id, name, status, mood, zone, created_at, updated_at, is_active, thought_log)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET
                name = excluded.name,
                status = excluded.status,
                mood = excluded.mood,
                zone = excluded.zone,
                updated_at = excluded.updated_at
        """, (
            agent_data['id'],
            agent_data['name'],
            agent_data.get('status', 'unknown'),
            agent_data.get('mood', 'neutral'),
            zone,
            now,
            now,
            True,
            thought_log
        ))
        conn.commit()

def get_memory_garden_agents():
    """Fetches all inactive agents (Echoes in the Memory Garden)."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM agents WHERE is_active = FALSE ORDER BY updated_at DESC")
        return [dict(row) for row in cursor.fetchall()]

def get_all_agents(active_only=True):
    """Fetches all agents from the database."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        query = "SELECT * FROM agents"
        if active_only:
            query += " WHERE is_active = TRUE"
        cursor.execute(query)
        return [dict(row) for row in cursor.fetchall()]

def deactivate_agent(agent_id):
    """Marks an agent as inactive (moves to Memory Garden)."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE agents
            SET is_active = FALSE, updated_at = ?
            WHERE id = ?
        """, (datetime.utcnow(), agent_id))
        conn.commit()

# Initialize the database when the module is loaded
if __name__ == '__main__':
    init_db()