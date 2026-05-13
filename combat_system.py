def process_combat(team1, team2):
    """
    Resolve ranged combat between two teams.
    Each living attacker fires at the nearest enemy within range.
    Returns a list of attack event dicts for front-end rendering.
    """
    attacks = []

    for attacker in team1:
        if not attacker.alive:
            continue

        best_target = None
        best_dist = float("inf")

        for target in team2:
            if not target.alive:
                continue
            dist = attacker.distance(target)
            if dist < attacker.range and dist < best_dist:
                best_dist = dist
                best_target = target

        if best_target is None:
            continue

        damage = attacker.attack
        if attacker.rank == "commander":
            damage *= 1.6
        if attacker.influence:
            damage *= 1.1

        best_target.health -= damage
        if best_target.health <= 0:
            best_target.health = 0
            best_target.alive = False

        attacks.append(
            {
                "x1": round(attacker.x, 1),
                "y1": round(attacker.y, 1),
                "x2": round(best_target.x, 1),
                "y2": round(best_target.y, 1),
                "team": attacker.team,
                "lethal": not best_target.alive,
            }
        )

    return attacks
