from src.entity.fighting_entity import FightingEntity
from src.entity.movable_entity import MovableEntity
from src.entity.player_entitiy import PlayerEntity


class Villager(FightingEntity, MovableEntity, PlayerEntity):
    def __init__(self, name: int, health_points, position, moving_points, attack_points, unit_range):
        super(Villager, self).__init__(name=name, health_points=health_points, position=position,
                                       attack_points=attack_points, moving_points=moving_points, unit_range=unit_range)

    def move(self, map):
        pass
