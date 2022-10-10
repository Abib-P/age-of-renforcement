import math
import random

import arcade
from arcade import SpriteList

from src.main.terrain.terrainCell import TerrainCell


class Terrain:
    available_cells = [TerrainCell(0, "", 0)]

    width: int
    height: int
    scale: float
    pos_x: int
    pos_y: int
    cells: [[TerrainCell]]
    cells_sprites: SpriteList

    def __init__(self, width, height, cells) -> None:
        self.cells = cells
        self.height = height
        self.width = width
        self.scale = 10
        self.pos_x = 0
        self.pos_y = 0

        self.cells_sprites = SpriteList()
        for ir, row in enumerate(self.cells):
            for ic, col in enumerate(row):
                self.cells_sprites.append(arcade.Sprite(col.resource_path))

        self.compute_sprites_positions()

    def compute_sprites_positions(self):
        for i, sprite in enumerate(self.cells_sprites):
            sprite.width = self.scale
            sprite.height = self.scale
            sprite.center_x = ((i % self.width) + 0.5 + self.pos_x) * self.scale
            sprite.center_y = (self.height - math.floor(i / self.width) - 0.5 + self.pos_y) * self.scale

    def move_x(self, dx):
        self.pos_x += dx
        self.compute_sprites_positions()

    def move_y(self, dy):
        self.pos_y += dy
        self.compute_sprites_positions()

    def set_scale(self, scale):
        self.scale = scale
        self.compute_sprites_positions()

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
