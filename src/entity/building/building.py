from arcade import Sprite

from src.entity.entity import Entity
from src.entity.position import Position
from src.player.player import Player
from src.terrain.terrain import Terrain


class Building(Entity):
    def __init__(self, name: str, position: Position, sprite: Sprite, terrain: Terrain, health_points: int):
        super().__init__(name=name, position=position, sprite=sprite, health_points=health_points)
        self.__terrain = terrain

    def play_turn(self, player: Player):
        raise NotImplementedError
