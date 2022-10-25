import arcade

from src.entity.building.building import Building
from src.entity.position import Position
from src.entity.unit.militia import Militia


class TownCenter(Building):
    default_sprites = {}

    def __init__(self, **kwargs):
        super(TownCenter, self).__init__(**kwargs)

    def create_villager(self):
        militia = None
        if self._terrain.is_cell_empty(Position(x=self._position.x, y=self._position.y + 1)):
            militia = self.__create_militia(Position(x=self._position.x, y=self._position.y + 1))
        elif self._terrain.is_cell_empty(Position(x=self._position.x + 1, y=self._position.y)):
            militia = self.__create_militia(Position(x=self._position.x + 1, y=self._position.y))
        elif self._terrain.is_cell_empty(Position(x=self._position.x, y=self._position.y - 1)):
            militia = self.__create_militia(Position(x=self._position.x, y=self._position.y - 1))
        elif self._terrain.is_cell_empty(Position(x=self._position.x - 1, y=self._position.y)):
            militia = self.__create_militia(Position(x=self._position.x - 1, y=self._position.y))
        if militia is not None:
            self._player.add_entity(militia)
            self._terrain.place_entity(militia)

    def __create_militia(self, position: Position):
        return Militia(
            terrain=self._terrain,
            name="test",
            sprite=arcade.Sprite(":resources:images/animated_characters/zombie/zombie_idle.png"),
            position=position,
            player=self._player,
            health_points=10,
            moving_points=1,
            attack_points=5,
            unit_range=1
        )

    def auto_play(self):
        # self.__create_villager()
        pass
