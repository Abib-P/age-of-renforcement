from src.entity.entity import Entity
from src.terrain.terrain import Terrain


class Building(Entity):
    def __init__(self, terrain: Terrain, **kwargs):
        super().__init__(**kwargs)
        self.__terrain = terrain
