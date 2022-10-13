from arcade import Sprite

from src.entity.entity import Entity
from src.entity.position import Position
from src.terrain.Terrain import Terrain


class Barracks(Entity):
    def __init__(self, name: str, health_points: int, position: Position, sprite: Sprite, terrain: Terrain):
        super(Barracks, self).__init__(name=name, health_points=health_points, position=position, sprite=sprite,
                                       terrain=terrain)

    def create_soldier(self):
        pass

    def __str__(self):
        return "Barracks"