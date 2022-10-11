from src.entity.Entity import Entity


class FightingEntity(Entity):
    def __init__(self, attack_points, **kwargs):
        self.attack_points = attack_points
        super(FightingEntity, self).__init__(**kwargs)
