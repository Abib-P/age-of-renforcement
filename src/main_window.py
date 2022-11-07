import arcade
import arcade.gui

from src.entity.entity import Entity
from src.entity.position import Position
from src.world import World


class MainWindow(arcade.Window):
    world: World
    world_dx: float
    world_dy: float

    __selected_entity: Entity | None

    def __init__(self, world: World):
        super().__init__(1280, 720, 'Age Of Renforcement')
        self.__selected_entity = None
        self.__world = world
        self.world_dy = 0
        self.world_dx = 0

        # Creating a UI MANAGER to handle the UI
        self.uimanager = arcade.gui.UIManager()
        self.uimanager.enable()

        # Create a vertical BoxGroup to align buttons
        self.v_box = arcade.gui.UIBoxLayout(align="left")

        quit_button = arcade.gui.UIFlatButton(text="Quit Game",
                                              width=200)

        quit_button.on_click = self.on_quit_button_click
        self.v_box.add(quit_button.with_space_around(bottom=20))

        # Creating Button using UIFlatButton
        reset_button = arcade.gui.UIFlatButton(text="Reset Game",
                                               width=200)
        reset_button.on_click = self.on_reset_button_click
        self.v_box.add(reset_button.with_space_around(bottom=20))

        self.score_label = arcade.gui.UILabel(text="test")
        self.v_box.add(self.score_label.with_space_around(bottom=20))

        self.exploration_label = arcade.gui.UILabel(text="test")
        self.v_box.add(self.exploration_label.with_space_around(bottom=20))

        # Adding button in our uimanager
        self.uimanager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="left",
                anchor_y="top",
                child=self.v_box)
        )

        self.__init_temp_panel()

    def __init_temp_panel(self):
        # Create a vertical BoxGroup to align buttons
        self.v_box = arcade.gui.UIBoxLayout(align="left")
        # Creating Button using UIFlatButton
        temp_button = arcade.gui.UIFlatButton(text="Temp",
                                              width=200)

        temp_button.on_click = self.on_temp_button_click
        self.v_box.add(temp_button.with_space_around(bottom=20))

        self.uimanager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="right",
                anchor_y="top",
                child=self.v_box)
        )

    def on_quit_button_click(self, event):
        self.close()

    def on_reset_button_click(self, event):
        self.__world.reset()

    def on_temp_button_click(self, event):
        self.__world.set_ai_exploration(1)

    def on_draw(self):
        arcade.start_render()
        self.__world.draw()
        if self.__selected_entity is not None:
            self.__selected_entity.draw_on_selection()

        # Drawing our ui manager
        self.uimanager.draw()

    def on_update(self, delta_time):
        self.exploration_label.text = "exploration: " + str(self.__world.get_ai_exploration())
        self.exploration_label.fit_content()

        self.score_label.text = "score: " + str(self.__world.get_ai_score())
        self.score_label.fit_content()

        self.__world.move_y(self.world_dy)
        self.__world.move_x(self.world_dx)
        if not self.__world.is_game_ended():
            self.__world.play_turn()
        else:
            self.__world.reset()
            print("reset")

    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            if self.__selected_entity is None:
                self.__selected_entity = self.__world.get_entity_on_clic(Position(x, y))
                if self.__selected_entity is not None:
                    self.__selected_entity.compute_possible_action()
            else:
                self.__world.action_entity(self.__selected_entity,
                                           self.__world.screen_position_to_terrain(Position(x, y)))
                self.__selected_entity = None
        elif button == arcade.MOUSE_BUTTON_RIGHT:
            self.__selected_entity = None

    def on_key_press(self, key, modifiers):
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
        elif key == arcade.key.ENTER:
            self.__selected_entity = None
            self.__world.player_end_turn()

    def on_key_release(self, key: int, modifiers: int):
        super().on_key_release(key, modifiers)
        if key == arcade.key.Z or key == arcade.key.S:
            self.world_dy = 0
        elif key == arcade.key.Q or key == arcade.key.D:
            self.world_dx = 0
