from pyglet.sprite import Sprite

from src.entity.position import Position


class Entity:

    def __init__(self, name: str, health_points: int, position: Position, sprite: Sprite):
        self.__sprite = sprite
        self.__name = name
        self.__hp = health_points
        self.__position = position

    def take_damage(self, damage):
        self.__hp -= damage
        if self.__hp <= 0:
            self.__die()

    def set_position(self, position: Position):
        self.__position = position

    def draw(self):
        self.__sprite.draw()

    def __die(self):
        self.__hp = 0
        self.__position = None

    @property
    def position(self):
        return self.__position

    @property
    def sprite(self):
        return self.__sprite
