from arcade import Sprite

from src.entity.entity import Entity


class TerrainCell:
    __id: int
    __necessary_move: int
    __resource_path: str
    __entity: Entity

    def __init__(self, _id, sprite_path: str, necessary_move, entity=None):
        self.__id = _id
        self.__necessary_move = necessary_move
        self.__sprite = Sprite(sprite_path)
        self.__entity = entity

    def set_position(self, x, y, scale):
        self.__sprite.width = scale
        self.__sprite.height = scale
        self.__sprite.center_x = x
        self.__sprite.center_y = y

    @property
    def sprite(self):
        return self.__sprite

    def place_entity(self, entity):
        self.__entity = entity
