class Position:
    def __init__(self, x, y):
        self.__x = x
        self.__y = y

    def __eq__(self, o: object) -> bool:
        return self.__x == o.x and self.__y == o.y

    @property
    def x(self):
        return self.__x

    @property
    def y(self):
        return self.__y
