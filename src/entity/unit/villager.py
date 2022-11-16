from enum import Enum

from src.entity.entity import Entity
from src.entity.fighting_entity import FightingEntity
from src.entity.movable_entity import MovableEntity
from src.entity.neutral.resource import Resource
from src.entity.position import Position


class VillagerOnActionRes(Enum):
    FORBIDDEN = 0
    MOVE = 1
    ATTACK_MILITIA = 2
    KILL_MILITIA = 3
    ATTACK_TOWN = 4
    KILL_TOWN = 5
    ATTACK_VILLAGER = 6
    KILL_VILLAGER = 7
    COLLECT_RESOURCE = 8


class Villager(FightingEntity, MovableEntity):
    def __init__(self, **kwargs):
        super(Villager, self).__init__(**kwargs)
        self.state = ()
        self._step_history = []

    @property
    def step_history(self):
        return self._step_history

    def _get_return_on_action(self, entity: Entity):
        from src.entity.building.town_center import TownCenter
        from src.entity.unit.militia import Militia
        if isinstance(entity, TownCenter):
            if entity.is_alive():
                return VillagerOnActionRes.ATTACK_TOWN
            return VillagerOnActionRes.KILL_TOWN
        elif isinstance(entity, Militia):
            if entity.is_alive():
                return VillagerOnActionRes.ATTACK_MILITIA
            return VillagerOnActionRes.KILL_MILITIA
        elif isinstance(entity, Villager):
            if entity.is_alive():
                return VillagerOnActionRes.ATTACK_VILLAGER
            return VillagerOnActionRes.KILL_VILLAGER
        elif isinstance(entity, Resource):
            return VillagerOnActionRes.COLLECT_RESOURCE
        raise Exception('Unknown entity')

    def on_action(self, destination: Position):
        if destination.y == self.position.y and destination.x == self.position.x:
            return VillagerOnActionRes.MOVE

        entity = self._terrain.get_entity_at_position(destination)
        if entity is None:
            if self.move(destination):
                super().on_action(destination)
                return VillagerOnActionRes.MOVE
            return VillagerOnActionRes.FORBIDDEN
        elif isinstance(entity, Resource):
            self._terrain.collect_resource(entity)
            self._player.add_resource()
            return VillagerOnActionRes.COLLECT_RESOURCE
        elif entity.belongs_to(self._player):
            return VillagerOnActionRes.FORBIDDEN
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

    def _die(self):
        super()._die()
        self._terrain.remove_entity(self)
