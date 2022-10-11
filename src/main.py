import arcade as arcade

from src.terrain.Terrain import Terrain
from src.terrain.TerrainCell import TerrainCell


class MainWindow(arcade.Window):
    terrain: Terrain
    terrain_dx: float
    terrain_dy: float

    def __init__(self, terrain: Terrain):
        super().__init__(1280,
                         720,
                         'Age Of Renforcement')
        self.terrain = terrain
        self.terrain_dy = 0
        self.terrain_dx = 0

    def setup(self):
        print("setup")

    def on_draw(self):
        arcade.start_render()
        self.terrain.draw()

    def new_game(self):
        print("new game")

    def on_update(self, delta_time):
        terrain.move_y(self.terrain_dy)
        terrain.move_x(self.terrain_dx)

    def on_key_press(self, key, modifiers):
        print("key_press: ", key)
        if key == arcade.key.P:
            terrain.set_scale(terrain.scale * 2)
        elif key == arcade.key.M:
            terrain.set_scale(terrain.scale / 2)
        elif key == arcade.key.Z:
            self.terrain_dy = -1
        elif key == arcade.key.S:
            self.terrain_dy = 1
        elif key == arcade.key.Q:
            self.terrain_dx = 1
        elif key == arcade.key.D:
            self.terrain_dx = -1

    def on_key_release(self, key: int, modifiers: int):
        super().on_key_release(key, modifiers)
        if key == arcade.key.Z or key == arcade.key.S:
            self.terrain_dy = 0
        elif key == arcade.key.Q or key == arcade.key.D:
            self.terrain_dx = 0


if __name__ == '__main__':
    terrain_cells = [TerrainCell(0, ":resources:images/tiles/water.png", 0),
                     TerrainCell(2, ":resources:images/topdown_tanks/tileSand1.png", 0),
                     TerrainCell(1, ":resources:images/topdown_tanks/tileGrass1.png", 0), ]
    terrain = Terrain.generate_random_terrain(100, 100, terrain_cells)

    terrain.display_to_console()

    windows = MainWindow(terrain)
    windows.setup()
    arcade.run()
