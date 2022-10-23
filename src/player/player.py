from src.entity.entity import Entity


class Player:
    def __init__(self, name: str, color: str, entities: [Entity], is_human: bool = False):
        self.__name = name
        self.__color = color
        self.__is_human = is_human
        self.__entities = entities

    @property
    def name(self):
        return self.__name

    @property
    def color(self):
        return self.__color

    @property
    def is_human(self):
        return self.__is_human

    @property
    def entities(self):
        return self.__entities

    def is_alive(self) -> bool:
        import src.entity.building.town_center as town_center
        for entity in filter(lambda e: isinstance(e, town_center.TownCenter), self.__entities):
            if entity.is_alive():
                return True
        return False
