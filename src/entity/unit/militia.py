from src.entity.fighting_entity import FightingEntity
from src.entity.movable_entity import MovableEntity


class Militia(FightingEntity, MovableEntity):
    def __init__(self, terrain, name, health_points, position, moving_points, attack_points, unit_range, sprite):
        super(Militia, self).__init__(name=name, health_points=health_points, position=position,
                                      terrain=terrain,
                                      unit_range=unit_range,
                                      sprite=sprite,
                                      attack_points=attack_points, moving_points=moving_points)
