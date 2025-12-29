import pygame
from object_types import Circle

class GoalOrb(Circle):
    def __init__(self, x, y, radius=14):
        super().__init__(x, y, radius)
        self.color = (255, 255, 0)
        self.collected = False

    def get_rect(self):
        return pygame.Rect(
            int(self.x - self.radius),
            int(self.y - self.radius),
            int(self.radius * 2),
            int(self.radius * 2),
        )
    
    def try_collect(self, player_rect):
        if self.collected:
            return False
        if player_rect.colliderect(self.get_rect()):
            self.collected = True
            return True
        
        return False

    def draw(self, screen, camera):
        if self.collected:
            return
        cx, cy = camera.get_draw_offset()
        sx = int(self.x - cx)
        sy = int(self.y - cy)
        pygame.draw.circle(screen, self.color, (sx, sy), self.radius)
        pygame.draw.circle(screen, (0, 0, 0), (sx, sy), self.radius, 2)
