import arcade as arcade

from src.configuration import Configuration
from src.main_window import MainWindow
from src.terrain.Terrain import Terrain
from src.terrain.TerrainCell import TerrainCell
from src.world import World

if __name__ == '__main__':
    terrain_cells = [TerrainCell(0, ":resources:images/tiles/water.png", 0),
                     TerrainCell(2, ":resources:images/topdown_tanks/tileSand1.png", 0),
                     TerrainCell(1, ":resources:images/topdown_tanks/tileGrass1.png", 0), ]
    config = Configuration("../config/default.ini")
    # terrain = Terrain.generate_random_terrain(100, 100, terrain_cells)
    terrain = Terrain.generate_random_terrain(config.get_int('Terrain', 'width'), config.get_int('Terrain', 'height'),
                                              terrain_cells)

    # terrain.display_to_console()

    world = World(terrain, None)

    windows = MainWindow(world)
    windows.setup()
    arcade.run()
