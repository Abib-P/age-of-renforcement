from arcade import Sprite

from src.entity.building.building import Building
from src.entity.player_entitiy import PlayerEntity
from src.entity.position import Position
from src.player.player import Player
from src.terrain.terrain import Terrain


class Barracks(Building, PlayerEntity):
    def __init__(self, name: str, health_points: int, position: Position, sprite: Sprite, terrain: Terrain):
        super(Barracks, self).__init__(name=name, health_points=health_points, position=position, sprite=sprite,
                                       terrain=terrain)

    def _create_soldier(self):
        pass

    def play_turn(self, player: Player):
        pass
