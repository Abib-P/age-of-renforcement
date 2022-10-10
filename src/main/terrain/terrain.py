import random

import arcade
from arcade import SpriteList

from src.main.terrain.terrainCell import TerrainCell


class Terrain:
    available_cells = [TerrainCell(0, "", 0)]

    width: int
    height: int
    cells: [[TerrainCell]]
    cells_sprites: SpriteList

    def __init__(self, width, height, cells) -> None:
        self.cells = cells
        self.height = height
        self.width = width

        self.compute_sprites(50)

    def compute_sprites(self, scale):
        self.cells_sprites = SpriteList()
        for ir, row in enumerate(self.cells):
            for ic, col in enumerate(row):
                sprite = arcade.Sprite(col.resource_path)
                sprite.scale = scale / sprite.width
                sprite.center_x = (ic + 0.5) * scale
                sprite.center_y = (self.height - ir + 0.5) * scale
                self.cells_sprites.append(sprite)

    def display_to_console(self):
        for row in self.cells:
            for col in row:
                print(col.id, end=' ')
            print("")

    def draw(self):
        self.cells_sprites.draw()

    @staticmethod
    def generate_random_terrain(width: int, height: int, available_cells: [TerrainCell]):
        cells: [[TerrainCell]] = [[]]
        for y in range(0, height):
            row = []
            for x in range(0, width):
                row.append(available_cells[random.randrange(len(available_cells))])
            cells.append(row)
        return Terrain(width, height, cells)
