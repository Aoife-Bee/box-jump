import pygame

class OpeningCredits:
    """
    skybox background + centered text that fades in and out
    skip by pressing any key
    """
    def __init__(self, cards, seconds_per_card=2.8):
        self.cards = cards  
        self.seconds_per_card = seconds_per_card
        self.active = True
        self.t = 0.0
        self.index = 0
        self._font = None

    def handle_event(self, event):
        if not self.active:
            return
        if event.type == pygame.KEYDOWN:
            self.active = False

    def update(self, dt):
        if not self.active:
            return False
        self.t += dt
        if self.t >= self.seconds_per_card:
            self.t = 0.0
            self.index += 1
            if self.index >= len(self.cards):
                self.active = False

        return self.active

    def draw(self, screen):
        if not self.active:
            return
        if self._font is None:
            self._font = pygame.font.Font(None, 96)

        u = self.t / self.seconds_per_card
        if u < 0.35:
            a = u / 0.35
        elif u > 0.65:
            a = (1.0 - u) / 0.35
        else:
            a = 1.0
        alpha = max(0, min(255, int(255 * a)))

        msg = self.cards[self.index]
        surf = self._font.render(msg, True, (255, 255, 255))
        surf.set_alpha(alpha)
        rect = surf.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
        screen.blit(surf, rect)

        hint_font = pygame.font.Font(None, 28)
        hint = hint_font.render("Press any key to skip", True, (255, 255, 255))
        hint.set_alpha(180)
        hint_rect = hint.get_rect(midbottom=(screen.get_width() // 2, screen.get_height() - 18))
        screen.blit(hint, hint_rect)


class EndCredits:
    """
    Black screen + scrolling credits
    """
    def __init__(self, items, scroll_speed=70):
        self.items = items
        self.scroll_speed = scroll_speed
        self.active = False
        self.y = 0.0
        self._font_title = None
        self._font_heading = None
        self._font_name = None

    def start(self, screen_h):
        self.active = True
        self.y = float(screen_h + 40)

    def handle_event(self, event):
        if not self.active:
            return
        #optional end credits skip - remove # if planning to use
        #if event.type == pygame.KEYDOWN:
            #self.active = False

    def update(self, dt):
        if not self.active:
            return False
        self.y -= self.scroll_speed * dt

        total_height = self._estimate_height()
        if self.y + total_height < -80:
            self.active = False

        return self.active
    
    def _estimate_height(self):
        h = 0
        for kind, _ in self.items:
            if kind == "spacer":
                h += 30
            elif kind == "title":
                h += 90
            elif kind == "heading":
                h += 70
            else: #name
                h += 50

        return h
    
    def draw(self, screen):
        if not self.active:
            return
        
        screen.fill((0,0,0))

        if self._font_title is None:
            self._font_title = pygame.font.Font(None, 80)
            self._font_heading = pygame.font.Font(None, 60)
            self._font_name = pygame.font.Font(None, 44)

        cx = screen.get_width() // 2
        y = self.y

        for kind, text in self.items:
            if kind == "spacer":
                y += 30
                continue
            
            if kind == "title":
                font = self._font_title
                line_gap = 90
            elif kind == "heading":
                font = self._font_heading
                line_gap = 70
            else: #name
                font = self._font_name
                line_gap = 50
        
            surf = font.render(text, True, (255, 255, 255))
            rect = surf.get_rect(center=(cx, int(y)))
            screen.blit(surf, rect)
            y += line_gap
        