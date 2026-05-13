import math


def update_ai(agent, allies, enemies, zones, obstacles, strategy):
    """
    Per-tick AI update for a single agent.

    Behavioural layers (applied in order, all additive):
      1. Zone attraction
      2. Commander cohesion / influence
      3. Enemy reaction  (attack / retreat / flank)
      4. Squad cohesion
      5. Obstacle avoidance
      6. Speed capping
    """

    # ── 1. Find commander ────────────────────────────────────────
    commander = None
    for ally in allies:
        if ally.rank == "commander":
            commander = ally
            break

    # ── 2. Zone attraction ───────────────────────────────────────
    strategic_zone = None
    best_score = -999_999

    for zone in zones:
        score = 0

        if strategy == "CONTROL":
            if zone["owner"] != agent.team:
                score += 200
        elif strategy == "DEFENSIVE":
            if zone["owner"] == agent.team:
                score += 150
        else:
            if zone["owner"] != agent.team:
                score += 100

        dist = math.sqrt(
            (zone["x"] - agent.x) ** 2 +
            (zone["y"] - agent.y) ** 2
        )
        score -= dist * 0.1

        if score > best_score:
            best_score = score
            strategic_zone = zone

    if strategic_zone:
        dx = strategic_zone["x"] - agent.x
        dy = strategic_zone["y"] - agent.y
        dist = math.sqrt(dx * dx + dy * dy)
        if dist > 0:
            dx /= dist
            dy /= dist

        movement_boost = 0.15
        if strategy == "AGGRESSIVE":
            movement_boost = 0.25
        elif strategy == "DEFENSIVE":
            movement_boost = 0.08
        elif strategy == "RECON":
            movement_boost = 0.30

        agent.vx += dx * movement_boost
        agent.vy += dy * movement_boost

    # ── 3. Commander cohesion / influence ────────────────────────
    if commander and commander.id != agent.id:
        dx = commander.x - agent.x
        dy = commander.y - agent.y
        dist = math.sqrt(dx * dx + dy * dy)

        if 0 < dist < 180:
            dx /= dist
            dy /= dist

            cohesion_boost = 0.08
            if strategy == "DEFENSIVE":
                cohesion_boost = 0.15

            agent.vx += dx * cohesion_boost
            agent.vy += dy * cohesion_boost
            agent.influence = 1
        else:
            agent.influence = 0

    # ── 4. Enemy reaction ────────────────────────────────────────
    nearest_enemy = None
    nearest_distance = 999_999

    for enemy in enemies:
        dist = agent.distance(enemy)
        if dist < nearest_distance:
            nearest_distance = dist
            nearest_enemy = enemy

    if nearest_enemy:
        dx_enemy = nearest_enemy.x - agent.x
        dy_enemy = nearest_enemy.y - agent.y
        dist_enemy = math.sqrt(dx_enemy ** 2 + dy_enemy ** 2)

        if dist_enemy > 0:
            dx_enemy /= dist_enemy
            dy_enemy /= dist_enemy

        if strategy == "RETREAT":
            agent.vx -= dx_enemy * 0.7
            agent.vy -= dy_enemy * 0.7

        elif strategy == "FLANK":
            flank_x = -dy_enemy
            flank_y = dx_enemy
            agent.vx += flank_x * 0.5
            agent.vy += flank_y * 0.5

        else:
            if nearest_distance < 140:
                attack_boost = 0.35
                if strategy == "AGGRESSIVE":
                    attack_boost = 0.55
                if strategy == "DEFENSIVE":
                    attack_boost = 0.20
                if agent.influence:
                    attack_boost += 0.15

                if agent.health > 40:
                    agent.vx += dx_enemy * attack_boost
                    agent.vy += dy_enemy * attack_boost
                else:
                    agent.vx -= dx_enemy * 0.5
                    agent.vy -= dy_enemy * 0.5

    # ── 5. Squad cohesion ────────────────────────────────────────
    cohesion_x = 0.0
    cohesion_y = 0.0
    total = 0

    for ally in allies:
        if ally.id == agent.id:
            continue
        if ally.squad != agent.squad:
            continue
        dist = agent.distance(ally)
        if dist < 150:
            cohesion_x += ally.x
            cohesion_y += ally.y
            total += 1

    if total > 0:
        cohesion_x /= total
        cohesion_y /= total

        cohesion_force = 0.001
        if strategy == "DEFENSIVE":
            cohesion_force = 0.004
        elif strategy == "RECON":
            cohesion_force = 0.0005

        agent.vx += (cohesion_x - agent.x) * cohesion_force
        agent.vy += (cohesion_y - agent.y) * cohesion_force

    # ── 6. Obstacle avoidance ────────────────────────────────────
    agent.avoid_obstacles(obstacles)

    # ── 7. Speed cap ─────────────────────────────────────────────
    speed = math.sqrt(agent.vx ** 2 + agent.vy ** 2)
    max_speed = agent.speed

    if strategy == "RECON":
        max_speed += 1.2
    elif strategy == "RETREAT":
        max_speed += 1.5
    elif strategy == "AGGRESSIVE":
        max_speed += 0.7

    if agent.influence:
        max_speed += 0.5

    if speed > max_speed:
        agent.vx = (agent.vx / speed) * max_speed
        agent.vy = (agent.vy / speed) * max_speed
