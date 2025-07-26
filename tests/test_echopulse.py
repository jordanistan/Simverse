import pytest
import asyncio
from unittest.mock import patch, MagicMock, AsyncMock
import sys
import os

# Add project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import echopulse

@pytest.mark.asyncio
@patch('asyncio.sleep', new_callable=AsyncMock)
@patch('echopulse.manager.broadcast_json', new_callable=AsyncMock)
@patch('echopulse.db')
@patch('echopulse.docker_sync')
async def test_sync_and_broadcast(mock_docker_sync, mock_db, mock_broadcast, mock_sleep):
    """Test that the sync_and_broadcast function calls its dependencies and broadcasts the correct data."""
    # 1. Setup Mocks
    mock_active_agents = {'agent1': {'id': 'agent1', 'status': 'running'}}
    mock_inactive_agents = [{'id': 'agent2', 'status': 'exited'}]

    mock_db.get_all_agents.return_value = mock_active_agents
    mock_db.get_memory_garden_agents.return_value = mock_inactive_agents

    # Make sleep raise an exception to break the while loop after one iteration
    mock_sleep.side_effect = asyncio.CancelledError

    # 2. Run the async function and catch the exception to exit the loop
    with pytest.raises(asyncio.CancelledError):
        await echopulse.sync_and_broadcast()

    # 3. Assertions
    mock_docker_sync.sync_agents_with_docker.assert_called_once()
    mock_db.get_all_agents.assert_called_once_with(active_only=True)
    mock_db.get_memory_garden_agents.assert_called_once()

    # Assert that the broadcast function was called with the correct payload
    expected_payload = {
        "type": "full_update",
        "payload": {
            "active_agents": mock_active_agents,
            "memory_garden": mock_inactive_agents
        }
    }
    mock_broadcast.assert_called_once_with(expected_payload)
