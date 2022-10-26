import random

import arcade

from src.ai.militia_ai import MilitiaAi
from src.configuration import Configuration
from src.entity.building.town_center import TownCenter
from src.entity.entity import Entity
from src.entity.player_entitiy import PlayerEntity
from src.entity.position import Position
from src.entity.unit.militia import Militia
from src.player.player import Player
from src.terrain.terrain import Terrain
from src.terrain.terrain_cell import TerrainCell


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
    __config: Configuration
    __terrain: Terrain
    __current_player_index: int
    __current_player: Player
    __players: [Player]
    __turn: int

    __scale: float
    __screen_offset: Position

    __militia_ai: MilitiaAi

    def __init__(self, config: Configuration):
        self.__terrain = generate_terrain(config)
        self.__config = config
        # self.__terrain.save("./map.txt")
        # self.__terrain = load_terrain(config, "./map.txt")

        self.__scale = 10
        self.__screen_offset = Position(0, 0)

        self.__militia_ai = MilitiaAi([], alpha=0.8, gamma=0.8)
        # self.__militia_ai.load("./ai.ai")
        self.reset()

    def reset(self):
        self.__players = []
        self.__turn = 0

        for i in range(self.__config.get_int('Players', 'number')):
            section_name = "Player_" + str(i + 1)
            player = Player(
                name=self.__config.get_string(section_name, 'name'),
                color=self.__config.get_string(section_name, 'color'),
                is_human=self.__config.get_bool(section_name, 'human'),
            )

            town_center = self.create_town_center(self.__config, section_name, player, self.__terrain)
            town_center.create_villager()
            self.__terrain.place_entity(town_center)
            self.__players.append(player)
            self.add_initial_unit_to_player(player, units=[town_center])

        self.__current_player_index = 0
        self.__current_player = self.__players[self.__current_player_index]
        self.update_screen_pos()

        self.__militia_ai.players = self.__players
        self.__militia_ai.save("./ai.ai")

    @staticmethod
    def add_initial_unit_to_player(player, units: [Entity]):
        for unit in units:
            player.add_entity(unit)

    def create_town_center(self, config: Configuration, section_name: str, player: Player,
                           terrain: Terrain) -> TownCenter:
        pos: Position
        if not self.__players:
            pos = Position(random.randrange(terrain.width), random.randrange(terrain.height))
        else:
            old_pos = self.__players[0].get_town_center().position
            pos = Position(random.randrange(terrain.width), random.randrange(terrain.height))
            while pos.dist(old_pos) < terrain.width / 3:
                pos = Position(random.randrange(terrain.width), random.randrange(terrain.height))
        return TownCenter(name=config.get_string('Town Center', 'name'),
                          health_points=config.get_int('Town Center', 'health_points'),
                          position=pos,
                          player=player,
                          sprite=arcade.Sprite(config.get_string(section_name, 'town_center_sprite')),
                          terrain=self.__terrain)

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
        return self.__terrain.get_entity_at_position(self.screen_position_to_terrain(clic))

    def action_entity(self, entity: Entity, position: Position):
        if not self.__current_player.is_human:
            pass
        elif isinstance(entity, PlayerEntity) and entity.belongs_to(self.__current_player):
            entity.on_action(position)

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

    def _next_player(self):
        self.__current_player.end_turn()
        self.__current_player_index = (self.__current_player_index + 1) % len(self.__players)
        self.__current_player = self.__players[self.__current_player_index]

    def player_end_turn(self):
        if self.__current_player.is_human:
            self._next_player()

    def is_game_ended(self) -> bool:
        return len([p for p in self.__players if p.is_alive()]) == 1

    def play_turn(self):
        if self.__current_player.is_human:
            return
        else:
            for entity in filter(lambda x: isinstance(x, Militia), self.__current_player.entities):
                entity.compute_possible_action()
                # entity.on_action(self.__militia_ai.chose_action(entity))
                self.__militia_ai.step(entity)
        self._next_player()
