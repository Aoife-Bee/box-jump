from object_types import Rectangle, GameObject
import pygame

class SolidTile(Rectangle):
    def __init__(self, x, y, width, height, color=None):
        super().__init__(x, y, width, height)
        self.color = color if color else ("red")
        self.collision_box = self.rect

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)


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

    def draw(self, screen):
        if self.direction == "up" or self.direction == "down":
            num_spikes = max(1, self.width // 20)
            spike_width = self.width // num_spikes
            for i in range(num_spikes):
                spike_x = self.rect.left + i * spike_width
                if self.direction == "up":
                    points = [
                        (spike_x, self.rect.bottom),
                        (spike_x + spike_width // 2, self.rect.top),
                        (spike_x + spike_width, self.rect.bottom)
                    ]
                elif self.direction == "down":
                    points = [
                        (spike_x, self.rect.top),
                        (spike_x + spike_width // 2, self.rect.bottom),
                        (spike_x + spike_width, self.rect.top)
                    ]
                pygame.draw.polygon(screen, self.color, points)
        else:
            num_spikes = max(1, self.height // 20)
            spike_height = self.height // num_spikes
            for i in range(num_spikes):
                spike_y = self.rect.top + i * spike_height
                if self.direction == "left":
                    points = [
                        (self.rect.right, spike_y),
                        (self.rect.left, spike_y + spike_height // 2),
                        (self.rect.right, spike_y + spike_height)
                    ]
                elif self.direction == "right":
                    points = [
                        (self.rect.left, spike_y),
                        (self.rect.right, spike_y + spike_height // 2),
                        (self.rect.left, spike_y + spike_height)
                    ]
                pygame.draw.polygon(screen, self.color, points)

class LavaTile(Rectangle):
    def __init__(self, x, y, width, height, color=None):
        super().__init__(x, y, width, height)
        self.color = color if color else ("orange")
        self.hit_box = self.rect

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)