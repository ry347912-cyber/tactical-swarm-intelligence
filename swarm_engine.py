from agent import Agent
from battlefield import Battlefield
from combat_system import process_combat
from formation_manager import FormationManager
from strategy_engine import determine_strategy
from tactical_ai import update_ai


class SwarmEngine:
    """
    Top-level simulation driver.
    Call  update()    once per tick (the /battle endpoint does this).
    Call  get_state() to serialise current state for the front-end.
    Call  reset()     to restart the battle.
    """

    TICK_STRATEGY_INTERVAL = 60   # re-evaluate strategy every N ticks

    def __init__(self):
        self.battlefield = Battlefield()
        self.blue_team, self.red_team = self._create_teams()
        self.formation_manager = FormationManager()
        self.tick = 0
        self.attacks: list[dict] = []
        self.blue_strategy = "CONTROL"
        self.red_strategy = "AGGRESSIVE"
        self.winner: str | None = None
        self.log: list[str] = []

    # ── public API ───────────────────────────────────────────────

    def update(self):
        if self.winner:
            return  # battle is over; freeze state

        self.tick += 1
        alive_blue = [a for a in self.blue_team if a.alive]
        alive_red = [a for a in self.red_team if a.alive]

        # check end conditions
        if not alive_blue:
            self.winner = "red"
            self._log("🔴 Red team wins!")
            return
        if not alive_red:
            self.winner = "blue"
            self._log("🔵 Blue team wins!")
            return

        # update zone ownership
        self.battlefield.update_zones(alive_blue, alive_red)
        blue_zones = self.battlefield.count_zones("blue")
        red_zones = self.battlefield.count_zones("red")

        # re-evaluate strategies periodically
        if self.tick % self.TICK_STRATEGY_INTERVAL == 0:
            old_b = self.blue_strategy
            old_r = self.red_strategy
            self.blue_strategy = determine_strategy(alive_blue, alive_red, blue_zones, red_zones)
            self.red_strategy = determine_strategy(alive_red, alive_blue, red_zones, blue_zones)
            if self.blue_strategy != old_b:
                self._log(f"[T{self.tick}] Blue → {self.blue_strategy}")
            if self.red_strategy != old_r:
                self._log(f"[T{self.tick}] Red  → {self.red_strategy}")

        # run tactical AI for each agent
        for agent in alive_blue:
            update_ai(agent, alive_blue, alive_red,
                      self.battlefield.zones, self.battlefield.obstacles,
                      self.blue_strategy)
            agent.update_position(self.battlefield.width, self.battlefield.height)

        for agent in alive_red:
            update_ai(agent, alive_red, alive_blue,
                      self.battlefield.zones, self.battlefield.obstacles,
                      self.red_strategy)
            agent.update_position(self.battlefield.width, self.battlefield.height)

        # resolve combat
        self.attacks = (
            process_combat(alive_blue, alive_red) +
            process_combat(alive_red, alive_blue)
        )

    def get_state(self) -> dict:
        alive_blue = sum(1 for a in self.blue_team if a.alive)
        alive_red = sum(1 for a in self.red_team if a.alive)
        blue_zones = self.battlefield.count_zones("blue")
        red_zones = self.battlefield.count_zones("red")

        return {
            "tick": self.tick,
            "blue_team": [a.to_dict() for a in self.blue_team],
            "red_team": [a.to_dict() for a in self.red_team],
            "battlefield": self.battlefield.to_dict(),
            "attacks": self.attacks,
            "blue_strategy": self.blue_strategy,
            "red_strategy": self.red_strategy,
            "blue_alive": alive_blue,
            "red_alive": alive_red,
            "blue_zones": blue_zones,
            "red_zones": red_zones,
            "winner": self.winner,
            "log": self.log[-20:],   # last 20 events
        }

    def reset(self):
        self.__init__()

    # ── internals ────────────────────────────────────────────────

    def _create_teams(self):
        blue_team = [Agent(i, "blue") for i in range(15)]
        red_team = [Agent(i + 100, "red") for i in range(15)]

        # configure commanders
        for team in (blue_team, red_team):
            cmd = team[0]
            cmd.rank = "commander"
            cmd.health = 250
            cmd.max_health = 250
            cmd.speed = 3.0
            cmd.attack = 18.0
            cmd.range = 110

        # assign squads (3 squads of 5)
        for i, agent in enumerate(blue_team):
            agent.squad = i // 5
        for i, agent in enumerate(red_team):
            agent.squad = i // 5

        return blue_team, red_team

    def _log(self, msg: str):
        self.log.append(msg)
        if len(self.log) > 100:
            self.log = self.log[-100:]
