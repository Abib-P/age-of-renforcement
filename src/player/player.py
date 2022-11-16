import arcade

from src.entity.entity import Entity


class Player:
    __entities: [Entity]

    def __init__(self, name: str, color: arcade.Color, is_human: bool = False):
        self.__resources_count = 0
        self.__name = name
        self.__color = color
        self.__is_human = is_human
        self.__entities = []

    def add_entity(self, entity: Entity):
        self.__entities.append(entity)

    def remove_entity(self, entity: Entity):
        self.__entities.remove(entity)

    def __eq__(self, o: object) -> bool:
        return isinstance(o, Player) and self.__name == o.__name

    def add_resource(self):
        self.__resources_count += 1

    def play_turn(self):
        if self.__resources_count > 0:
            self.get_town_center().create_militia()
            self.__resources_count -= 1

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

    def end_turn(self):
        from src.entity.player_entitiy import PlayerEntity
        for entity in filter(lambda e: isinstance(e, PlayerEntity), self.__entities):
            entity.reset()

    def is_alive(self) -> bool:
        import src.entity.building.town_center as town_center
        for entity in filter(lambda e: isinstance(e, town_center.TownCenter), self.__entities):
            if entity.is_alive():
                return True
        return False

    def get_town_center(self) -> Entity | None:
        import src.entity.building.town_center as town_center
        for entity in filter(lambda e: isinstance(e, town_center.TownCenter), self.__entities):
            return entity
        return None
