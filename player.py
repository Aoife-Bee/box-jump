from object_types import Rectangle
from constants import *
from health import Health
import pygame

class Player(Rectangle):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_WIDTH, PLAYER_HEIGHT)
        self._init_position(x, y)
        self._init_health()
        self._init_physics()
        self._init_jump()
        self._init_state()
        self._init_damage()

    def _init_position(self, x, y):
        self.x = float(x)
        self.y = float(y)
        self.update_rect()

    def _init_health(self):
        self.health = Health(5)

    def _init_physics(self):
        self.velocity_x = 0
        self.speed_multiplier = 1.0
        self.liquid_slowdown = 1.0
        self.liquid_timer = 0.0
        self.velocity_y = 0
        self.rise_gravity_mult = 0.9
        self.fall_gravity_mult = 1.4
    
    def _init_jump(self):
        self.jump_speed = 680
        self.jump_buffer = 0.0
        self.jump_buffer_time = 0.12
        self.coyote = 0.0
        self.coyote_time = 0.10
        self.jump_cut_multiplier = 0.35
        self.jump_cut_used = False
        self.jump_held = False

    def _init_state(self):
        self.direction = "right"
        self.is_grounded = False
        self.is_sprinting = False
        self.was_sprinting = False
        self.is_jumping = False
        self.in_liquid = False
        self.state = "idle"

    def _init_damage(self):
        self.iframes = 0.0
        self.hurt_timer = 0.0
        self.knockback_timer = 0.0

        self.iframes_time = 1.00
        self.hurt_time = 0.25
        self.knockback_time = 0.25
        self.kb_x_speed = 270
        self.kb_y_speed = 180

    def draw(self, screen, camera):
        if self.iframes > 0:
            if int(self.iframes * 20) % 2 == 0:  # 25 = flicker speed
                return


        cx, cy = camera.get_draw_offset()
        rect = self.rect.move(-cx, -cy)
        pygame.draw.rect(screen, "black", rect)
        eye_y = rect.centery - 6
        if self.direction == "right":
            eye_x = rect.centerx + 8
        else:
            eye_x = rect.centerx - 8
        pygame.draw.circle(screen, "white", (eye_x, eye_y), 4)
        pygame.draw.rect(screen, "gray", rect, width=1)

    def update(self, dt, keys):
        self._update_hurt_timers(dt)
        
        if self.jump_buffer > 0:
            self.jump_buffer -= dt

        if self.is_grounded:
            self.coyote = self.coyote_time
        else:
            if self.coyote > 0:
                self.coyote -= dt
        
        if self.jump_buffer > 0 and self.coyote > 0 and self.knockback_timer <= 0:  
            self.velocity_y = -self.jump_speed
            self.is_grounded = False
            self.is_jumping = True
            self.jump_cut_used =  False
            self.jump_buffer = 0.0
            self.coyote = 0.0

        
        self.update_state(keys)
        self.apply_movement(keys, dt)
        self.apply_gravity(dt)

        if self.velocity_x > self.max_speed:
            self.velocity_x = self.max_speed
        if self.velocity_x < -self.max_speed:
            self.velocity_x = -self.max_speed

    def move_x(self, dt):
        self.x += self.velocity_x * dt * self.speed_multiplier
        self.update_rect()

    def move_y(self, dt):
        self.y += self.velocity_y * dt * self.speed_multiplier
        self.update_rect()

    def update_state(self, keys):
        if keys[pygame.K_s]:
            self.state = "crouching"
            self.is_sprinting = False
            return

        if keys[pygame.K_LSHIFT] and self.is_grounded and self.liquid_timer == 0:
            self.state = "sprinting"
            self.is_sprinting = True
            self.was_sprinting = True
        elif self.is_grounded:
            self.state = "walking"
            self.is_sprinting = False
            self.was_sprinting = False

        if not self.is_grounded and getattr(self, "was_sprinting", False):
            self.is_sprinting = True

    def apply_movement(self, keys, dt):

        if self.knockback_timer > 0:
            self.apply_friction(dt * 0.5)
            return

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

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self.jump_held = True
            self.jump_buffer = self.jump_buffer_time

        if event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
            self.jump_held = False
            if self.velocity_y < 0 and not self.jump_cut_used:
                self.velocity_y *= self.jump_cut_multiplier
                self.jump_cut_used = True

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
        if self.is_grounded:
            self.rise_gravity_mult = 0.9
            self.fall_gravity_mult = 1.4
            return
        
        if self.in_liquid:
            self.rise_gravity_mult = 1.35
            self.fall_gravity_mult = 1.0
        else:
            self.rise_gravity_mult = 0.9
            self.fall_gravity_mult = 1.4

        if self.velocity_y < 0:
            self.velocity_y += GRAVITY * self.rise_gravity_mult * dt
        else:
            self.velocity_y += GRAVITY * self.fall_gravity_mult * dt

    def _update_hurt_timers(self, dt):
        if self.iframes > 0:
            self.iframes = max(0.0, self.iframes - dt)
        if self.hurt_timer > 0:
            self.hurt_timer = max(0.0, self.hurt_timer - dt)
        if self.knockback_timer > 0:
            self.knockback_timer = max(0.0, self.knockback_timer - dt)

    def try_take_damage(self, amount, source_rect=None):
        if self.iframes > 0 or self.health.is_dead:
            return False
        
        self.health.take_damage(amount)

        self.iframes = self.iframes_time
        self.hurt_timer = self.hurt_time
        self.knockback_timer = self.knockback_time

        self.jump_buffer = 0.0
        self.coyote = 0.0
        self.jump_cut_used = True

        if source_rect is not None:
            dir_x = 1 if self.rect.centerx >= source_rect.centerx else -1
        else:
            dir_x = -1 if self.direction == "right" else 1

        self.velocity_x = dir_x * self.kb_x_speed
        self.velocity_y =  -self.kb_y_speed

        return True

    def walk(self):
        self.acceleration = 600
        self.friction = 800
        self.max_speed = 300
    
    def sprint(self):
        self.acceleration = 1000
        self.friction = 1600
        self.max_speed = 450
    
    def crouch_walk(self):
        self.acceleration = 400
        self.friction = 1200
        self.max_speed = 150