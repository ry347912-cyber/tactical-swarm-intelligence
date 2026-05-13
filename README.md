# TACTICAL SWARM INTELLIGENCE

> A real-time multi-agent battle simulation built with Python (Flask) and a canvas-based tactical HUD.

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.0-000000?style=flat-square&logo=flask)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

---

## Overview

Tactical Swarm Intelligence is a multi-agent AI simulation where two teams of autonomous units fight for zone control on a procedural battlefield. Each agent perceives its local environment and makes independent movement/attack decisions every tick, producing emergent squad-level tactics.

The **Python backend** runs the simulation and exposes a REST API. The **HTML frontend** renders the battlefield in real time on a `<canvas>`, displaying unit health bars, zone capture progress, strategy indicators, and a live event log.

---

## Features

| Feature | Details |
|---|---|
| **Swarm AI** | Per-agent behavioural layers: zone attraction, commander cohesion, enemy engagement, squad cohesion, obstacle avoidance |
| **6 strategies** | `AGGRESSIVE` `DEFENSIVE` `CONTROL` `FLANK` `RECON` `RETREAT` — auto-selected based on battlefield state |
| **Commanders** | One commander per team; nearby soldiers gain +attack bonus and +speed from their influence aura |
| **Combat system** | Range-based ranged fire; commanders deal ×1.6 damage; influenced soldiers deal ×1.1 |
| **5 capture zones** | Alpha, Bravo, Charlie, Delta, Echo — zones flip owner when more agents are inside |
| **6 obstacles** | Solid terrain features that agents avoid |
| **Formation manager** | `line`, `wedge`, `circle`, `column` formations available per squad |
| **Live HUD** | Scanline-overlay tactical interface; per-unit HP bars; zone control bar; strategy badges; event log |
| **Speed control** | ×1 / ×2 / ×5 / ×10 simulation speed via dropdown |

---

## Project Structure

```
tactical-swarm-intelligence/
│
├── app.py                # Flask REST API entry point
├── agent.py              # Agent class (state + physics)
├── battlefield.py        # Battlefield, zones, obstacles
├── combat_system.py      # Range-based damage resolution
├── formation_manager.py  # Squad formation geometry
├── strategy_engine.py    # Macro-strategy selector
├── swarm_engine.py       # Simulation orchestrator
├── tactical_ai.py        # Per-agent behavioural update
│
├── index.html            # Canvas-based tactical frontend
├── requirements.txt      # Python dependencies
└── README.md
```

---

## Quick Start

### 1. Clone

```bash
git clone https://github.com/<your-username>/tactical-swarm-intelligence.git
cd tactical-swarm-intelligence
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the server

```bash
python app.py
```

The server starts at `http://localhost:5000`.

### 4. Open the frontend

Open `index.html` in your browser **or** navigate to `http://localhost:5000` (the Flask app serves it automatically).

Press **▶ START** in the HUD to begin the simulation.

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Serves `index.html` |
| `GET` | `/battle` | Advance simulation by **one tick**, return state |
| `GET` | `/state` | Return current state **without** advancing |
| `GET` | `/reset` | Restart the simulation from scratch |

### State object (JSON)

```json
{
  "tick": 420,
  "blue_team": [ { "id": 0, "x": 123.4, "y": 200.1, "health": 85.2, "rank": "commander", ... } ],
  "red_team":  [ ... ],
  "battlefield": {
    "width": 800, "height": 600,
    "zones": [ { "id": 0, "x": 200, "y": 150, "owner": "blue", "radius": 45, "label": "Alpha" } ],
    "obstacles": [ { "x": 355, "y": 195, "radius": 32 } ]
  },
  "attacks": [ { "x1": 120, "y1": 200, "x2": 300, "y2": 250, "team": "blue", "lethal": false } ],
  "blue_strategy": "CONTROL",
  "red_strategy": "AGGRESSIVE",
  "blue_alive": 12,
  "red_alive": 9,
  "blue_zones": 3,
  "red_zones": 1,
  "winner": null,
  "log": [ "[T60] Blue → DEFENSIVE", "[T120] Red → FLANK" ]
}
```

---

## AI Architecture

### Behavioural Layers (per tick, per agent)

Each agent runs `update_ai()` which applies **additive velocity impulses** in this order:

```
1. Zone attraction        → move toward highest-scoring uncaptured zone
2. Commander cohesion     → if within 180 px of commander, gain "influence"
3. Enemy engagement       → ATTACK / FLANK / RETREAT based on strategy
4. Squad cohesion         → stay near same-squad allies within 150 px
5. Obstacle avoidance     → push away from terrain
6. Speed cap              → clamp |velocity| to max_speed
```

### Strategy Selection (every 60 ticks)

```python
if alive_ratio < 0.45       → RETREAT
if owned_zones == 0         → AGGRESSIVE
if owned_zones > enemy + 1  → DEFENSIVE
if owned_zones < enemy      → AGGRESSIVE or CONTROL
if ratio > 1.4              → AGGRESSIVE
if ratio < 0.7              → FLANK
else                        → random(FLANK, CONTROL, RECON)
```

### Combat

- Each attacker fires at the **nearest enemy within range** (85 px for soldiers, 110 px for commanders)
- Base damage: 6–14 (random per-agent); commanders ×1.6; influenced agents ×1.1
- Agents retreat from enemies when `health < 40`

---

## Configuration

| Parameter | Location | Default | Effect |
|---|---|---|---|
| Team size | `swarm_engine.py` `_create_teams` | 15 | Units per side |
| Commander HP | `swarm_engine.py` | 250 | Commander survivability |
| Strategy interval | `swarm_engine.py` | 60 ticks | How often strategy re-evaluates |
| Zone radius | `battlefield.py` | 45–50 | Capture point size |
| Agent speed | `agent.py` | 2.5 | Base movement speed |
| Attack range | `agent.py` | 85 | Soldier firing range |
| Commander range | `swarm_engine.py` | 110 | Commander firing range |

---

## Extending the Project

**Add a new strategy:**
1. Add the name to `STRATEGIES` in `strategy_engine.py`
2. Add strategy conditions in `determine_strategy()`
3. Handle the new strategy tag in `tactical_ai.py` (`update_ai()`)

**Add more agents or teams:**
Modify `_create_teams()` in `swarm_engine.py`. The AI and combat system handle arbitrary numbers.

**Plug in an LLM strategy commander:**
Replace or wrap `determine_strategy()` to call an external API and return a strategy string.

---

## Requirements

- Python 3.10+
- `flask >= 3.0.0`
- `flask-cors >= 4.0.0`
- Any modern browser (Chrome, Firefox, Edge, Safari)

---

## License

MIT — see `LICENSE` for details.

---

*Built with Python · Flask · HTML5 Canvas*
