import math


class FormationManager:
    """
    Applies formation offsets to squad agents.
    Offsets are injected as lightweight velocity nudges so they
    blend naturally with the tactical AI's movement decisions.
    """

    FORMATIONS = ["line", "wedge", "circle", "column"]

    def __init__(self):
        self._squad_formations: dict[int, str] = {}

    def assign_formation(self, squad_id: int, formation: str):
        if formation in self.FORMATIONS:
            self._squad_formations[squad_id] = formation

    def get_formation(self, squad_id: int) -> str:
        return self._squad_formations.get(squad_id, "line")

    def apply(self, agents, cx: float, cy: float):
        if not agents:
            return
        squad_id = agents[0].squad
        formation = self.get_formation(squad_id)
        targets = self._compute_targets(formation, len(agents), cx, cy)
        for agent, (tx, ty) in zip(agents, targets):
            dx = tx - agent.x
            dy = ty - agent.y
            agent.vx += dx * 0.003
            agent.vy += dy * 0.003

    # ── formation geometry ──────────────────────────────────────

    def _compute_targets(self, formation, n, cx, cy):
        if formation == "line":
            return self._line(n, cx, cy)
        if formation == "wedge":
            return self._wedge(n, cx, cy)
        if formation == "circle":
            return self._circle(n, cx, cy)
        return self._column(n, cx, cy)

    @staticmethod
    def _line(n, cx, cy, spacing=38):
        half = (n - 1) * spacing / 2
        return [(cx - half + i * spacing, cy) for i in range(n)]

    @staticmethod
    def _column(n, cx, cy, spacing=38):
        half = (n - 1) * spacing / 2
        return [(cx, cy - half + i * spacing) for i in range(n)]

    @staticmethod
    def _wedge(n, cx, cy, spacing=40):
        targets = []
        for i in range(n):
            row = i // 3
            col = (i % 3) - 1
            targets.append((cx + col * spacing - row * 18, cy + row * spacing))
        return targets

    @staticmethod
    def _circle(n, cx, cy, radius=70):
        targets = []
        for i in range(n):
            angle = (2 * math.pi * i) / n
            targets.append((cx + radius * math.cos(angle), cy + radius * math.sin(angle)))
        return targets
