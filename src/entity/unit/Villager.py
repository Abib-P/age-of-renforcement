from src.entity.FightingEntity import FightingEntity
from src.entity.MovableEntity import MovableEntity


class Villager(FightingEntity, MovableEntity):
    def __init__(self, name, health_points, position, moving_points, attack_points):
        super(Villager, self).__init__(name=name, health_points=health_points, position=position, attack_points=attack_points, moving_points=moving_points)
        # MovableEntity.__init__(self, name=name, health_points=health_points, position=position, moving_points=moving_points)
        # super(MovableEntity).__init__(name=name, health_points=health_points, position=position, moving_points=moving_points)

    def move(self, map):
        pass

    def __str__(self):
        return "Villager"
