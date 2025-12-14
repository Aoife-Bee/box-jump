import pygame
import sys
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from logger import log_state, log_event
from player import Player
from platforms import Platform


def main():
    pygame.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    player = Player(SCREEN_WIDTH-1100, SCREEN_HEIGHT-100)

    floor = Platform(0, SCREEN_HEIGHT - 50, SCREEN_WIDTH, 50)

    running = True

    while running:
        dt = clock.tick(60) / 1000 

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                log_event("Quit event detected. Exiting the game.")
                running = False

        player.update(dt)

        check_collisions(player, floor)

        #draw everything
        screen.fill((135, 206, 235)) # Sky Blue Background
        floor.draw(screen)
        player.draw(screen)

        #display game objects here
        pygame.display.flip()

def check_collisions(player, platform):
    if player.rect.colliderect(platform.rect):
        if player.velocity_y > 0 and player.rect.bottom <= platform.rect.top + 20:
            player.rect.bottom = platform.rect.top
            player.y = player.rect.y
            player.velocity_y = 0
            player.is_grounded = True
            player.is_jumping = False

if __name__ == "__main__":
    main()