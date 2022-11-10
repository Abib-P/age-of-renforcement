import json
import os
import pickle
from random import uniform, choice, randrange

from src.entity.building.town_center import TownCenter
from src.entity.position import Position
from src.entity.unit.militia import Militia, MilitiaOnActionRes
from src.player.player import Player

import numpy as np
from sklearn.neural_network import MLPRegressor


class MilitiaAi:
    players: [Player]
    _qtable: {}
    _possible_actions: [str]
    _rewards: {}
    _alpha: float
    _gamma: float
    _exploration: float
    _score: float

    def __init__(self, players: [Player], alpha: float, gamma: float, exploration: float = 0,
                 cooling_rate: float = 0.99):
        self.players = players
        self._qtable = {}
        self._possible_actions = ['R', 'L', 'U', 'D', 'O']
        self._exploration = exploration
        self.__cooling_rate = cooling_rate
        self._rewards = {MilitiaOnActionRes.FORBIDDEN: -100000,
                         MilitiaOnActionRes.MOVE: -1,
                         MilitiaOnActionRes.ATTACK_MILITIA: 100,
                         MilitiaOnActionRes.KILL_MILITIA: 200,
                         MilitiaOnActionRes.ATTACK_TOWN: 300,
                         # peut etre a changer car meurt souvant en attaquant la base enemy
                         MilitiaOnActionRes.KILL_TOWN: 400}

        # Initialisation du réseau de neurones
        # Ici : 1 couche cachée de 2000 neurones
        self.__mlp = MLPRegressor(hidden_layer_sizes=(2000, 1000),
                                  activation='tanh',
                                  solver='sgd',
                                  learning_rate_init=alpha,
                                  max_iter=1,
                                  warm_start=True)
        self.__mlp.fit([[0, 0, 0, 0, 0, 0, 0, 0]], [[0] * len(self._possible_actions)])

        self._score = 0
        self._alpha = alpha
        self._gamma = gamma

    def __get_enemy_player(self, militia: Militia) -> Player:
        return list(filter(lambda x: x != militia.player, self.players))[0]

    def __get_enemy_town_center_position(self, militia: Militia) -> Position | None:
        town = self.__get_enemy_player(militia).get_town_center()
        if town is None:
            return None
        return town.position

    def __get_ally_town_center_position(self, militia: Militia) -> Position:
        return militia.player.get_town_center().position

    def __get_direction(self, src: Position, dst: Position) -> (int, int):
        dx = dst.x - src.x
        dy = dst.y - src.y

        return dx, dy

    def __get_nearset_enemy(self, militia: Militia) -> Militia | None:
        enemy = self.__get_enemy_player(militia)
        enemy_militias = list(filter(lambda x: isinstance(x, Militia), enemy.entities))
        if len(enemy_militias) == 0:
            return None
        nearest = enemy_militias.pop(0)
        for e in enemy_militias:
            if militia.position.dist(e.position) > militia.position.dist(nearest.position):
                nearest = e
        return nearest

    def __get_relative_position(self, militia: Militia) -> (float, float):
        dx = militia.position.x / (militia.terrain.width - 1)
        dy = militia.position.y / (militia.terrain.height - 1)
        return dx, dy

    def __get_town_center_ally_direction(self, militia: Militia) -> (float, float):
        position = self.__get_ally_town_center_position(militia)
        dx = (militia.position.x - position.x ) / militia.terrain.width / 2 + 0.5
        dy = (militia.position.y - position.y ) / militia.terrain.height / 2 + 0.5
        return dx, dy

    def __get_town_center_enemy_direction(self, militia: Militia) -> (float, float):
        enemy = self.__get_enemy_player(militia).get_town_center()
        if enemy is None:
            return 0.5, 0.5
        dx = (militia.position.x - enemy.position.x ) / militia.terrain.width / 2 + 0.5
        dy = (militia.position.y - enemy.position.y ) / militia.terrain.height / 2 + 0.5
        return dx, dy

    def __get_nearset_enemy_direction(self, militia: Militia) -> (float, float):
        enemy = self.__get_nearset_enemy(militia)
        if enemy is None:
            return 0.5, 0.5
        dx = (militia.position.x - enemy.position.x) / militia.terrain.width / 2 + 0.5
        dy = (militia.position.y - enemy.position.y) / militia.terrain.height / 2 + 0.5
        return dx, dy

    def __get_state(self, militia: Militia) -> [int]:
        direction_enemy_town_center = self.__get_town_center_enemy_direction(militia)
        direction_ally_town_center = self.__get_town_center_ally_direction(militia)
        direction_nearest_enemy = self.__get_nearset_enemy_direction(militia)
        relative_position = self.__get_relative_position(militia)

        state = (relative_position[0], relative_position[1],
                 direction_ally_town_center[0], direction_ally_town_center[1],
                 direction_enemy_town_center[0], direction_enemy_town_center[1],
                 direction_nearest_enemy[0], direction_nearest_enemy[1],
                 )
        return state

    def __get_best_action(self, state):
        if uniform(0, 1) < self._exploration:
            self._exploration *= self.__cooling_rate
            return randrange(len(self._possible_actions))

        qvector = self.__mlp.predict([state])[0]
        return np.argmax(qvector)

    def __move_position(self, src: Position, direction: str) -> Position:
        match direction:
            case 'R':
                return Position(src.x + 1, src.y)
            case 'L':
                return Position(src.x - 1, src.y)
            case 'U':
                return Position(src.x, src.y + 1)
            case 'D':
                return Position(src.x, src.y - 1)
            case 'O':
                return Position(src.x, src.y)

    def chose_action(self, militia: Militia) -> Position | None:
        return self.__move_position(militia.position,
                                    self._possible_actions[self.__get_best_action(self.__get_state(militia))])

    def step(self, militia: Militia):
        old_state = self.__get_state(militia)

        action_index = self.__get_best_action(old_state)
        res = militia.on_action(self.__move_position(militia.position,
                                                     self._possible_actions[action_index]))
        reward = self._rewards[res]
        self._score += reward

        new_state = self.__get_state(militia)
        max_q = max(self.__mlp.predict([new_state])[0])

        qvector = self.__mlp.predict([old_state])[0]
        reward = reward * self._alpha + max_q * self._gamma
        qvector[action_index] = reward
        self.__mlp.fit([old_state], [qvector])

    def load(self, path: str):
        with open(path, 'rb') as file:
            self.__mlp = pickle.load(file)

    def save(self, path: str):
        with open(path, 'wb') as file:
            pickle.dump(self.__mlp, file)

    def save_visible(self, path: str):
        return
        with open(path, 'w') as file:
            for key, value in self._qtable.items():
                file.write(json.dumps(key) + " : " + json.dumps(value) + "\n")

    def file_exists(self, path: str) -> bool:
        return os.path.isfile(path)

    @property
    def exploration(self):
        return self._exploration

    @exploration.setter
    def exploration(self, value):
        self._exploration = value

    @property
    def score(self):
        return self._score

    def reset(self):
        self._score = 0
