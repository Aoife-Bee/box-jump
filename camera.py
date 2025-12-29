from constants import *
import pygame

class Camera:
    def __init__(self, level_width, level_height):
        self.x = 0
        self.y = 0
        self.offset_y = 0
        self.level_width = level_width
        self.level_height = level_height

        self.look_speed = 200.0
        self.max_offset = 150.0
        self.return_speed_mult = 2.0
        self.look_dir = 0 # -1 up, +1 down, 0 none

        self.look_hold_time = 0.5
        self.look_hold_timer = 0.0
        self.look_engaged = False
    
    def update(self, target, dt, keys):
        holding_down = keys[pygame.K_s]
        holding_up = keys[pygame.K_w]

        speed_x = abs(getattr(target, "velocity_x", 0.0))
        speed_y = abs(getattr(target, "velocity_y", 0.0))
        is_still = (not keys[pygame.K_a]) and (not keys[pygame.K_d])

        desired_dir = 0

        if holding_up and not holding_down:
            desired_dir = -1

        elif holding_down and not holding_up:
            desired_dir = 1
        
        if desired_dir != self.look_dir:
            self.look_dir = desired_dir
            self.look_hold_timer = 0.0
            self.look_engaged = False


        if self.look_dir != 0 and not self.look_engaged:
            if is_still:
                self.look_hold_timer += dt
                if self.look_hold_timer >= self.look_hold_time:
                    self.look_engaged = True
            else:
                self.look_hold_timer = 0.0

        if self.look_engaged and self.look_dir != 0:
            self.offset_y += self.look_dir * self.look_speed * dt

        else:
            if self.offset_y > 0:
                self.offset_y = max(0.0, self.offset_y - self.look_speed * dt * self.return_speed_mult)
            elif self.offset_y < 0:
                self.offset_y = min (0.0, self.offset_y + self.look_speed * dt * self.return_speed_mult)

        self.offset_y = max(-self.max_offset, min(self.max_offset, self.offset_y))

        target_cx = target.x + target.rect.width / 2
        target_cy = target.y + target.rect.height / 2

        self.x = target_cx - SCREEN_WIDTH / 2
        self.y = target_cy - SCREEN_HEIGHT / 2 + self.offset_y

        self.x = max(0, min(self.x, self.level_width - SCREEN_WIDTH))
        self.y = max(0, min(self.y, self.level_height - SCREEN_HEIGHT))

    def get_draw_offset(self):
        return int(self.x), int(self.y)