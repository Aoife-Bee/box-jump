import pygame
from constants import *
from logger import log_state, log_event
from player import Player
from builder import build_level_from_ascii
from rooms import ROOMS, DOORS, START_ROOM
from healthbar import HealthBar
from collisions import *
from room_manager import RoomManager
from death_controller import DeathController
from credits import OpeningCredits, EndCredits
from credits_data import OPENING_CARDS, END_CREDITS

def main():
    pygame.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    player = Player(0,0)
    health_bar = HealthBar()
    death = DeathController(delay=4.0)

    rm = RoomManager(ROOMS, DOORS, TILE_SIZE, build_level_from_ascii)
    opening = OpeningCredits(cards=OPENING_CARDS, seconds_per_card=3.9)
    end_credits = EndCredits(items=END_CREDITS, scroll_speed=70)
    rm.load_room(START_ROOM, player)

    running = True

    while running:
        dt = clock.tick(60) / 1000 

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                log_event("Quit event detected. Exiting the game.")
                running = False
            if opening.active:
                opening.handle_event(event)
                continue
            if end_credits.active:
                end_credits.handle_event(event)
                continue

            player.handle_event(event)

            # TEMP CREDIT TEST TRIGGER
            if event.type == pygame.KEYDOWN and event.key == pygame.K_k:
                end_credits.start(SCREEN_HEIGHT)
        
        keys = pygame.key.get_pressed()

        if opening.active:
            opening.update(dt)
            rm.sky.draw(screen)
            opening.draw(screen)
            pygame.display.flip()
            continue

        if end_credits.active:
            end_credits.update(dt)
            end_credits.draw(screen)
            pygame.display.flip()
            continue

        if death.update(dt, player, rm):
            pass
        else:
            apply_liquid_effects(player, rm.liquid_tiles, dt)
            player.update(dt, keys)

            player.move_x(dt)
            resolve_solid_collisions_x(player, rm.solid_tiles)
            player.move_y(dt)
            resolve_solid_collisions_y(player, rm.solid_tiles)

            hazard_collision(player, rm.hazard_tiles)

            if goal_collision(player, rm.goal):
                end_credits.start(SCREEN_HEIGHT)

            rm.update_transition(dt, player)

        rm.camera.update(player, dt, keys)

        #draw everything
        rm.sky.draw(screen)
        player.draw(screen, rm.camera)
        for tile in rm.tiles_to_draw:
            tile.draw(screen, rm.camera)
        if rm.goal:
            rm.goal.draw(screen, rm.camera)

        health_bar.draw(screen, player.health)
        death.draw(screen)
        pygame.display.flip()



if __name__ == "__main__":
    main()