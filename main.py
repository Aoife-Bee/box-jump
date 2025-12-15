import pygame
import sys
from constants import *
from logger import log_state, log_event
from player import Player
from tiles import SolidTile
from hazards import SpikeTile, LavaTile
from builder import build_level_from_ascii
from levels import LEVEL_1


def main():
    pygame.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    solid_tiles, hazard_tiles, player_spawn = build_level_from_ascii(LEVEL_1, tile_size=TILE_SIZE)
    player = Player(*player_spawn)
    tiles = solid_tiles + hazard_tiles

    running = True

    while running:
        dt = clock.tick(60) / 1000 

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                log_event("Quit event detected. Exiting the game.")
                running = False

        player.update(dt)


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
                    elif player.velocity_y < 0:
                        player.rect.top = tile.collision_box.bottom
                        player.y = player.rect.y
                        player.velocity_y = 0

        #draw everything
        screen.fill((135, 206, 235)) # Sky Blue Background
        for tile in tiles:
            tile.draw(screen)
        player.draw(screen)

        #display game objects here
        pygame.display.flip()



if __name__ == "__main__":
    main()