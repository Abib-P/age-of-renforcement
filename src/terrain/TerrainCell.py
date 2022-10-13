from arcade import Sprite


class TerrainCell:
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
