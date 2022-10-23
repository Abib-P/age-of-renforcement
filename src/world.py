import arcade
from arcade import SpriteList

from src.configuration import Configuration
from src.entity.building.town_center import TownCenter
from src.entity.entity import Entity
from src.entity.movable_entity import MovableEntity
from src.entity.position import Position
from src.entity.unit.militia import Militia
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


def load_terrain(config, path):
    terrain_cells = [TerrainCell(0, ":resources:images/tiles/water.png", 0),
                     TerrainCell(2, ":resources:images/topdown_tanks/tileSand1.png", 0),
                     TerrainCell(1, ":resources:images/topdown_tanks/tileGrass1.png", 0), ]
    terrain = Terrain.load(path, terrain_cells)
    return terrain


class World:
    __terrain: Terrain
    __players: [Player]
    __turn: int
    __entities_sprites: SpriteList

    __scale: float
    __screen_offset: Position

    def __init__(self, config: Configuration):
        self.__terrain = generate_terrain(config)
        self.__terrain.save("./map.txt")
        # self.__terrain = load_terrain(config, "./map.txt")

        self.__scale = 10
        self.__screen_offset = Position(0, 0)

        self.__players = []
        self.__turn = 0
        self.__entities_sprites = SpriteList()

        for i in range(config.get_int('Players', 'number')):
            section_name = "Player_" + str(i + 1)
            pos = Position(config.get_int(section_name, 'town_x'),
                           config.get_int(section_name, 'town_y'))
            town_center = TownCenter(name=config.get_string('Town Center', 'name'),
                                     health_points=config.get_int('Town Center', 'health_points'), position=pos,
                                     sprite=arcade.Sprite(config.get_string(section_name, 'town_center_sprite')),
                                     terrain=self.__terrain)
            self.__terrain.place_entity(town_center)

            pion = Militia(terrain=self.__terrain,
                           name="test", health_points=10,
                           sprite=arcade.Sprite(":resources:images/topdown_tanks/tank_blue.png"),
                           position=Position(pos.x + 1, pos.y + 1),
                           moving_points=10000, attack_points=1, unit_range=1)
            self.__terrain.place_entity(pion)

            self.__players.append(Player(name=config.get_string(section_name, 'name'),
                                         color=config.get_string(section_name, 'color'), entities=[town_center, pion]))
            self.__entities_sprites.append(town_center.sprite)

        self.update_screen_pos()

    def update_screen_pos(self):
        self.terrain.update_screen_pos(self.__scale, self.__screen_offset)
        for player in self.__players:
            for entity in player.entities:
                entity.update_screen_pos(self.__scale, self.__screen_offset)

    def move_x(self, dx):
        self.__screen_offset = Position(self.__screen_offset.x + dx, self.__screen_offset.y)
        self.update_screen_pos()

    def move_y(self, dy):
        self.__screen_offset = Position(self.__screen_offset.x, self.__screen_offset.y + dy)
        self.update_screen_pos()

    def set_scale(self, scale: float):
        self.__scale = scale
        self.update_screen_pos()

    def screen_position_to_terrain(self, position: Position) -> Position:
        return Position(int((position.x - self.__screen_offset.x) / self.__scale),
                        int((position.y - self.__screen_offset.y) / self.__scale))

    def get_entity_on_clic(self, clic: Position) -> Entity:
        return self.__terrain.get_entity(self.screen_position_to_terrain(clic))

    def move_entity(self, entity: Entity, position: Position):
        if isinstance(entity, MovableEntity):
            entity.move(position)

    def draw(self):
        self.__terrain.draw()
        for player in self.__players:
            for entity in player.entities:
                entity.draw()

    @property
    def terrain(self):
        return self.__terrain

    @property
    def players(self):
        return self.__players

    @property
    def turn(self):
        return self.__turn

    @property
    def scale(self):
        return self.__scale
