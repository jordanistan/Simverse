import pytest
import sqlite3
import sys
import os
import json
from datetime import datetime

# Add project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import db

def test_init_db(db_connection):
    """Test that the database table is created correctly."""
    cursor = db_connection.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='agents';")
    assert cursor.fetchone() is not None, "'agents' table should exist after init_db"

def test_add_or_update_agent(db_connection):
    """Test adding a new agent and updating an existing one."""
    # Add a new agent
    agent_data = {
        'id': 'test_agent_1',
        'name': 'Test Agent',
        'status': 'running',
        'mood': 'serene',
        'zone': json.dumps({'name': 'ECHO_PLAZA'})
    }
    db.add_or_update_agent(agent_data)

    # Verify the agent was added
    retrieved = db.get_all_agents()[0]
    assert retrieved['id'] == 'test_agent_1'
    assert retrieved['name'] == 'Test Agent'
    assert retrieved['is_active'] == True

    # Update the agent
    updated_agent_data = {
        'id': 'test_agent_1',
        'name': 'Test Agent Updated',
        'status': 'exited',
        'mood': 'silent',
        'zone': json.dumps({'name': 'OMEGA_GATE'})
    }
    db.add_or_update_agent(updated_agent_data)

    # Verify the agent was updated
    retrieved_updated = db.get_all_agents()[0]
    assert retrieved_updated['name'] == 'Test Agent Updated'
    assert retrieved_updated['status'] == 'exited'

def test_deactivate_agent(db_connection):
    """Test that an agent can be marked as inactive."""
    agent_data = {'id': 'test_agent_2', 'name': 'To Be Deactivated'}
    db.add_or_update_agent(agent_data)

    # Deactivate the agent
    db.deactivate_agent('test_agent_2')

    # Verify it's no longer in the active list
    active_agents = db.get_all_agents(active_only=True)
    assert len(active_agents) == 0

    # Verify it's in the memory garden
    inactive_agents = db.get_memory_garden_agents()
    assert len(inactive_agents) == 1
    assert inactive_agents[0]['id'] == 'test_agent_2'
