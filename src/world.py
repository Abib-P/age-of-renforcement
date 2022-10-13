import arcade

from src.configuration import Configuration
from src.entity.building.town_center import TownCenter
from src.entity.position import Position
from src.player.player import Player
from src.terrain.Terrain import Terrain
from src.terrain.TerrainCell import TerrainCell


def generate_terrain(config):
    terrain_cells = [TerrainCell(0, ":resources:images/tiles/water.png", 0),
                     TerrainCell(2, ":resources:images/topdown_tanks/tileSand1.png", 0),
                     TerrainCell(1, ":resources:images/topdown_tanks/tileGrass1.png", 0), ]
    terrain = Terrain.generate_random_terrain(config.get_int('Terrain', 'width'),
                                              config.get_int('Terrain', 'height'),
                                              terrain_cells)
    return terrain


class World:
    def __init__(self, config: Configuration):
        self.__terrain = generate_terrain(config)

        self.__players = []
        for i in range(config.get_int('Players', 'number')):
            section_name = "Player_" + str(i + 1)
            pos = Position(config.get_int(section_name, 'town_x'),
                           config.get_int(section_name, 'town_y'))
            center = TownCenter(name=config.get_string('Town Center', 'name'),
                                health_points=config.get_int('Town Center', 'health_points'), position=pos,
                                sprite=arcade.Sprite(config.get_string(section_name, 'town_center_sprite')),
                                terrain=self.__terrain)
            self.__players = Player(name=config.get_string(section_name, 'name'), color="oui", entities=[center])

        self.__turn = 0

    @property
    def terrain(self):
        return self.__terrain

    @property
    def players(self):
        return self.__players

    @property
    def turn(self):
        return self.__turn
