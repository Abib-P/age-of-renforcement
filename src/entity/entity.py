from pyglet.sprite import Sprite

from src.entity.position import Position
from src.terrain import Terrain


class Entity:

    def __init__(self, name: str, health_points: int, terrain: Terrain, position: Position, sprite: Sprite):
        self.__sprite = sprite
        self.__name = name
        self.__hp = health_points
        self.__position = position
        self.__terrain = terrain

    def take_damage(self, damage):
        self.__hp -= damage
        if self.__hp <= 0:
            self.__die()

    def set_position(self, position: Position):
        screen_position = self.__terrain.cell_to_screen_position(self.__position)
        pass

    def draw(self):
        self.__sprite.draw()

    def __die(self):
        self.__hp = 0
        self.__position = None
