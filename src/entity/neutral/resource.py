from src.entity.entity import Entity


class Resource(Entity):
    def __init__(self, terrain, **kwargs):
        super(Resource, self).__init__(**kwargs)
        self.__terrain = terrain

    def is_alive(self):
        return True
