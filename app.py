from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
from swarm_engine import SwarmEngine
import os

app = Flask(__name__, static_folder=".")
CORS(app)

engine = SwarmEngine()


# ── static ───────────────────────────────────────────────────────

@app.route("/")
def index():
    return send_from_directory(".", "index.html")


# ── simulation API ───────────────────────────────────────────────

@app.route("/battle")
def battle():
    """Advance the simulation by one tick and return the new state."""
    engine.update()
    return jsonify(engine.get_state())


@app.route("/state")
def state():
    """Return current state without advancing the tick."""
    return jsonify(engine.get_state())


@app.route("/reset")
def reset():
    """Restart the entire simulation."""
    engine.reset()
    return jsonify({"status": "reset", "message": "Battle restarted!"})


# ── entry point ──────────────────────────────────────────────────

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("FLASK_ENV", "production") == "development"
    print(f"🚀  Tactical Swarm Intelligence running on http://localhost:{port}")
    app.run(host="0.0.0.0", port=port, debug=debug)
