import pygame
import sys
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from logger import log_state, log_event
from player import Player
from tiles import SolidTile, SpikeTile, LavaTile


def main():
    pygame.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    player = Player(SCREEN_WIDTH-1100, SCREEN_HEIGHT-100)

        # Create some test tiles manually
    floor = SolidTile(0, SCREEN_HEIGHT - 50, SCREEN_WIDTH, 50, "brown")
    platform1 = SolidTile(300, 400, 200, 20, "green")
    platform2 = SolidTile(600, 300, 150, 20, "green")

    spikes_floor = SpikeTile(500, SCREEN_HEIGHT - 70, 100, 20, "up")
    spikes_wall = SpikeTile(250, 350, 20, 100, "right")
    spikes_wall2 = SpikeTile(800, 25, 20, 100, "left")
    spikes_roof = SpikeTile(400, 200, 100, 20, "down")
    lava = LavaTile(700, SCREEN_HEIGHT - 80, 150, 30)

    tiles = [floor, platform1, platform2, spikes_floor, spikes_wall, spikes_wall2, spikes_roof, lava]

    running = True

    while running:
        dt = clock.tick(60) / 1000 

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                log_event("Quit event detected. Exiting the game.")
                running = False

        player.update(dt)

        for tile in tiles:
            if hasattr(tile, 'collision_box') and tile.collision_box:
                if player.collision_box.colliderect(tile.collision_box):
                    if player.velocity_y > 0 and player.rect.bottom <= tile.collision_box.top + 20:
                        player.rect.bottom = tile.collision_box.top
                        player.y = player.rect.y
                        player.velocity_y = 0
                        player.is_grounded = True
                        player.is_jumping = False
                    elif player.velocity_y < 0 and player.rect.top >= tile.collision_box.bottom - 20:
                        player.rect.top = tile.collision_box.bottom
                        player.y = player.rect.y
                        player.velocity_y = 0
                    
                    if player.velocity_x > 0 and player.rect.right <= tile.collision_box.left + 20:
                        player.rect.right = tile.collision_box.left
                        player.x = player.rect.x
                        player.velocity_x = 0
                    elif player.velocity_x < 0 and player.rect.left >= tile.collision_box.right - 20:
                        player.rect.left = tile.collision_box.right
                        player.x = player.rect.x
                        player.velocity_x = 0

        #draw everything
        screen.fill((135, 206, 235)) # Sky Blue Background
        for tile in tiles:
            tile.draw(screen)
        player.draw(screen)

        #display game objects here
        pygame.display.flip()



if __name__ == "__main__":
    main()