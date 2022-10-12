from src.terrain.Terrain import Terrain


class World:
    def __init__(self, terrain: Terrain, entities):
        self.__terrain = terrain
        self.__entities = entities
        self.__turn = 0

    @property
    def terrain(self):
        return self.__terrain

    @property
    def entities(self):
        return self.__entities

    @property
    def turn(self):
        return self.__turn
