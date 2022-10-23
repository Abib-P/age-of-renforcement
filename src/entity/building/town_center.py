from src.entity.building.building import Building


class TownCenter(Building):
    def __init__(self, **kwargs):
        super(TownCenter, self).__init__(**kwargs)

    def __create_villager(self):
        pass

    def play(self):
        self.__create_villager()
