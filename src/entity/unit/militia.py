from src.entity.fighting_entity import FightingEntity
from src.entity.movable_entity import MovableEntity


class Milita(FightingEntity, MovableEntity):
    def __init__(self, name, health_points, position, moving_points, attack_points, unit_range):
        super(Milita, self).__init__(name=name, health_points=health_points, position=position,
                                     attack_points=attack_points, moving_points=moving_points)
