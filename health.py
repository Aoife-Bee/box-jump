

class Health:
    def __init__(self, max_health):
        self.max_health = max_health
        self.health = max_health
        self.is_dead = False

    def take_damage(self, amount):
        if self.is_dead:
            return
        self.health = max(0, self.health - amount)
        if self.health == 0:
            self.is_dead = True
    
    def heal(self, amount):
        if self.is_dead:
            return
        self.health = min(self.max_health, self.health + amount)

    def kill(self):
        self.health = 0
        self.is_dead = True

    def respawn(self):
        if self.is_dead:
            self.health = self.max_health
            self.is_dead = False

