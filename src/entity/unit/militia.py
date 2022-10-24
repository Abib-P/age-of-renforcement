from src.entity.fighting_entity import FightingEntity
from src.entity.movable_entity import MovableEntity
from src.entity.position import Position


class Militia(FightingEntity, MovableEntity):
    def __init__(self, **kwargs):
        super(Militia, self).__init__(**kwargs)

    def move(self, destination: Position):
        entity = self._terrain.get_entity(destination)
        if entity is None:
            super().move(destination)
        elif self._position.dist(destination) <= self._unit_range:
            self.attack(entity)
        else:
            best = sorted(self._possible_move, key=lambda x: x[0].dist(destination))
            if len(best) > 0:
                super().move(best[0][0])
                self.attack(entity)

    def auto_play(self):
        pass
        # raise NotImplementedError
