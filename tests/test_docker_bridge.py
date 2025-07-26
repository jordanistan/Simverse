import pytest
from unittest.mock import MagicMock, patch
import sys
import os

# Add project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import docker_bridge
import docker



@patch('docker_bridge.client')
def test_get_all_containers_success(mock_client):
    """Test successful retrieval of a list of containers."""
    # Create mock container objects
    mock_container_1 = MagicMock()
    mock_container_1.id = 'container_1_id'
    mock_container_1.name = 'container_one'
    mock_container_1.status = 'running'

    mock_container_2 = MagicMock()
    mock_container_2.id = 'container_2_id'
    mock_container_2.name = 'container_two'
    mock_container_2.status = 'exited'

    mock_client.containers.list.return_value = [mock_container_1, mock_container_2]

    containers = docker_bridge.get_all_containers()

    assert len(containers) == 2
    assert containers[0].name == 'container_one'
    mock_client.containers.list.assert_called_once_with(all=True)

@patch('docker_bridge.client', None)
def test_get_all_containers_docker_error():
    """Test that an empty list is returned when the Docker client is not available."""
    containers = docker_bridge.get_all_containers()
    assert containers == []
