from src.entity.position import Position
from src.player.player import Player


class PlayerEntity:
    _player: Player
    _has_played: bool

    def __init__(self, player: Player, **kwargs):
        super(PlayerEntity, self).__init__(**kwargs)
        self._player = player
        self._has_played = False

    def belongs_to(self, player: Player):
        return self._player == player

    def reset(self):
        self._has_played = False

    def on_action(self, position: Position):
        self._has_played = True

    @property
    def player(self) -> Player:
        return self._player
