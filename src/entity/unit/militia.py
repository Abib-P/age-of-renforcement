from src.entity.fighting_entity import FightingEntity
from src.entity.movable_entity import MovableEntity
from src.entity.player_entitiy import PlayerEntity


class Militia(FightingEntity, MovableEntity, PlayerEntity):
    def __init__(self, **kwargs):
        super(Militia, self).__init__(**kwargs)

    def auto_play(self):
        pass
        # raise NotImplementedError
