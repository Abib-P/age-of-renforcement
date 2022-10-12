from src.entity.entity import Entity


class FightingEntity(Entity):
    def __init__(self, attack_points: int, unit_range: int, **kwargs):
        self.__attack_points = attack_points
        self.__unit_range = unit_range
        super(FightingEntity, self).__init__(**kwargs)

    def attack(self, attacked: Entity):
        attacked.take_damage(self.__attack_points)
