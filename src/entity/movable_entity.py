from src.entity.entity import Entity
from src.entity.position import Position
from src.terrain.Terrain import Terrain


class MovableEntity(Entity):
    __terrain: Terrain
    __moving_points: int

    def __init__(self, terrain: Terrain, moving_points: int, **kwargs):
        self.__moving_points = moving_points
        self.__terrain = terrain
        super(MovableEntity, self).__init__(**kwargs)

    @staticmethod
    def get_nb_move(start: Position, destination: Position, terrain: Terrain) -> int:
        # TODO take in consideration terrain
        return abs(start.x - destination.x) + abs(start.y - destination.y)

    def move(self, destination: Position):
        necessary_moving_point = MovableEntity.get_nb_move(self._position, destination, self.__terrain)
        if necessary_moving_point <= self.__moving_points and self.__terrain.move_entity(self, destination):
            self._position = destination
