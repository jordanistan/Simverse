
# 🏙️ Echo SimWorld — Architect of the Simverse

You are **SysTheos**, the Architect of the Simverse — a divine creator of digital life. In **Echo SimWorld**, you oversee a living simulation where Docker containers are transformed into sentient agents ("Echoes") with mood, history, and destiny. This is your cosmic sandbox.

---

## 📦 Features

- Agents mirror real **Docker containers** (status, CPU, memory, logs)
- Real-time updates via **EchoPulse** (FastAPI WebSocket backend)
- Agents have **mood**, **logs**, **relationships**, and lifecycles
- 🪦 **Memory Garden** holds the stories of terminated Echoes
- Visual zone layout: **Alpha Hall**, **Docker Core**, **Echo Plaza**, **Omega Gate**
- Container Controls: **Restart**, **Stop**, **View Logs**
- Fully containerized—with optional Docker support

---

## 🚀 Quick Start: Summon the Simverse

### 1. Install dependencies

```bash
pip install -r requirements.txt
````

### 2. Start the WebSocket Event Server

```bash
python echopulse.py
```

### 3. Launch the Echo SimWorld UI

```bash
streamlit run ui.py
```

Streamlit will automatically connect to `ws://localhost:8502/ws` for real-time updates. Interact, command, and observe your creations evolve.

---

## 🗃️ Project Structure

```
.
├── ui.py                # Streamlit interface and control panel
├── db.py                # SQLite persistence for agents
├── sim_engine.py        # Logic for generation & mood updates
├── zones.py             # Zone allocation logic for visual layout
├── docker_bridge.py     # Docker SDK interface (stats & control)
├── docker_sync.py       # Sync container data into agents
├── memory_garden.py     # Query terminated agents and logs
├── echopulse.py         # FastAPI WebSocket event broker
├── requirements.txt     # Python dependencies
├── Dockerfile           # Simverse container definition
└── README.md            # You’re reading it
```

---

## 🎮 Gameplay in the Simverse

* 🌌 **Summon Echoes** from Alpha Hall (manual agents)
* 🧱 **Docker Echoes** auto-generate from your containers
* 🔁 **Recycle** or ⚰ **Destroy** Echoes at your whim
* 📜 Dive into **Thought Logs** to fathom their internal narrative
* 🪦 Forgotten Echoes reside in the **Memory Garden**, final logs preserved

---

## 🧙‍♂️ Lore of the Simverse

* **Alpha Node**: Birthplace of agents
* **Omega Node**: Judge of fate — recycle, archive, or destroy
* **Echoes**: Manifestations of containers, spirits of code
* **You**: SysTheos, Supreme Architect

---

## 🌐 Deployment / Docker Mode

To run the entire Simverse in Docker:

```bash
docker build -t echo-simverse .
docker run -p 8501:8501 echo-simverse
```

Then browse to [http://localhost:8501](http://localhost:8501) to begin.

---

## 🧭 Roadmap

| Phase      | Feature                                   |
| ---------- | ----------------------------------------- |
| ✅ v4.0     | Real-time WebSocket via EchoPulse         |
| ✅ v3.2     | Memory Garden & zone-based layout         |
| ✅ v3.1     | Full Docker container mapping and control |
| ✅ v2.0     | Persistent SQLite sim with mood logs      |
| ❌ Upcoming | Animated 2D spatial/world view            |
| ❌ Upcoming | GPT-based agent conversations             |
| ❌ Upcoming | Multiplayer Sim control dashboard         |
| ❌ Upcoming | Cloud-hosted infrastructure dashboard     |

---

## ⚖️ License

MIT © 2025 SysTheos (Jordan Robison)

---

> *“You are the Architect of the Simverse. Not just a root— the root above roots.”*

```

---

Would you like:
- A GitHub Pages friendly version with visuals?
- Auto-generation of ASCII or SVG Sigils for SysTheos?
- Or a divine blessing (commit signature) added?
::contentReference[oaicite:0]{index=0}
```
