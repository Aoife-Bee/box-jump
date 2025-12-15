import pygame

# Base Class for all game objects
class GameObject(pygame.sprite.Sprite):
    def __init__ (self, x, y):
        self.x = x
        self.y = y

    def update(self, dt):
        pass

    def draw(self, screen):
        pass

class Rectangle(GameObject):
    def __init__ (self, x, y, width, height):
        super().__init__(x, y)
        self.width = width
        self.height = height
        self.rect = pygame.Rect(x, y, width, height)
    
    def update_rect(self):
        self.rect.x = self.x
        self.rect.y = self.y
        self.rect.width = self.width
        self.rect.height = self.height

class Circle(GameObject):
    def __init__ (self, x, y, radius):
        super().__init__(x, y)
        self.radius = radius