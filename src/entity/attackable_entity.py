import arcade

from src.entity.position import Position


class AttackableEntity:
    _hp: int
    _max_hp: int

    def __init__(self, health_points: int, **kwargs):
        super(AttackableEntity, self).__init__(**kwargs)
        self._hp = health_points
        self._max_hp = health_points

    def is_alive(self):
        return self._hp > 0

    def take_damage(self, damage):
        self._hp -= damage
        if self._hp <= 0:
            self._die()

    def _die(self):
        self._hp = 0

    def draw_ui(self, position: Position, scale: float, color: arcade.color):
        arcade.draw_rectangle_filled(position.x,
                                     position.y,
                                     15 * (self._hp / self._max_hp) * scale / 10,
                                     scale / 2,
                                     color)

        arcade.draw_rectangle_outline(position.x,
                                      position.y,
                                      15 * scale / 10,
                                      scale / 2,
                                      arcade.color.BLACK)
