from object_types import GameObject
import pygame


class DecoTile(GameObject):
    def __init__(self, x, y, color):
        super().__init__(x, y) 
        self.color = color 

    def draw(self, screen):
        pass # Decorative tiles do not have a defined shape

