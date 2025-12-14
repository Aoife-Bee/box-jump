from object_types import Rectangle
import pygame

class Platform(Rectangle):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self.color = "green"
    
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
