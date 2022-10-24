from src.entity.attackable_entity import AttackableEntity
from src.entity.entity import Entity
from src.terrain.terrain import Terrain


class Building(AttackableEntity, Entity):
    def __init__(self, terrain: Terrain, **kwargs):
        super(Building, self).__init__(**kwargs)
        self._terrain = terrain
