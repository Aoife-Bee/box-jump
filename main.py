import pygame
from constants import *
from logger import log_state, log_event
from player import Player
from builder import build_level_from_ascii
from levels import LEVELS
from camera import Camera
from healthbar import HealthBar
from backgrounds import Sky
from collisions import *



def main():
    pygame.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    level_index = 0
    level_data = LEVELS[level_index]
    layout = level_data["layout"]

    solid_tiles, hazard_tiles, liquid_tiles, player_spawn = build_level_from_ascii(
        layout, tile_size=TILE_SIZE
        )
    player = Player(*player_spawn)
    health_bar = HealthBar()
    tiles = solid_tiles + hazard_tiles + liquid_tiles

    level_width = len(layout[0]) * TILE_SIZE
    level_height = len(layout) * TILE_SIZE
    camera = Camera(level_width, level_height)

    sky = Sky(level_data["sky_top"], level_data["sky_bottom"])

    running = True

    while running:
        dt = clock.tick(60) / 1000 

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                log_event("Quit event detected. Exiting the game.")
                running = False
            
            player.handle_event(event)
        
        keys = pygame.key.get_pressed()

        apply_liquid_effects(player, liquid_tiles, dt)
        player.update(dt, keys)

        player.move_x(dt)
        resolve_solid_collisions_x(player, solid_tiles)
        player.move_y(dt)
        resolve_solid_collisions_y(player, solid_tiles)

        hazard_collision(player, hazard_tiles)

        camera.update(player, dt, keys)


        #draw everything
        sky.draw(screen)
        player.draw(screen, camera)
        for tile in tiles:
            tile.draw(screen, camera)
        health_bar.draw(screen, player.health)

        #display game objects here
        pygame.display.flip()



if __name__ == "__main__":
    main()