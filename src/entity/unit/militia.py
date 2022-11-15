import random
from enum import Enum

from src.entity.entity import Entity
from src.entity.fighting_entity import FightingEntity
from src.entity.movable_entity import MovableEntity
from src.entity.position import Position


class MilitiaOnActionRes(Enum):
    FORBIDDEN = 0
    MOVE = 1
    ATTACK_MILITIA = 2
    KILL_MILITIA = 3
    ATTACK_TOWN = 4
    KILL_TOWN = 5


class Militia(FightingEntity, MovableEntity):
    state: ()
    _step_history: []

    def __init__(self, **kwargs):
        super(Militia, self).__init__(**kwargs)
        self.state = ()
        self._step_history = []

    @property
    def step_history(self):
        return self._step_history

    def _get_return_on_action(self, entity: Entity):
        from src.entity.building.town_center import TownCenter
        if isinstance(entity, TownCenter):
            if entity.is_alive():
                return MilitiaOnActionRes.ATTACK_TOWN
            return MilitiaOnActionRes.KILL_TOWN
        elif isinstance(entity, Militia):
            if entity.is_alive():
                return MilitiaOnActionRes.ATTACK_MILITIA
            return MilitiaOnActionRes.KILL_MILITIA
        raise Exception('Unknown entity')

    def on_action(self, destination: Position):
        if destination.y == self.position.y and destination.x == self.position.x:
            return MilitiaOnActionRes.MOVE

        entity = self._terrain.get_entity_at_position(destination)
        if entity is None:
            if self.move(destination):
                super().on_action(destination)
                return MilitiaOnActionRes.MOVE
            return MilitiaOnActionRes.FORBIDDEN
        elif entity.belongs_to(self._player):
            return MilitiaOnActionRes.FORBIDDEN
        elif self._position.dist(destination) <= self._unit_range:
            self.attack(entity)
            super().on_action(destination)
            return self._get_return_on_action(entity)
        else:
            best = sorted(self._possible_move, key=lambda x: x[0].dist(destination))
            if len(best) > 0 and self.move(best[0][0]) and self._position.dist(destination) <= self._unit_range:
                self.attack(entity)
                super().on_action(destination)
            return self._get_return_on_action(entity)

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
