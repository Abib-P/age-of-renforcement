import arcade
from pyglet.sprite import Sprite

from src.entity.position import Position


class Entity:
    __sprite: Sprite
    __scale: float
    __screen_offset: Position
    __name: str

    def __init__(self, name: str, health_points: int, position: Position, sprite: Sprite):
        self.__sprite = sprite
        self.__name = name
        self.__hp = health_points
        self.__max_hp = health_points
        self.__position = position
        self.__scale = 10

    def take_damage(self, damage):
        self.__hp -= damage
        if self.__hp <= 0:
            self.__die()

    def set_position(self, position: Position):
        self.__position = position

    def update_screen_pos(self, scale, offset: Position):
        self.__scale = scale
        self.__screen_offset = offset
        self.__sprite.center_x = (self.__position.x + 0.5) * scale + offset.x
        self.__sprite.center_y = (self.__position.y - 0.5) * scale + offset.y
        self.__sprite.width = scale
        self.__sprite.height = scale

    def draw(self):
        self.__sprite.draw()
        arcade.draw_text(self.__name,
                         (self.__position.x - 0.5) * self.__scale + self.__screen_offset.x,
                         (self.__position.y + 1) * self.__scale + self.__screen_offset.y,
                         arcade.color.BLACK, self.__scale / 2)

        arcade.draw_rectangle_filled((self.__position.x + 0.5) * self.__scale + self.__screen_offset.x,
                                     (self.__position.y + 0.5) * self.__scale + self.__screen_offset.y,
                                     15 * (self.__hp / self.__max_hp) * self.__scale / 10,
                                     self.__scale / 2,
                                     arcade.color.GREEN)

        arcade.draw_rectangle_outline((self.__position.x + 0.5) * self.__scale + self.__screen_offset.x,
                                      (self.__position.y + 0.5) * self.__scale + self.__screen_offset.y,
                                      15 * self.__scale / 10,
                                      self.__scale / 2,
                                      arcade.color.BLACK)

    def __die(self):
        self.__hp = 0
        self.__position = None

    @property
    def position(self):
        return self.__position

    @property
    def sprite(self):
        return self.__sprite
