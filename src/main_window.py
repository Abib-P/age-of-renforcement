import arcade

from src.world import World


class MainWindow(arcade.Window):
    world: World
    terrain_dx: float
    terrain_dy: float

    def __init__(self, world: World):
        super().__init__(1280,
                         720,
                         'Age Of Renforcement')
        self.__world = world
        self.terrain_dy = 0
        self.terrain_dx = 0

    def setup(self):
        print("setup")

    def on_draw(self):
        arcade.start_render()
        self.__world.terrain.draw()

    def new_game(self):
        print("new game")

    def on_update(self, delta_time):
        self.__world.terrain.move_y(self.terrain_dy)
        self.__world.terrain.move_x(self.terrain_dx)

    def on_key_press(self, key, modifiers):
        print("key_press: ", key)
        if key == arcade.key.P:
            self.__world.terrain.set_scale(self.__world.terrain.scale * 2)
        elif key == arcade.key.M:
            self.__world.terrain.set_scale(self.__world.terrain.scale / 2)
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
