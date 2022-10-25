from queue import Queue

import arcade

from src.entity.entity import Entity
from src.entity.position import Position
from src.terrain.terrain import Terrain


class MovableEntity(Entity):
    _terrain: Terrain
    __moving_points: int
    _possible_mov: [(Position, int)]

    def __init__(self, terrain: Terrain, moving_points: int, **kwargs):
        super(MovableEntity, self).__init__(**kwargs)
        self.__moving_points = moving_points
        self._terrain = terrain
        self._possible_move = []

    @property
    def terrain(self):
        return self._terrain

    @staticmethod
    def get_nb_move(start: Position, destination: Position, terrain: Terrain) -> int:
        # TODO take in consideration terrain
        return abs(start.x - destination.x) + abs(start.y - destination.y)

    def move(self, destination: Position) -> bool:
        if any(x[0] == destination for x in self._possible_move) \
                and self._terrain.move_entity(self, destination):
            self._position = destination
            self.compute_possible_action()
            self._possible_move = []
            return True
        return False

    def compute_possible_action(self):
        self._possible_move = []
        to_check = Queue()
        to_check.put((Position(self._position.x + 1, self._position.y), self.__moving_points))
        to_check.put((Position(self._position.x, self._position.y + 1), self.__moving_points))
        to_check.put((Position(self._position.x - 1, self._position.y), self.__moving_points))
        to_check.put((Position(self._position.x, self._position.y - 1), self.__moving_points))

        while not to_check.empty():
            pos = to_check.get()

            if not self._terrain.is_in_bound(pos[0]) or any(filter(lambda x: x[0] == pos[0], self._possible_move)):
                continue

            necessary_point_to_move = 1  # TODO check from terrain
            if self._terrain.is_cell_empty(pos[0]) and pos[1] >= necessary_point_to_move:
                self._possible_move.append(pos)
                to_check.put((Position(pos[0].x + 1, pos[0].y), pos[1] - necessary_point_to_move))
                to_check.put((Position(pos[0].x, pos[0].y + 1), pos[1] - necessary_point_to_move))
                to_check.put((Position(pos[0].x - 1, pos[0].y), pos[1] - necessary_point_to_move))
                to_check.put((Position(pos[0].x, pos[0].y - 1), pos[1] - necessary_point_to_move))

    def draw_on_selection(self):
        for pos in self._possible_move:
            start_x = (pos[0].x + 0.5) * self._scale + self._screen_offset.x
            start_y = (pos[0].y + 0.5) * self._scale + self._screen_offset.y
            size = self._scale

            arcade.draw_rectangle_filled(start_x, start_y,
                                         size, size,
                                         (0, 100, 255, 128))

        # arcade.draw_rectangle_outline((self._position.x + 0.5) * self.__scale + self.__screen_offset.x,
        #                               (self._position.y + 0.5) * self.__scale + self.__screen_offset.y,
        #                               15 * self.__scale / 10,
        #                               self.__scale / 2,
        #                               arcade.color.BLACK)
