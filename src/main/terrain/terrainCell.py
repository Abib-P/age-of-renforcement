class TerrainCell:
    id: int
    necessary_move: int
    resource_path: str

    def __init__(self, _id, resource_path, necessary_move):
        self.id = _id
        self.necessary_move = necessary_move
        self.resource_path = resource_path

