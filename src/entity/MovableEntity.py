from src.entity.Entity import Entity


class MovableEntity(Entity):
    def __init__(self, moving_points, **kwargs):
        self.moving_points = moving_points
        super(MovableEntity, self).__init__(**kwargs)

    def move(self, map):
        pass
        # TODO: Implement
