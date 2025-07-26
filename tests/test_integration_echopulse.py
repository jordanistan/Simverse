import pytest
from fastapi.testclient import TestClient
import sys
import os

# Add project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from echopulse import app

client = TestClient(app)

def test_websocket_connection():
    """Tests that a client can connect to the WebSocket and receive a message."""
    with client.websocket_connect("/ws") as websocket:
        data = websocket.receive_json()
        assert data["type"] == "full_update"
        assert "payload" in data
        assert "active_agents" in data["payload"]
        assert "memory_garden" in data["payload"]
