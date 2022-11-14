import arcade as arcade

from src.configuration import Configuration
from src.main_window import MainWindow
from src.world import World
import matplotlib.pyplot as plt

if __name__ == '__main__':
    config = Configuration("../config/default.ini")
    world = World(config)
    world.learn(1000000)

    windows = MainWindow(world)
    arcade.run()

