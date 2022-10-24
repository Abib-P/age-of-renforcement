from src.entity.entity import Entity
from src.terrain.terrain import Terrain


class Building(Entity):
    _terrain: Terrain
    def __init__(self, terrain: Terrain, **kwargs):
        super().__init__(**kwargs)
        self._terrain = terrain
