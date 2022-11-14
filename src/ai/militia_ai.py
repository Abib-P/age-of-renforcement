import json
import os
import pickle
from random import uniform, choice

from src.entity.building.town_center import TownCenter
from src.entity.position import Position
from src.entity.unit.militia import Militia, MilitiaOnActionRes
from src.player.player import Player


class MilitiaAi:
    players: [Player]
    _qtable: {}
    _possible_actions: [str]
    _rewards: {}
    _alpha: float
    _gamma: float
    _exploration: float
    _score: float
    _score_history: []
    _nb_turn: int
    _step_history_max: int

    def __init__(self, players: [Player], alpha: float, gamma: float, exploration: float = 0,
                 cooling_rate: float = 0.99):
        self.players = players
        self._qtable = {}
        self._score_history = []
        self._step_history_max = 1
        self._possible_actions = ['L', 'R', 'U', 'D', 'O']
        self._exploration = exploration
        self.__cooling_rate = cooling_rate
        self._rewards = {MilitiaOnActionRes.FORBIDDEN: -400,
                         MilitiaOnActionRes.MOVE: -1,
                         MilitiaOnActionRes.ATTACK_MILITIA: -1,
                         MilitiaOnActionRes.KILL_MILITIA: 25,
                         MilitiaOnActionRes.ATTACK_TOWN: -1,
                         MilitiaOnActionRes.KILL_TOWN: 200}

        self._score = 0
        self._nb_turn = 0
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

    def __get_direction(self, src: Position, dst: Position) -> str:
        dx = dst.x - src.x
        dy = dst.y - src.y
        res = ''

        if abs(dx) > abs(dy):
            if dx > 0:
                res += 'R'
            else:
                res += 'L'
        else:
            if dy > 0:
                res += 'U'
            else:
                res += 'D'

        return res

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

    def __get_town_center_enemy_direction(self, militia: Militia) -> str:
        enemy = self.__get_enemy_player(militia).get_town_center()
        if enemy is None:
            return 'O'
        return self.__get_direction(militia.position, enemy.position)

    def __get_nearset_enemy_direction(self, militia: Militia) -> str:
        enemy = self.__get_nearset_enemy(militia)
        if enemy is None:
            return 'O'
        return self.__get_direction(militia.position, enemy.position)

    def __is_nearest_town_center_ally(self, militia: Militia) -> bool:
        town_pos = self.__get_enemy_town_center_position(militia)
        if town_pos is None:
            return True
        return self.__get_ally_town_center_position(militia).dist(militia.position) < town_pos.dist(militia.position)

    def __get_out_of_bound_state(self, militia: Militia) -> tuple[bool, bool, bool, bool]:
        return (militia.position.x == 0, militia.position.x == militia.terrain.width - 1,
                militia.position.y == 0, militia.position.y == militia.terrain.height - 1)

    def __get_element_at_position(self, militia: Militia, position: Position) -> str:
        if not militia.terrain.is_in_bound(position):
            return '#'
        if militia.terrain.is_cell_empty(position):
            return 'O'
        entity = militia.terrain.get_entity_at_position(position)
        if entity is None:
            raise Exception('Unknown entity')

        if isinstance(entity, Militia):
            if entity.player == militia.player:
                return 'A'
            else:
                return 'ME'
        if isinstance(entity, TownCenter):
            if entity.player == militia.player:
                return 'A'
            else:
                return 'TE'
        raise Exception('Unknown entity')

    def __get_next_to_agent(self, militia: Militia) -> tuple[str, str, str, str]:
        return (self.__get_element_at_position(militia, Position(militia.position.x - 1, militia.position.y)),
                self.__get_element_at_position(militia, Position(militia.position.x + 1, militia.position.y)),
                self.__get_element_at_position(militia, Position(militia.position.x, militia.position.y + 1)),
                self.__get_element_at_position(militia, Position(militia.position.x, militia.position.y - 1)))

    def __get_state(self, militia: Militia):
        direction_enemy_town_center = self.__get_town_center_enemy_direction(militia)
        direction_ally_town_center = self.__get_direction(militia.position,
                                                          self.__get_ally_town_center_position(militia))
        # is_nearest_town_center_ally = self.__is_nearest_town_center_ally(militia)
        direction_nearest_enemy = self.__get_nearset_enemy_direction(militia)
        # out_of_bound_state = self.__get_out_of_bound_state(militia)
        next_to_agent = self.__get_next_to_agent(militia)

        state = (direction_ally_town_center,
                 direction_nearest_enemy,
                 direction_enemy_town_center,
                 # is_nearest_town_center_ally,
                 #  out_of_bound_state,
                 next_to_agent)
        return state

    def __get_state_actions(self, state):
        if state not in self._qtable:
            self._qtable[state] = {}
            for act in self._possible_actions:
                self._qtable[state][act] = 0

        return self._qtable[state]

    def __get_best_action(self, state) -> str:
        if uniform(0, 1) < self._exploration:
            self._exploration *= self.__cooling_rate
            return choice(self._possible_actions)
        actions = self.__get_state_actions(state)
        return max(actions, key=actions.get)

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
        return self.__move_position(militia.position, self.__get_best_action(self.__get_state(militia)))

    def step(self, militia: Militia):
        current_state = self.__get_state(militia)
        current_state_action = self.__get_state_actions(current_state)
        max_reward = max(current_state_action.values())

        selected_action = self.__get_best_action(current_state)
        res = militia.on_action(self.chose_action(militia))
        reward = self._rewards[res]

        for previous_step in militia.step_history:
            previous_state_actions = self.__get_state_actions(previous_step[0])
            previous_state_actions[previous_step[1]] += self._alpha * (previous_step[2] + self._gamma * max_reward - previous_state_actions[previous_step[1]])

        if len(militia.step_history) >= self._step_history_max:
            militia.step_history.pop(0)
        militia.step_history.append((current_state, selected_action, reward))

        self._score += reward
        self._nb_turn += 1

    def load(self, path: str):
        with open(path, 'rb') as file:
            self._qtable = pickle.load(file)

    def save(self, path: str):
        with open("ai2_history.txt", 'a') as file:
            for h in self._score_history:
                file.write(str(h[0]) + " " + str(h[1]) + "\n")
        self._score_history = []
        with open(path, 'wb') as file:
            pickle.dump(self._qtable, file)

    def save_visible(self, path: str):
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

    @property
    def history(self):
        return self._score_history

    def reset(self):
        self._score_history.append((self._score, self._nb_turn))
        self._nb_turn = 0
        self._score = 0
        self._exploration = 0
