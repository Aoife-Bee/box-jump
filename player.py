from object_types import Rectangle
from constants import *
import pygame

class Player(Rectangle):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_WIDTH, PLAYER_HEIGHT)
        self.attack_box = None
        self.velocity_x = 0
        self.velocity_y = 0
        self.direction = "right"
        self.is_grounded = False
        self.is_jumping = False
        self.state = "idle"

    def draw(self, screen, camera):
        rect = self.rect.move(-camera.x, -camera.y)
        pygame.draw.rect(screen, "black", rect)
        eye_y = rect.centery - 6
        if self.direction == "right":
            eye_x = rect.centerx + 8
        else:
            eye_x = rect.centerx - 8
        pygame.draw.circle(screen, "white", (eye_x, eye_y), 4)
        pygame.draw.rect(screen, "gray", rect, width=1)

    def update(self, dt):
        keys = pygame.key.get_pressed()
        self.update_state(keys)

        self.apply_movement(keys, dt)
        self.apply_gravity(dt)

        if self.velocity_x > self.max_speed:
            self.velocity_x = self.max_speed
        if self.velocity_x < -self.max_speed:
            self.velocity_x = -self.max_speed

    def move_x(self, dt):
        self.x += self.velocity_x * dt
        self.update_rect()

    def move_y(self, dt):
        self.y += self.velocity_y * dt
        self.update_rect()


    def update_state(self, keys):

        if keys[pygame.K_SPACE] and self.is_grounded:
            self.is_jumping = True
            self.velocity_y = -500
            self.is_grounded = False
            return

        if keys[pygame.K_LSHIFT] and not keys[pygame.K_s]:
            self.state = "sprinting"
        elif keys[pygame.K_s]:
            self.state = "crouching"
        elif self.velocity_x != 0:
            self.state = "walking"
        else:
            self.state = "idle"

    def apply_movement(self, keys, dt):

        if self.state == "idle" or self.state == "walking":
            self.walk()
        elif self.state == "sprinting":
            self.sprint()
        elif self.state == "crouching":
            self.crouch_walk()
        
        if keys[pygame.K_a]:
            self.velocity_x -= self.acceleration * dt
            self.direction = "left"
        elif keys[pygame.K_d]:
            self.velocity_x += self.acceleration * dt
            self.direction = "right"
        else:
            self.apply_friction(dt)

    def apply_friction(self, dt):
        if self.velocity_x > 0:
            self.velocity_x -= self.friction * dt
            if self.velocity_x < 0:
                self.velocity_x = 0
        elif self.velocity_x < 0:
            self.velocity_x += self.friction * dt
            if self.velocity_x > 0:
                self.velocity_x = 0

    def apply_gravity(self, dt):
        if not self.is_grounded:
            self.velocity_y += GRAVITY * dt

    def walk(self):
        self.acceleration = 600
        self.friction = 800
        self.max_speed = 300
    
    def sprint(self):
        self.acceleration = 1000
        self.friction = 1200
        self.max_speed = 450
    
    def crouch_walk(self):
        self.acceleration = 400
        self.friction = 800
        self.max_speed = 150
