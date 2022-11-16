import copy
from typing import Any

from arcade import SpriteList

from src.entity.entity import Entity
from src.entity.position import Position
from src.terrain.perlin_noise_utils import generate_map
from src.terrain.terrain_cell import TerrainCell


class Terrain:
    __width: int
    __height: int
    __cells: [[TerrainCell]]
    __cells_sprites: SpriteList

    def __init__(self, width: int, height: int, cells: [[TerrainCell]]) -> None:
        self.__cells = cells
        self.__height = height
        self.__width = width
        self.__resources = []

        self.__cells_sprites = SpriteList()
        for ir, row in enumerate(self.__cells):
            for ic, col in enumerate(row):
                self.__cells_sprites.append(col.sprite)

    def add_resource(self, resource: Entity):
        self.__resources.append(resource)
        self.place_entity(resource)

    def update_screen_pos(self, scale, offset: Position):
        for resource in self.__resources:
            resource.update_screen_pos(scale, offset)
        for ir, row in enumerate(self.__cells):
            for ic, col in enumerate(row):
                col.update_screen_pos(scale, Position(int((ic + 0.5) * scale + offset.x),
                                                      int((ir - 0.5) * scale + offset.y + scale)))

    def display_to_console(self):
        for row in self.__cells:
            for col in row:
                print(col.id, end=' ')
            print("")

    def is_in_bound(self, position: Position):
        return 0 <= position.x < self.__width and 0 <= position.y < self.__height

    def is_cell_empty(self, position: Position):
        return self.is_in_bound(position) and \
               ((self.__cells[position.y][position.x].entity is None)
                or (not self.__cells[position.y][position.x].entity.is_alive()))

    def move_entity(self, entity: Entity, destination: Position) -> bool:
        if self.is_cell_empty(destination):
            self.__cells[entity.position.y][entity.position.x].place_entity(None)
            self.__cells[destination.y][destination.x].place_entity(entity)
            return True
        return False

    def place_entity(self, entity: Entity):
        if self.is_in_bound(entity.position):
            self.__cells[entity.position.y][entity.position.x].place_entity(entity)

    def remove_entity(self, entity: Entity):
        if self.is_in_bound(entity.position):
            self.__cells[entity.position.y][entity.position.x].place_entity(None)

    def get_entity_at_position(self, position: Position) -> Any | None:
        if not self.is_in_bound(position):
            return None
        return self.__cells[position.y][position.x].entity

    def collect_resource(self, entity: Entity):
        self.__resources.remove(entity)
        self.__cells[entity.position.y][entity.position.x].place_entity(None)

    def get_nearest_resource(self, position: Position):
        if len(self.__resources) == 0:
            return None
        return min(self.__resources, key=lambda x: x.position.dist(position))

    def draw(self):
        self.__cells_sprites.draw()
        for resource in self.__resources:
            resource.draw()

    def reset(self):
        for ir, row in enumerate(self.__cells):
            for ic, col in enumerate(row):
                col.place_entity(None)
        self.__resources = []

    def save(self, file_path: str):
        f = open(file_path, "w")

        for row in self.__cells:
            for col in row:
                f.write(str(col.id) + " ")
            f.write("\n")

        f.close()

    @property
    def width(self):
        return self.__width

    @property
    def height(self):
        return self.__height

    @staticmethod
    def load(file_path: str, available_cells: [TerrainCell]):
        f = open(file_path, "r")

        lines = f.readlines()

        nb_row = len(lines)
        nb_col = len(lines[0])
        cells: [[TerrainCell]] = [[]]

        for line in lines:
            row = []
            for c in line.split():
                cell = list(filter(lambda x: x.id == int(c), available_cells))
                row.append(copy.deepcopy(cell[0]))
            cells.append(row)

        f.close()
        return Terrain(nb_row, nb_col, cells)

    @staticmethod
    def generate_random_terrain(width: int, height: int, available_cells: [TerrainCell]):
        noise = generate_map(width, height, [2, 6, 12, 24], 0.5)
        noise_min = min(min(r) for r in noise)
        noise_max = max(max(r) for r in noise)
        noise_delta = noise_max - noise_min

        noise = [[((col - noise_min) / noise_delta) for col in row] for row in noise]

        cells: [[TerrainCell]] = []
        for y in range(0, height):
            row = []
            for x in range(0, width):
                noise_value = noise[y][x]
                for i, cell in enumerate(available_cells):
                    if noise_value <= ((i + 1) * 1 / len(available_cells)):
                        row.append(copy.deepcopy(cell))
                        break
            cells.append(row)
        return Terrain(width, height, cells)
