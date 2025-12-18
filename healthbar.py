import pygame

class HealthBar:
    def __init__(self, x=50, y=20, radius=10, gap=8):
        self.x = x
        self.y = y
        self.radius = radius
        self.gap = gap

    def draw(self, screen, health):
        for i in range(health.max_health):
            cx = self.x + i * (self.radius * 2 + self.gap)
            cy = self.y

            pygame.draw.circle(screen, (0, 0, 0), (cx, cy), self.radius, 2)

            if i < health.health:
                pygame.draw.circle(screen, (40, 220, 40), (cx, cy), self.radius - 2)

            

    