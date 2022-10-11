class Entity:
    def __init__(self, name, health_points, position):
        self.name = name
        self.hp = health_points
        self.position = position

    def take_damage(self, damage):
        self.hp -= damage
        if self.hp <= 0:
            self.die()

    def die(self):
        self.hp = 0
        self.position = None
