from src.entity.fighting_entity import FightingEntity
from src.entity.movable_entity import MovableEntity


class Militia(FightingEntity, MovableEntity):
    def __init__(self, **kwargs):
        super(Militia, self).__init__(**kwargs)

    def auto_play(self):
        pass
        # raise NotImplementedError
