from object_types import GameObject
import pygame


class Sky:
    def __init__(self, top_color, bottom_color):
        self.top_color = top_color
        self.bottom_color = bottom_color


    def draw(self, screen):
        height = screen.get_height()

        for y in range(height):
            t = y / height
            r = int(self.top_color[0] * (1 - t) + self.bottom_color[0] * t)
            g = int(self.top_color[1] * (1 - t) + self.bottom_color[1] * t)
            b = int(self.top_color[2] * (1 - t) + self.bottom_color[2] * t)
            pygame.draw.line(screen, (r, g, b), (0, y), (screen.get_width(), y))

