import pygame
from object_types import Rectangle


class SpikeTile(Rectangle):
    def __init__(self, x, y, width, height, direction="up", color=None):
        super().__init__(x, y, width, height)
        self.color = color if color else ("gray")
        self.direction = direction
        self.set_hitbox()

    def set_hitbox(self):

        danger_percent = 0.6

        if self.direction == "up":
            hit_height = int(self.height * danger_percent)
            self.hit_box = pygame.Rect(
                self.rect.left,
                self.rect.top,
                self.width,
                hit_height
            )
        elif self.direction == "down":
            hit_height = int(self.height * danger_percent)
            self.hit_box = pygame.Rect(
                self.rect.left,
                self.rect.bottom - hit_height,
                self.width,
                hit_height
            )
        elif self.direction == "left":
            hit_width = int(self.width * danger_percent)
            self.hit_box = pygame.Rect(
                self.rect.left,
                self.rect.top,
                hit_width,
                self.height
            )
        
        elif self.direction == "right":
            hit_width = int(self.width * danger_percent)
            self.hit_box = pygame.Rect(
                self.rect.right - hit_width,
                self.rect.top,
                hit_width,
                self.height
            )

    def draw(self, screen, camera):
        cx, cy = camera.get_draw_offset()
        rect = self.rect.move(-cx, -cy)
        if self.direction == "up" or self.direction == "down":
            num_spikes = max(1, self.width // 20)
            spike_width = self.width // num_spikes
            for i in range(num_spikes):
                spike_x = rect.left + i * spike_width
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
                pygame.draw.polygon(screen, (255,255,255), highlight_points)
                pygame.draw.polygon(screen, (0, 0, 0), points, width=1)
        else:
            num_spikes = max(1, self.height // 20)
            spike_height = self.height // num_spikes
            for i in range(num_spikes):
                spike_y = rect.top + i * spike_height
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
                pygame.draw.polygon(screen, (255,255,255), highlight_points)
                pygame.draw.polygon(screen, (0, 0, 0), points, width=1)

class LavaTile(Rectangle):
    def __init__(self, x, y, width, height, color=None):
        super().__init__(x, y, width, height)
        self.color = color if color else (255, 70, 10)
        self.hit_box = self.rect

    def draw(self, screen, camera):
        cx, cy = camera.get_draw_offset()
        rect = self.rect.move(-cx, -cy)
        highlight_color = (255, 200, 150)

        pygame.draw.rect(screen, self.color, rect)
        pygame.draw.rect(screen, (150,30,5), rect, width=2)
        highlight_height = 2
        highlight_rect = pygame.Rect(
            rect.left + 6,
            rect.top+1,
            rect.width - 8,
            highlight_height
        )
        pygame.draw.rect(screen, highlight_color, highlight_rect)