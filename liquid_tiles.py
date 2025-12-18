from object_types import Rectangle
import pygame

class WaterTile(Rectangle):
    def __init__(self, x, y, width, height, color="blue", depth=1.0, slowdown=0.6):
        super().__init__(x, y, width, height)
        self.color = color if color else (10, 70, 255)
        self.depth = depth
        self.slowdown = slowdown

        self.height = int(self.height * depth)
        self.y = y + (height - self.height)
        self.update_rect()

    def draw(self, screen, camera):
        cx, cy = camera.get_draw_offset()
        rect = self.rect.move(-cx, -cy)
        highlight_color = (100, 200, 255)

        pygame.draw.rect(screen, self.color, rect)
        pygame.draw.rect(screen, (5,30,150), rect, width=2)
        highlight_height = 2
        highlight_rect = pygame.Rect(
            rect.left + 6,
            rect.top+1,
            rect.width - 8,
            highlight_height
        )
        pygame.draw.rect(screen, highlight_color, highlight_rect)

class SwampWaterTile(WaterTile):
    def __init__(self, x, y, width, height, color="olive", depth=1.0, slowdown=0.3):
        super().__init__(x, y, width, height, color=color, depth=depth, slowdown=slowdown)