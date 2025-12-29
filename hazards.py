import pygame
from object_types import Rectangle
from constants import SPIKE_SIZE


class SpikeTile(Rectangle):
    def __init__(self, x, y, width, height, direction="up", color=None):
        super().__init__(x, y, width, height)
        self.color = color if color else (205, 50, 50)
        self.direction = direction
        self.damage_cause = "spikes"
        self.set_hitbox()
        if self.direction in ("up", "down"):
            self.hit_box = self.hit_box.inflate(-13, -5)
        else:
            self.hit_box = self.hit_box.inflate(-5, -13)
        self.collision_box = self.hit_box

    def set_hitbox(self):

        danger_percent = 0.6
        num_spikes = 3

        if self.direction == "up":
            total_width = SPIKE_SIZE * num_spikes
            start_x = self.rect.centerx - total_width // 2
            hit_height = int(self.height * danger_percent)
            self.hit_box = pygame.Rect(
                start_x,
                self.rect.top,
                total_width,
                hit_height
            )
        elif self.direction == "down":
            total_width = SPIKE_SIZE * num_spikes
            start_x = self.rect.centerx - total_width // 2
            hit_height = int(self.height * danger_percent)
            self.hit_box = pygame.Rect(
                start_x,
                self.rect.bottom - hit_height,
                total_width,
                hit_height
            )
        elif self.direction == "left":
            total_height = SPIKE_SIZE * num_spikes
            start_y = self.rect.centery - total_height // 2
            hit_width = int(self.width * danger_percent)
            self.hit_box = pygame.Rect(
                self.rect.left,
                start_y,
                hit_width,
                total_height
            )
        
        elif self.direction == "right":
            total_height = SPIKE_SIZE * num_spikes
            start_y = self.rect.centery - total_height // 2
            hit_width = int(self.width * danger_percent)
            self.hit_box = pygame.Rect(
                self.rect.right - hit_width,
                start_y,
                hit_width,
                total_height
            )

    def draw(self, screen, camera):
        cx, cy = camera.get_draw_offset()
        rect = self.rect.move(-cx, -cy)
        if self.direction == "up" or self.direction == "down":
            num_spikes = 3
            spike_width = SPIKE_SIZE
            total_width = SPIKE_SIZE * num_spikes
            start_x = rect.centerx - total_width // 2
            for i in range(num_spikes):
                spike_x = start_x + i * spike_width
                if self.direction == "up":
                    points = [
                        (spike_x, rect.bottom),
                        (spike_x + spike_width // 2, rect.top),
                        (spike_x + spike_width, rect.bottom)
                    ]
                    highlight_points = [
                    points[0],
                    points[1],
                    (points[0][0] + 3, points[0][1])
                ]
                else:
                    points = [
                        (spike_x, rect.top),
                        (spike_x + spike_width // 2, rect.bottom),
                        (spike_x + spike_width, rect.top)
                    ]
                    highlight_points = [
                    points[0],                          # top-left
                    points[1],                          # tip
                    (points[0][0] + 3, points[0][1])    # slightly right from base-left
                    ]

                pygame.draw.polygon(screen, self.color, points)
                pygame.draw.polygon(screen, (150,50,30), highlight_points)
                pygame.draw.polygon(screen, (0, 0, 0), points, width=1)
        else:
            num_spikes = 3
            spike_height = SPIKE_SIZE
            total_height = spike_height * num_spikes
            start_y = rect.centery - total_height // 2
            for i in range(num_spikes):

                spike_y = start_y + i * spike_height
                if self.direction == "left":
                    points = [
                        (rect.right, spike_y),
                        (rect.left, spike_y + spike_height // 2),
                        (rect.right, spike_y + spike_height)
                    ]
                    highlight_points = [
                    points[0],                          # top-right
                    points[1],                          # tip (left)
                    (points[0][0], points[0][1] + 3)    # slightly DOWN from top-right
                    ]

                elif self.direction == "right":
                    points = [
                        (rect.left, spike_y),
                        (rect.right, spike_y + spike_height // 2),
                        (rect.left, spike_y + spike_height)
                    ]
                    highlight_points = [
                    points[0],                          # top-left
                    points[1],                          # tip (right)
                    (points[0][0], points[0][1] + 3)    # slightly DOWN from top-left
                    ]

                pygame.draw.polygon(screen, self.color, points) 
                pygame.draw.polygon(screen, (150,50,30), highlight_points)
                pygame.draw.polygon(screen, (0, 0, 0), points, width=1)