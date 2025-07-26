import pytest
from unittest.mock import patch, MagicMock, call
import sys
import os

# Add project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import docker_sync

@patch('docker_sync.db')
@patch('docker_sync.docker_bridge')
def test_sync_agents_with_docker(mock_docker_bridge, mock_db):
    """Test the core logic of synchronizing Docker containers with the agent database."""
    # 1. Setup Mocks

    # Mock containers from Docker
    mock_container_new = MagicMock()
    mock_container_new.id = 'new_container_id'
    mock_container_new.name = 'new_agent'
    mock_container_new.status = 'running'

    mock_container_updated = MagicMock()
    mock_container_updated.id = 'existing_agent_id'
    mock_container_updated.name = 'existing_agent'
    mock_container_updated.status = 'exited' # Status has changed

    mock_docker_bridge.get_all_containers.return_value = [mock_container_new, mock_container_updated]

    # Mock agents from DB
    mock_db.get_all_agents.return_value = {
        'existing_agent_id': {'id': 'existing_agent_id', 'name': 'existing_agent', 'status': 'running'},
        'stale_agent_id': {'id': 'stale_agent_id', 'name': 'stale_agent', 'status': 'running'}
    }

    # 2. Run the function to be tested
    docker_sync.sync_agents_with_docker()

    # 3. Assertions

    # Verify that get_all_containers and get_all_agents were called
    mock_docker_bridge.get_all_containers.assert_called_once()
    mock_db.get_all_agents.assert_called_once()

    # Verify calls to add_or_update_agent
    # It should be called for the new container and the updated container
    assert mock_db.add_or_update_agent.call_count == 2

    # Check the call for the new agent
    call_new_agent = call({
        'id': 'new_container_id',
        'name': 'new_agent',
        'status': 'running',
        'mood': 'serene',
        'zone': {'name': 'Echo Plaza', 'description': 'The bustling hub where active Echoes live and interact.', 'emoji': '🏙️'}
    })

    # Check the call for the updated agent
    call_updated_agent = call({
        'id': 'existing_agent_id',
        'name': 'existing_agent',
        'status': 'exited',
        'mood': 'silent',
        'zone': {'name': 'Omega Gate', 'description': 'The final gateway, where Echoes prepare to fade into memory.', 'emoji': '🚪'}
    })

    mock_db.add_or_update_agent.assert_has_calls([call_new_agent, call_updated_agent], any_order=True)

    # Verify that the stale agent was deactivated
    mock_db.deactivate_agent.assert_called_once_with('stale_agent_id')
