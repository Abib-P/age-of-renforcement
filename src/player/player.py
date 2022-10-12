from src.entity.building.town_center import TownCenter
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

    def is_alive(self):
        for entity in self.__entities:
            if isinstance(entity, TownCenter):
                return True
        return False

    def __str__(self):
        return self.__name

    def __repr__(self):
        return self.__name

    def __eq__(self, other):
        return self.__name == other.__name

    def __hash__(self):
        return hash(self.__name)
