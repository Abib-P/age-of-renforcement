from __future__ import annotations
from math import sqrt


class Position:
    def __init__(self, x, y):
        self.__x = x
        self.__y = y

    def __eq__(self, o: object) -> bool:
        return self.__x == o.x and self.__y == o.y

    def dist(self, pos: Position) -> float:
        return sqrt(pow(abs(self.x - pos.x), 2) + pow(abs(self.y - pos.y), 2))

    @property
    def x(self):
        return self.__x

    @property
    def y(self):
        return self.__y
