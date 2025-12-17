import pygame
import sys
from constants import *
from logger import log_state, log_event
from player import Player
from solid_tiles import SolidTile
from hazards import SpikeTile
from liquid_tiles import WaterTile
from builder import build_level_from_ascii
from levels import LEVEL_1
from camera import Camera


def main():
    pygame.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    solid_tiles, hazard_tiles, liquid_tiles, player_spawn = build_level_from_ascii(LEVEL_1, tile_size=TILE_SIZE)
    player = Player(*player_spawn)
    tiles = solid_tiles + hazard_tiles + liquid_tiles

    level_width = len(LEVEL_1[0]) * TILE_SIZE
    level_height = len(LEVEL_1) * TILE_SIZE

    camera = Camera(level_width, level_height)

    running = True

    while running:
        dt = clock.tick(60) / 1000 

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                log_event("Quit event detected. Exiting the game.")
                running = False
            
            player.handle_event(event)
        
        keys = pygame.key.get_pressed()

        player.update(dt, keys)


        for liquid in liquid_tiles:
            if player.rect.colliderect(liquid.rect):
                player.in_liquid = True
                player.speed_multiplier = 1.0 * liquid.slowdown
                player.liquid_timer = 0.2
        
        if player.liquid_timer > 0:
            player.liquid_timer -= dt
            player.speed_multiplier = 1.0 * liquid.slowdown
        else:
            player.speed_multiplier = 1.0




        player.move_x(dt)
        for tile in solid_tiles:
            if hasattr(tile, "collision_box") and tile.collision_box:
                if player.rect.colliderect(tile.collision_box):
                    if player.velocity_x > 0:
                        player.rect.right = tile.collision_box.left
                        player.x = player.rect.x
                        player.velocity_x = 0
                    elif player.velocity_x < 0:
                        player.rect.left = tile.collision_box.right
                        player.x = player.rect.x
                        player.velocity_x = 0
        player.move_y(dt)
        player.is_grounded = False
        for tile in solid_tiles:    
            if hasattr(tile, 'collision_box') and tile.collision_box:
                if player.rect.colliderect(tile.collision_box):
                    if player.velocity_y > 0:
                        player.rect.bottom = tile.collision_box.top
                        player.y = player.rect.y
                        player.velocity_y = 0
                        player.is_grounded = True
                        player.is_jumping = False
                        player.jump_cut_used = False
                    elif player.velocity_y < 0:
                        player.rect.top = tile.collision_box.bottom
                        player.y = player.rect.y
                        player.velocity_y = 0

        for hazard in hazard_tiles:
            if hasattr(hazard, "hit_box") and hazard.hit_box:
                if player.rect.colliderect(hazard.hit_box):
                    pass

        camera.update(player, dt, keys)


        #draw everything
        screen.fill((135, 206, 235)) # Sky Blue Background
        player.draw(screen, camera)
        for tile in tiles:
            tile.draw(screen, camera)

        #display game objects here
        pygame.display.flip()



if __name__ == "__main__":
    main()