from __future__ import annotations

import arcade

from src.entity.attackable_entity import AttackableEntity
from src.entity.entity import Entity
from src.entity.player_entitiy import PlayerEntity


class FightingEntity(AttackableEntity, PlayerEntity, Entity):
    _unit_range: int

    def __init__(self, attack_points: int, unit_range: int, **kwargs):
        super(FightingEntity, self).__init__(**kwargs)
        self.__attack_points = attack_points
        self._unit_range = unit_range

    def attack(self, attacked: FightingEntity):
        attacked.take_damage(self.__attack_points)

    def take_damage(self, damage):
        super().take_damage(damage)
        if not self.is_alive():
            self._player.remove_entity(self)

    def draw(self):
        super().draw()

        arcade.draw_rectangle_filled((self._position.x + 0.5) * self._scale + self._screen_offset.x,
                                     (self._position.y + 1) * self._scale + self._screen_offset.y,
                                     15 * (self._hp / self._max_hp) * self._scale / 10,
                                     self._scale / 2,
                                     arcade.color.GREEN)

        arcade.draw_rectangle_outline((self._position.x + 0.5) * self._scale + self._screen_offset.x,
                                      (self._position.y + 1) * self._scale + self._screen_offset.y,
                                      15 * self._scale / 10,
                                      self._scale / 2,
                                      arcade.color.BLACK)
