import random

from src.main.terrain.terrainCell import TerrainCell


class Terrain:
    available_cells = [TerrainCell(0, 0)]

    width: int
    height: int
    cells: [[TerrainCell]]

    def __init__(self, width, height, cells) -> None:
        self.cells = cells
        self.height = height
        self.width = width

    def display_to_console(self):
        for row in self.cells:
            for col in row:
                print(col.id, end=' ')
            print("")

    @staticmethod
    def generate_random_terrain(width: int, height: int, available_cells: [TerrainCell]):
        cells: [[TerrainCell]] = [[]]
        for y in range(0, height):
            row = []
            for x in range(0, width):
                row.append(available_cells[random.randrange(len(available_cells))])
            cells.append(row)
        return Terrain(width, height, cells)
