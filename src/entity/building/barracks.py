from src.entity.entity import Entity


class Barracks(Entity):
    def __init__(self, name, health_points, position):
        super(Barracks, self).__init__(name=name, health_points=health_points, position=position)

    def create_soldier(self, map):
        pass

    def __str__(self):
        return "Barracks"
