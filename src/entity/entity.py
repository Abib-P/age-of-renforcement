class Entity:
    def __init__(self, name, health_points, position):
        self.name = name
        self.hp = health_points
        self.position = position

    def take_damage(self, damage):
        self.__hp -= damage
        if self.__hp <= 0:
            self.__die()

    def __die(self):
        self.__hp = 0
        self.__position = None
