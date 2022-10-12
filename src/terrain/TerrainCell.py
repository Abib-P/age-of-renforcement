class TerrainCell:
    id: int
    necessary_move: int
    resource_path: str

    def __init__(self, _id, resource_path, necessary_move, entity=None):
        self.__id = _id
        self.__necessary_move = necessary_move
        self.__resource_path = resource_path
        self.__entity = entity
