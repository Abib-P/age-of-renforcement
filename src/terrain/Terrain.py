import math

import arcade
from arcade import SpriteList

from src.terrain.PerlinNoiseUtils import generate_map
from src.terrain.TerrainCell import TerrainCell


class Terrain:
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
        noise = generate_map(width, height, [2, 6, 12, 24], 0.5)
        noise_min = min(min(r) for r in noise)
        noise_max = max(max(r) for r in noise)
        noise_delta = noise_max - noise_min

        noise = [[((col - noise_min) / noise_delta) for col in row] for row in noise]

        cells: [[TerrainCell]] = [[]]
        for y in range(0, height):
            row = []
            for x in range(0, width):
                noise_value = noise[y][x]
                for i, cell in enumerate(available_cells):
                    if noise_value <= ((i + 1) * 1 / len(available_cells)):
                        row.append(cell)
                        break
            cells.append(row)
        return Terrain(width, height, cells)
