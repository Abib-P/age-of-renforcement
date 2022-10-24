from src.entity.building.building import Building


class TownCenter(Building):
    default_sprites = {}

    def __init__(self, **kwargs):
        super(TownCenter, self).__init__(**kwargs)

    def __create_villager(self):
        # self._terrain.place_entity()
        pass

    def auto_play(self):
        self.__create_villager()


