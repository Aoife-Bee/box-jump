from object_types import Rectangle
import pygame

class Tile(Rectangle):
    def __init__(self, x, y, width, height, color="brown"):
        super().__init__(x, y, width, height)
        self.color = color

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
