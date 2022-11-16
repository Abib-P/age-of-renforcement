import arcade

from src.entity.building.building import Building
from src.entity.position import Position
from src.entity.unit.militia import Militia
from src.entity.unit.villager import Villager


class TownCenter(Building):
    default_sprites = {}

    def __init__(self, **kwargs):
        super(TownCenter, self).__init__(**kwargs)

    def create_militia(self):
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
            militia.update_screen_pos(self._scale, self._screen_offset)

    def create_villager(self):
        villager = None
        if self._terrain.is_cell_empty(Position(x=self._position.x, y=self._position.y + 1)):
            villager = self.__create_villager(Position(x=self._position.x, y=self._position.y + 1))
        elif self._terrain.is_cell_empty(Position(x=self._position.x + 1, y=self._position.y)):
            villager = self.__create_villager(Position(x=self._position.x + 1, y=self._position.y))
        elif self._terrain.is_cell_empty(Position(x=self._position.x, y=self._position.y - 1)):
            villager = self.__create_villager(Position(x=self._position.x, y=self._position.y - 1))
        elif self._terrain.is_cell_empty(Position(x=self._position.x - 1, y=self._position.y)):
            villager = self.__create_villager(Position(x=self._position.x - 1, y=self._position.y))
        if villager is not None:
            self._player.add_entity(villager)
            self._terrain.place_entity(villager)

    def __create_militia(self, position: Position):
        return Militia(
            terrain=self._terrain,
            name="test",
            sprite=arcade.Sprite(":resources:images/animated_characters/zombie/zombie_idle.png"),
            position=position,
            player=self._player,
            health_points=50,
            moving_points=1,
            attack_points=10,
            unit_range=1
        )

    def __create_villager(self, position: Position):
        return Villager(
            terrain=self._terrain,
            name="test",
            sprite=arcade.Sprite(":resources:images/animated_characters/robot/robot_idle.png"),
            position=position,
            player=self._player,
            health_points=30,
            moving_points=1,
            attack_points=5,
            unit_range=1
        )

    def auto_play(self):
        # self.__create_villager()
        pass
