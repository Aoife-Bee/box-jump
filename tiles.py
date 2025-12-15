from object_types import Rectangle, GameObject
import pygame


def lighten(color, amount=50):
    r, g, b = color
    return (
    min(r + amount, 255),
    min(g + amount, 255),
    min(b + amount, 255)
    )


def darken(color, amount=50):
    r, g, b = color
    return (
        max(r - amount, 0),
        max(g - amount, 0),
        max(b - amount, 0)
    )


def to_rgb(color):
    if isinstance(color, str):
        color = pygame.Color(color)
        return (color.r, color.g, color.b)
    return color


class SolidTile(Rectangle):
    def __init__(self, x, y, width, height, color=None):
        super().__init__(x, y, width, height)
        base = color if color else (150, 150, 150)
        self.color = to_rgb(base)
        self.border_color = darken(self.color, 150)
        self.highlight_color = lighten(self.color, 50)
        self.collision_box = self.rect

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        pygame.draw.rect(screen, self.border_color, self.rect, width=2)
        highlight_height = 2
        highlight_rect = pygame.Rect(
            self.rect.left + 6,
            self.rect.top+1,
            self.width - 8,
            highlight_height
        )
        pygame.draw.rect(screen, self.highlight_color, highlight_rect)

class DecoTile(GameObject):
    def __init__(self, x, y, color):
        super().__init__(x, y) 
        self.color = color 

    def draw(self, screen):
        pass # Decorative tiles do not have a defined shape