from src.player.player import Player


class PlayerEntity:
    _player: Player

    def __init__(self, player: Player, **kwargs):
        super(PlayerEntity, self).__init__(**kwargs)
        self._player = player
