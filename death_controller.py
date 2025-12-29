import pygame

class DeathController:
    def __init__(self, delay=4.0):
        self.delay = delay
        self.active = False
        self.timer = 0.0
        self.cause = None

        self._font = None
        self._overlay = None #cached surface

    def start(self, player, cause="hp"):
        if self.active:
            return
        self.active = True
        self.timer = self.delay
        self.cause = cause

        player.velocity_x = 0
        player.velocity_y = 0

        player.health.is_dead = True

    def update(self, dt, player, rm):
        if self.active:
            self.timer -= dt
            if self.timer <= 0:
                self.active = False
                rm.respawn_player(player)
            return True
        
        if player.health.is_dead:
            self.start(player, getattr(player, "last_damage_cause", "hp"))
            return True
        
        fall_margin = rm.tile_size * 6
        if player.rect.top > rm.level_height_px + fall_margin:
            player.health.kill()
            player.health.is_dead = True
            self.start(player, "fall")
            return True
        
        return False
    

    def draw(self, screen):
        if not self.active:
            return

        # lazy init cached overlay
        if self._overlay is None or self._overlay.get_size() != screen.get_size():
            self._overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)

        # fade to black based on remaining time (stronger at start)
        t = max(0.0, min(1.0, self.timer / self.delay))  # 1 -> 0
        alpha = int(180 * (1.0 - t))  # 0 .. 180
        self._overlay.fill((0, 0, 0, alpha))
        screen.blit(self._overlay, (0, 0))

        if self._font is None:
            self._font = pygame.font.Font(None, 96)

        DEATH_MESSAGES = {
            "fall": "You fell to your demise.",
            "spikes": "You were impaled by spikes.",
            "hp": "You died.",
        }

        msg = DEATH_MESSAGES.get(self.cause, "You died.")

        text = self._font.render(msg, True, (255, 255, 255))
        rect = text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
        screen.blit(text, rect)