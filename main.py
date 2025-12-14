import pygame
import sys
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from logger import log_state, log_event


def main():
    pygame.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    running = True

    while running:
        dt = clock.tick(60) / 1000 

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                log_event("Quit event detected. Exiting the game.")
                running = False

        #update game logic

        #draw everything
        screen.fill((135, 206, 235)) # Sky Blue Background

        #display game objects here
        pygame.display.flip()

if __name__ == "__main__":
    main()