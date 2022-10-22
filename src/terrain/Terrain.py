import copy

from arcade import SpriteList

from src.entity.entity import Entity
from src.entity.position import Position
from src.terrain.PerlinNoiseUtils import generate_map
from src.terrain.TerrainCell import TerrainCell


class Terrain:
    width: int
    height: int
    cells: [[TerrainCell]]
    __cells_sprites: SpriteList

    def __init__(self, width: int, height: int, cells: [[TerrainCell]]) -> None:
        self.cells = cells
        self.height = height
        self.width = width

        self.__cells_sprites = SpriteList()
        for ir, row in enumerate(self.cells):
            for ic, col in enumerate(row):
                self.__cells_sprites.append(col.sprite)

    def update_screen_pos(self, scale, offset: Position):
        for ir, row in enumerate(self.cells):
            for ic, col in enumerate(row):
                col.update_screen_pos(scale, Position(int((ic + 0.5) * scale + offset.x),
                                                      int((ir - 0.5) * scale + offset.y)))

    def display_to_console(self):
        for row in self.cells:
            for col in row:
                print(col.id, end=' ')
            print("")

    def place_entity(self, entity: Entity):
        self.cells[entity.position.y][entity.position.x].place_entity(entity)

    def draw(self):
        self.__cells_sprites.draw()

    def save(self, file_path: str):
        f = open(file_path, "w")

        for row in self.cells:
            for col in row:
                f.write(str(col.id) + " ")
            f.write("\n")

        f.close()

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
