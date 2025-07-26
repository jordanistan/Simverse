import pytest
import sys
import os

# Add project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from zones import assign_zone, ZONES

@pytest.mark.parametrize("status, expected_zone_key", [
    ("created", "ALPHA_HALL"),
    ("running", "ECHO_PLAZA"),
    ("up", "ECHO_PLAZA"),
    ("restarting", "DOCKER_CORE"),
    ("paused", "DOCKER_CORE"),
    ("exited", "OMEGA_GATE"),
    ("dead", "OMEGA_GATE"),
    ("stopped", "OMEGA_GATE"),
])
def test_assign_zone_known_statuses(status, expected_zone_key):
    """Test that known container statuses are assigned to the correct zones."""
    expected_zone = ZONES[expected_zone_key]
    result = assign_zone(status)
    assert result == expected_zone, f"Status '{status}' should be in '{expected_zone['name']}'"

def test_assign_zone_unknown_status():
    """Test that an unknown container status is assigned to 'The Void'."""
    unknown_status = "some_weird_state"
    result = assign_zone(unknown_status)
    assert result['name'] == "The Void", "Unknown status should be assigned to 'The Void'"
    assert result['emoji'] == "🌌", "The emoji for 'The Void' should be correct"
