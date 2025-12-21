from constants import *
import pygame

class Camera:
    def __init__(self, level_width, level_height):
        self.x = 0
        self.y = 0
        self.offset_y = 0
        self.level_width = level_width
        self.level_height = level_height
        self.look_speed = 200
    
    def update(self, target, dt, keys):

        if keys[pygame.K_w]:
            self.offset_y -= self.look_speed * dt
        elif keys[pygame.K_s]:
            self.offset_y += self.look_speed * dt
        else:
            if self.offset_y > 0:
                self.offset_y = max(0, self.offset_y - self.look_speed * dt * 2)
            elif self.offset_y < 0:
                self.offset_y = min(0, self.offset_y + self.look_speed * dt * 2)

        max_offset = 150
        self.offset_y = max(-max_offset, min(max_offset, self.offset_y))


        target_cx = target.x + target.rect.width / 2
        target_cy = target.y + target.rect.height / 2


        self.x = target_cx - SCREEN_WIDTH / 2
        self.y = target_cy - SCREEN_HEIGHT / 2 + self.offset_y

        self.x = max(0, min(self.x, self.level_width - SCREEN_WIDTH))
        self.y = max(0, min(self.y, self.level_height - SCREEN_HEIGHT))

    def get_draw_offset(self):
        return int(self.x), int(self.y)