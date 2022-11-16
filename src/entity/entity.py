import arcade
from pyglet.sprite import Sprite

from src.entity.position import Position


class Entity:
    __sprite: Sprite
    _position: Position | None
    _scale: float
    _screen_offset: Position
    __name: str

    def __init__(self, name: str, position: Position, sprite: Sprite):
        self.__sprite = sprite
        self.__name = name
        self._position = position
        self._scale = 10
        self._screen_offset = Position(0, 0)

    def update_screen_pos(self, scale, offset: Position):
        self._scale = scale
        self._screen_offset = offset
        self.__sprite.center_x = (self._position.x + 0.5) * scale + offset.x
        self.__sprite.center_y = (self._position.y - 0.5) * scale + offset.y + scale
        self.__sprite.width = scale
        self.__sprite.height = scale

    def compute_possible_action(self):
        pass

    def draw_on_selection(self):
        pass

    def draw(self):
        self.__sprite.draw()
        arcade.draw_text(self.__name,
                         (self._position.x - 0.5) * self._scale + self._screen_offset.x,
                         (self._position.y + 1.5) * self._scale + self._screen_offset.y,
                         arcade.color.BLACK, self._scale / 2)

    @property
    def position(self):
        return self._position

    @property
    def sprite(self):
        return self.__sprite
