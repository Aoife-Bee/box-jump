import pygame
from object_types import Circle

class Coin(Circle):
    def __init__(self, x, y, radius, color=None):
        super().__init__(x, y, radius)
        self.color = color
        
    def draw(self, screen, camera):
        self_x = self.x - camera.x
        self_y = self.y - camera.y

        pygame.draw(screen, self.color, (self_x, self_y), self.radius)
