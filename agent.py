import math
import random


class Agent:
    def __init__(self, agent_id, team):
        self.id = agent_id
        self.team = team

        if team == "blue":
            self.x = random.uniform(40, 180)
            self.y = random.uniform(40, 560)
        else:
            self.x = random.uniform(620, 760)
            self.y = random.uniform(40, 560)

        self.vx = 0.0
        self.vy = 0.0
        self.health = 100
        self.max_health = 100
        self.speed = 2.5
        self.attack = random.uniform(6, 14)
        self.range = 85
        self.rank = "soldier"
        self.squad = agent_id // 5
        self.influence = 0
        self.alive = True

    def distance(self, other):
        return math.sqrt(
            (self.x - other.x) ** 2 +
            (self.y - other.y) ** 2
        )

    def avoid_obstacles(self, obstacles):
        for obs in obstacles:
            dx = self.x - obs["x"]
            dy = self.y - obs["y"]
            dist = math.sqrt(dx * dx + dy * dy)
            if dist < obs["radius"] + 22 and dist > 0:
                self.vx += (dx / dist) * 0.6
                self.vy += (dy / dist) * 0.6

    def update_position(self, width, height):
        self.x += self.vx
        self.y += self.vy
        self.vx *= 0.84
        self.vy *= 0.84
        self.x = max(12, min(width - 12, self.x))
        self.y = max(12, min(height - 12, self.y))

    def to_dict(self):
        return {
            "id": self.id,
            "team": self.team,
            "x": round(self.x, 2),
            "y": round(self.y, 2),
            "health": round(self.health, 1),
            "max_health": self.max_health,
            "rank": self.rank,
            "squad": self.squad,
            "influence": self.influence,
            "alive": self.alive,
        }
