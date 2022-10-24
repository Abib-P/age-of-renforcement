import random

from src.entity.fighting_entity import FightingEntity
from src.entity.movable_entity import MovableEntity
from src.entity.position import Position


class Militia(FightingEntity, MovableEntity):
    def __init__(self, **kwargs):
        super(Militia, self).__init__(**kwargs)

    def on_action(self, destination: Position):
        if self._has_played:
            return
        super().on_action(destination)
        entity = self._terrain.get_entity(destination)

        if entity is None:
            super().move(destination)
        elif entity.belongs_to(self._player):
            pass
        elif self._position.dist(destination) <= self._unit_range:
            self.attack(entity)
        else:
            best = sorted(self._possible_move, key=lambda x: x[0].dist(destination))
            if len(best) > 0 and super().move(best[0][0]):
                self.attack(entity)

    def compute_possible_action(self):
        if not self._has_played:
            super().compute_possible_action()

    def _die(self):
        super()._die()
        self._terrain.remove_entity(self)

    def auto_play(self):
        self.compute_possible_action()
        if len(self._possible_move) > 0:
            action = random.choice(self._possible_move)
            self.move(action[0])
