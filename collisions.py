def apply_liquid_effects(player, liquid_tiles, dt):
    player.in_liquid = False
    for liquid in liquid_tiles:
        if player.rect.colliderect(liquid.rect):
            player.in_liquid = True
            player.liquid_slowdown = liquid.slowdown
            player.liquid_timer = 0.3
            break
        
    if player.in_liquid:
        player.speed_multiplier = player.liquid_slowdown
    else:
        if player.liquid_timer > 0:
            player.liquid_timer = max(0, player.liquid_timer - dt)
            player.speed_multiplier = player.liquid_slowdown
        else:
            player.speed_multiplier = 1.0

def resolve_solid_collisions_x(player, solid_tiles):
    for tile in solid_tiles:
        box = getattr(tile, "collision_box", None)
        if box and player.rect.colliderect(box):
            if player.velocity_x > 0:
                player.rect.right = box.left
            elif player.velocity_x < 0:
                player.rect.left = box.right

            player.x = player.rect.x
            player.velocity_x = 0

def resolve_solid_collisions_y(player, solid_tiles):
    player.is_grounded = False
    for tile in solid_tiles:    
        box = getattr(tile, "collision_box", None)
        if box and player.rect.colliderect(box):
            if player.velocity_y > 0:
                player.rect.bottom = box.top
                player.is_grounded = True
                player.is_jumping = False
                player.jump_cut_used = False
            elif player.velocity_y < 0:
                player.rect.top = box.bottom

            player.y = player.rect.y
            player.velocity_y = 0

def hazard_collision(player, hazard_tiles):
    for hazard in hazard_tiles:
        hit = getattr(hazard, "hit_box", None)
        if hit and player.rect.colliderect(hit.inflate(2, 2)):
            if player.try_take_damage(1, hit):
                player.last_damage_cause = getattr(hazard, "damage_cause", "hazard")
            return True
    return False

def goal_collision(player, goal):
    if goal is None:
        return False
    return goal.try_collect(player.rect)