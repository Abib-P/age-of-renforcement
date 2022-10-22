import arcade

from src.world import World


class MainWindow(arcade.Window):
    world: World
    world_dx: float
    world_dy: float

    def __init__(self, world: World):
        super().__init__(1280,
                         720,
                         'Age Of Renforcement')
        self.__world = world
        self.world_dy = 0
        self.world_dx = 0

    def setup(self):
        print("setup")

    def on_draw(self):
        arcade.start_render()
        self.__world.draw()

    def new_game(self):
        print("new game")

    def on_update(self, delta_time):
        self.__world.move_y(self.world_dy)
        self.__world.move_x(self.world_dx)

    def on_key_press(self, key, modifiers):
        print("key_press: ", key)
        if key == arcade.key.P:
            self.__world.set_scale(self.__world.scale * 2)
        elif key == arcade.key.M:
            self.__world.set_scale(self.__world.scale / 2)
        elif key == arcade.key.Z:
            self.world_dy = -10
        elif key == arcade.key.S:
            self.world_dy = 10
        elif key == arcade.key.Q:
            self.world_dx = 10
        elif key == arcade.key.D:
            self.world_dx = -10

    def on_key_release(self, key: int, modifiers: int):
        super().on_key_release(key, modifiers)
        if key == arcade.key.Z or key == arcade.key.S:
            self.world_dy = 0
        elif key == arcade.key.Q or key == arcade.key.D:
            self.world_dx = 0
