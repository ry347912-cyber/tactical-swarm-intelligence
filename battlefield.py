class Battlefield:
    WIDTH = 800
    HEIGHT = 600

    def __init__(self):
        self.width = self.WIDTH
        self.height = self.HEIGHT
        self.zones = self._create_zones()
        self.obstacles = self._create_obstacles()

    def _create_zones(self):
        return [
            {"id": 0, "x": 200, "y": 150, "owner": "neutral", "radius": 45, "label": "Alpha"},
            {"id": 1, "x": 400, "y": 300, "owner": "neutral", "radius": 50, "label": "Bravo"},
            {"id": 2, "x": 600, "y": 150, "owner": "neutral", "radius": 45, "label": "Charlie"},
            {"id": 3, "x": 200, "y": 450, "owner": "neutral", "radius": 45, "label": "Delta"},
            {"id": 4, "x": 600, "y": 450, "owner": "neutral", "radius": 45, "label": "Echo"},
        ]

    def _create_obstacles(self):
        return [
            {"x": 355, "y": 195, "radius": 32},
            {"x": 445, "y": 405, "radius": 32},
            {"x": 290, "y": 340, "radius": 26},
            {"x": 510, "y": 260, "radius": 26},
            {"x": 400, "y": 120, "radius": 22},
            {"x": 400, "y": 480, "radius": 22},
        ]

    def update_zones(self, blue_team, red_team):
        for zone in self.zones:
            blue_count = 0
            red_count = 0
            for agent in blue_team:
                if agent.alive:
                    dx = agent.x - zone["x"]
                    dy = agent.y - zone["y"]
                    if (dx * dx + dy * dy) ** 0.5 < zone["radius"]:
                        blue_count += 1
            for agent in red_team:
                if agent.alive:
                    dx = agent.x - zone["x"]
                    dy = agent.y - zone["y"]
                    if (dx * dx + dy * dy) ** 0.5 < zone["radius"]:
                        red_count += 1
            if blue_count > red_count:
                zone["owner"] = "blue"
            elif red_count > blue_count:
                zone["owner"] = "red"
            # else: keep current owner (contested → stays)

    def count_zones(self, team):
        return sum(1 for z in self.zones if z["owner"] == team)

    def to_dict(self):
        return {
            "width": self.width,
            "height": self.height,
            "zones": self.zones,
            "obstacles": self.obstacles,
        }
