class AttackableEntity:
    _hp: int
    _max_hp: int

    def __init__(self, health_points: int, **kwargs):
        super(AttackableEntity, self).__init__(**kwargs)
        self._hp = health_points
        self._max_hp = health_points

    def is_alive(self):
        return self._hp > 0

    def take_damage(self, damage):
        self._hp -= damage
        if self._hp <= 0:
            self.__die()

    def __die(self):
        self._hp = 0
