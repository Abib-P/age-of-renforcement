import arcade

from src.entity.entity import Entity
from src.entity.position import Position
from src.world import World


class MainWindow(arcade.Window):
    world: World
    world_dx: float
    world_dy: float

    __selected_entity: Entity | None

    def __init__(self, world: World):
        super().__init__(1280,
                         720,
                         'Age Of Renforcement')
        self.__selected_entity = None
        self.__world = world
        self.world_dy = 0
        self.world_dx = 0

    def setup(self):
        print("setup")

    def on_draw(self):
        arcade.start_render()
        self.__world.draw()
        if self.__selected_entity is not None:
            self.__selected_entity.draw_on_selection()

    def new_game(self):
        print("new game")

    def on_update(self, delta_time):
        self.__world.move_y(self.world_dy)
        self.__world.move_x(self.world_dx)
        if not self.__world.one_player_left():
            self.__world.play_turn()
        else:
            print("Game Over")

    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            if self.__selected_entity is None:
                self.__selected_entity = self.__world.get_entity_on_clic(Position(x, y))
            else:
                self.__world.move_entity(self.__selected_entity,
                                         self.__world.screen_position_to_terrain(Position(x, y)))
                self.__selected_entity = None
        elif button == arcade.MOUSE_BUTTON_RIGHT:
            self.__selected_entity = None

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
        elif key == arcade.key.ESCAPE:
            self.close()

    def on_key_release(self, key: int, modifiers: int):
        super().on_key_release(key, modifiers)
        if key == arcade.key.Z or key == arcade.key.S:
            self.world_dy = 0
        elif key == arcade.key.Q or key == arcade.key.D:
            self.world_dx = 0
