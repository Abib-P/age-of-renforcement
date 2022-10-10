import arcade as arcade

from src.main.terrain.terrain import Terrain
from src.main.terrain.terrainCell import TerrainCell


class MainWindow(arcade.Window):
    terrain: Terrain

    def __init__(self, terrain: Terrain):
        super().__init__(1280,
                         720,
                         'Age Of Renforcement')
        self.terrain = terrain

    def setup(self):
        print("setup")

    def on_draw(self):
        arcade.start_render()
        self.terrain.draw()

    def new_game(self):
        print("new game")

    def on_update(self, delta_time):
        pass

    def on_key_press(self, key, modifiers):
        print("key_press: ", key)


if __name__ == '__main__':
    terrain_cells = [TerrainCell(0, ":resources:images/topdown_tanks/tileGrass1.png", 0), TerrainCell(1, ":resources:images/topdown_tanks/tileSand1.png", 0)]
    terrain = Terrain.generate_random_terrain(100, 100, terrain_cells)

    terrain.display_to_console()

    windows = MainWindow(terrain)
    windows.setup()
    arcade.run()
