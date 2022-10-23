from src.entity.building.building import Building
from src.entity.player_entitiy import PlayerEntity


class TownCenter(Building, PlayerEntity):
    def __init__(self, **kwargs):
        super(TownCenter, self).__init__(**kwargs)

    def __create_villager(self):
        pass

    def auto_play(self):
        self.__create_villager()
