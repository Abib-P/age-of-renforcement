from src.entity.attackable_entity import AttackableEntity
from src.entity.entity import Entity
from src.entity.player_entitiy import PlayerEntity
from src.entity.position import Position
from src.terrain.terrain import Terrain


class Building(AttackableEntity, PlayerEntity, Entity):
    _terrain: Terrain

    def __init__(self, terrain: Terrain, **kwargs):
        super(Building, self).__init__(**kwargs)
        self._terrain = terrain

    def draw(self):
        super().draw()
        self.draw_ui(Position((self._position.x + 0.5) * self._scale + self._screen_offset.x,
                              (self._position.y + 1) * self._scale + self._screen_offset.y, ),
                     self._scale,
                     self.player.color)

    def _die(self):
        super()._die()
        self._player.remove_entity(self)
        self._terrain.remove_entity(self)



