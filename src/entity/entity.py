import arcade
from pyglet.sprite import Sprite

from src.entity.position import Position


class Entity:
    __sprite: Sprite
    _position: Position
    _scale: float
    _screen_offset: Position
    __name: str

    def __init__(self, name: str, health_points: int, position: Position, sprite: Sprite):
        self.__sprite = sprite
        self.__name = name
        self.__hp = health_points
        self.__max_hp = health_points
        self._position = position
        self._scale = 10

    def take_damage(self, damage):
        self.__hp -= damage
        if self.__hp <= 0:
            self.__die()

    def set_position(self, position: Position):
        self._position = position

    def update_screen_pos(self, scale, offset: Position):
        self._scale = scale
        self._screen_offset = offset
        self.__sprite.center_x = (self._position.x + 0.5) * scale + offset.x
        self.__sprite.center_y = (self._position.y - 0.5) * scale + offset.y + scale
        self.__sprite.width = scale
        self.__sprite.height = scale

    def draw_on_selection(self):
        pass

    def draw(self):
        self.__sprite.draw()
        arcade.draw_text(self.__name,
                         (self._position.x - 0.5) * self._scale + self._screen_offset.x,
                         (self._position.y + 1) * self._scale + self._screen_offset.y,
                         arcade.color.BLACK, self._scale / 2)

        arcade.draw_rectangle_filled((self._position.x + 0.5) * self._scale + self._screen_offset.x,
                                     (self._position.y + 0.5) * self._scale + self._screen_offset.y,
                                     15 * (self.__hp / self.__max_hp) * self._scale / 10,
                                     self._scale / 2,
                                     arcade.color.GREEN)

        arcade.draw_rectangle_outline((self._position.x + 0.5) * self._scale + self._screen_offset.x,
                                      (self._position.y + 0.5) * self._scale + self._screen_offset.y,
                                      15 * self._scale / 10,
                                      self._scale / 2,
                                      arcade.color.BLACK)

    def __die(self):
        self.__hp = 0
        self._position = None

    @property
    def position(self):
        return self._position

    @property
    def sprite(self):
        return self.__sprite
