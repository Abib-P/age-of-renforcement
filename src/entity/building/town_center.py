from src.entity.entity import Entity
from src.entity.position import Position


class TownCenter(Entity):
    def __init__(self, name: str, health_points: int, position: Position):
        super(TownCenter, self).__init__(name=name, health_points=health_points, position=position)

    def create_villager(self):
        pass
