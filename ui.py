import streamlit as st
import asyncio
import websockets
from collections import defaultdict
import json

# --- Page Configuration ---
st.set_page_config(
    page_title="Architect of the Simverse",
    page_icon="🏙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- WebSocket Connection ---
ECHOPULSE_URI = "ws://localhost:8502/ws"

st.title("🏙️ Architect of the Simverse")
st.caption("The divine control panel for your digital ecosystem.")

# --- UI Components & State ---
status_placeholder = st.empty()
agent_display_placeholder = st.empty()
memory_garden_placeholder = st.empty()

if 'zones_data' not in st.session_state:
    st.session_state.zones_data = {}
if 'memory_garden' not in st.session_state:
    st.session_state.memory_garden = []

def get_mood_emoji(mood):
    """Returns an emoji based on the agent's mood."""
    mood_map = {
        'serene': '😌',
        'agitated': '😬',
        'asleep': '😴',
        'silent': '⚪',
        'dreaming': '✨',
        'inscrutable': '🤔'
    }
    return mood_map.get(mood, '❔')

def get_status_emoji(status):
    """Returns an emoji based on the container status."""
    if 'running' in status or 'up' in status:
        return "🟢"
    elif 'exited' in status or 'stopped' in status:
        return "🔴"
    else:
        return "🟡"

async def listen_to_echopulse():
    """Connects to the WebSocket and updates the UI with agent data."""
    status_placeholder.info("Connecting to the Simverse...", icon="📡")
    while True:
        try:
            async with websockets.connect(ECHOPULSE_URI) as websocket:
                status_placeholder.success("Connected to the Simverse! Awaiting Echoes...", icon="✅")
                while True:
                    message = await websocket.recv()
                    data = json.loads(message)
                    if data.get("type") == "full_update":
                        payload = data.get("payload", {})
                        st.session_state.active_agents = {a['id']: a for a in payload.get('active_agents', [])}
                        st.session_state.memory_garden = payload.get('memory_garden', [])

                        # --- Process and Group Agents by Zone ---
                        zones_data = defaultdict(lambda: {'details': {}, 'agents': []})
                        active_agents = payload.get('active_agents', [])
                        for agent in active_agents:
                            try:
                                zone_info = json.loads(agent.get('zone', '{}'))
                                zone_name = zone_info.get('name', 'The Void')
                            except (json.JSONDecodeError, AttributeError):
                                zone_info = {'name': 'The Void', 'description': 'An uncharted space.', 'emoji': '🌌'}
                                zone_name = 'The Void'

                            zones_data[zone_name]['details'] = zone_info
                            zones_data[zone_name]['agents'].append(agent)
                        
                        st.session_state.zones_data = zones_data

                        # --- Render Zones and their Echoes ---
                        with agent_display_placeholder.container():
                            if not st.session_state.zones_data:
                                st.subheader("Active Echoes")
                                st.write("No Echoes detected. Are your containers running?")
                            else:
                                for zone_name, data in sorted(st.session_state.zones_data.items()):
                                    details = data['details']
                                    agents_in_zone = data['agents']
                                    st.subheader(f"{details.get('emoji', '')} {zone_name}")
                                    st.caption(details.get('description', ''))
                                    
                                    if not agents_in_zone:
                                        st.write("This zone is quiet.")
                                    else:
                                        for agent in agents_in_zone:
                                            status_emoji = get_status_emoji(agent['status'])
                                            mood_emoji = get_mood_emoji(agent.get('mood', 'inscrutable'))
                                            st.markdown(f"- {status_emoji} **{agent['name']}** — Mood: {mood_emoji} *{agent.get('mood', 'inscrutable')}* (`{agent['status']}`)")
                                    st.divider()
                        
                        # --- Render Memory Garden ---
                        with memory_garden_placeholder.container():
                            st.subheader("🪦 The Memory Garden")
                            if not st.session_state.memory_garden:
                                st.write("The garden is quiet. All Echoes are currently active.")
                            else:
                                for agent in st.session_state.memory_garden:
                                    st.markdown(f"- ⚪ **{agent['name']}** (Faded on {agent['updated_at']})")

        except (websockets.exceptions.ConnectionClosed, ConnectionRefusedError):
            status_placeholder.error("Connection lost. Is the EchoPulse server running? Retrying...", icon="❌")
            await asyncio.sleep(5)
        except Exception as e:
            status_placeholder.error(f"An error occurred: {e}", icon="🔥")
            await asyncio.sleep(5)

if __name__ == "__main__":
    # Run the async function to listen to the websocket
    try:
        asyncio.run(listen_to_echopulse())
    except RuntimeError as e:
        # In Streamlit, asyncio.run() can cause a RuntimeError because Streamlit
        # already runs an event loop. A common workaround is to get the existing loop.
        if "cannot run loop while another loop is running" in str(e):
            loop = asyncio.get_event_loop()
            loop.run_until_complete(listen_to_echopulse())
        else:
            raise e