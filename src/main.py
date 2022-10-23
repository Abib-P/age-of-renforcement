import arcade as arcade

from src.configuration import Configuration
from src.main_window import MainWindow
from src.world import World

if __name__ == '__main__':
    config = Configuration("../config/default.ini")
    world = World(config)
    windows = MainWindow(world)
    arcade.run()
