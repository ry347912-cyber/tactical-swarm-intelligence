import random


STRATEGIES = [
    "AGGRESSIVE",
    "DEFENSIVE",
    "FLANK",
    "CONTROL",
    "RECON",
    "RETREAT",
]


def determine_strategy(team, enemy_team, owned_zones, enemy_zones):
    """
    Chooses the best macro-strategy for *team* given battlefield state.

    Priority ladder (highest first):
      1. RETREAT  – badly outnumbered
      2. AGGRESSIVE – losing the zone war
      3. DEFENSIVE  – winning the zone war; protect lead
      4. FLANK     – roughly equal forces & zones
      5. CONTROL   – enemy has slight zone lead
      6. RECON     – fallback / information-gather
    """
    alive = [a for a in team if a.alive]
    alive_enemy = [a for a in enemy_team if a.alive]

    if not alive:
        return "RETREAT"

    ratio = len(alive) / max(len(alive_enemy), 1)

    if ratio < 0.45:
        return "RETREAT"

    if owned_zones == 0 and enemy_zones > 0:
        return "AGGRESSIVE"

    if owned_zones > enemy_zones + 1:
        return "DEFENSIVE"

    if owned_zones < enemy_zones:
        return random.choice(["AGGRESSIVE", "CONTROL"])

    if ratio > 1.4:
        return "AGGRESSIVE"

    if ratio < 0.7:
        return "FLANK"

    return random.choice(["FLANK", "CONTROL", "RECON"])
