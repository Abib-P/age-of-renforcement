import json
import os
import pickle
from random import uniform, choice

from src.entity.building.town_center import TownCenter
from src.entity.neutral.resource import Resource
from src.entity.position import Position
from src.entity.unit.militia import Militia
from src.entity.unit.villager import Villager, VillagerOnActionRes
from src.player.player import Player


class VillagerAi:
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
    _step_history_scale: float

    def __init__(self, players: [Player], alpha: float, gamma: float, exploration: float = 0,
                 cooling_rate: float = 0.99):
        self.players = players
        self._qtable = {}
        self._score_history = []
        self._step_history_max = 1
        self._step_history_scale = 0.01
        self._possible_actions = ['L', 'R', 'U', 'D', 'O']
        self._exploration = exploration
        self.__cooling_rate = cooling_rate
        self._rewards = {VillagerOnActionRes.FORBIDDEN: -400,
                         VillagerOnActionRes.MOVE: -2,
                         VillagerOnActionRes.ATTACK_MILITIA: -1,
                         VillagerOnActionRes.KILL_MILITIA: 25,
                         VillagerOnActionRes.ATTACK_TOWN: -1,
                         VillagerOnActionRes.KILL_TOWN: 50,
                         VillagerOnActionRes.ATTACK_VILLAGER: -1,
                         VillagerOnActionRes.KILL_VILLAGER: 10,
                         VillagerOnActionRes.COLLECT_RESOURCE: 200, }

        self._score = 0
        self._nb_turn = 0
        self._alpha = alpha
        self._gamma = gamma

    def __get_enemy_player(self, villager: Villager) -> Player:
        return list(filter(lambda x: x != villager.player, self.players))[0]

    def __get_enemy_town_center_position(self, villager: Villager) -> Position | None:
        town = self.__get_enemy_player(villager).get_town_center()
        if town is None:
            return None
        return town.position

    def __get_ally_town_center_position(self, villager: Villager) -> Position:
        return villager.player.get_town_center().position

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

    def __get_nearset_enemy(self, villager: Villager) -> Militia | Villager | None:
        nearest = None
        enemy = self.__get_enemy_player(villager)
        enemy_militias = list(filter(lambda x: isinstance(x, Militia), enemy.entities))
        enemy_villager = list(filter(lambda x: isinstance(x, Villager), enemy.entities))
        if len(enemy_militias) == 0 and len(enemy_villager) == 0:
            return None
        if len(enemy_villager) != 0:
            nearest = enemy_villager.pop(0)
            for e in enemy_villager:
                if villager.position.dist(e.position) > villager.position.dist(nearest.position):
                    nearest = e
        if len(enemy_militias) != 0:
            nearest = enemy_militias.pop(0)
            for e in enemy_militias:
                if villager.position.dist(e.position) > villager.position.dist(nearest.position):
                    nearest = e
        return nearest

    def __get_town_center_enemy_direction(self, villager: Villager) -> str:
        enemy = self.__get_enemy_player(villager).get_town_center()
        if enemy is None:
            return 'O'
        return self.__get_direction(villager.position, enemy.position)

    def __get_nearset_enemy_direction(self, villager: Villager) -> str:
        enemy = self.__get_nearset_enemy(villager)
        if enemy is None:
            return 'O'
        return self.__get_direction(villager.position, enemy.position)

    def __is_nearest_town_center_ally(self, villager: Villager) -> bool:
        town_pos = self.__get_enemy_town_center_position(villager)
        if town_pos is None:
            return True
        return self.__get_ally_town_center_position(villager).dist(villager.position) < town_pos.dist(villager.position)

    def __get_element_at_position(self, villager: Villager, position: Position) -> str:
        if not villager.terrain.is_in_bound(position):
            return '#'
        if villager.terrain.is_cell_empty(position):
            return 'O'
        entity = villager.terrain.get_entity_at_position(position)
        if entity is None:
            raise Exception('Unknown entity')

        if isinstance(entity, Militia):
            if entity.player == villager.player:
                return 'A'
            else:
                return 'ME'
        if isinstance(entity, TownCenter):
            if entity.player == villager.player:
                return 'A'
            else:
                return 'TE'
        if isinstance(entity, Villager):
            if entity.player == villager.player:
                return 'A'
            else:
                return 'VE'
        if isinstance(entity, Resource):
            return 'R'
        raise Exception('Unknown entity')

    def __get_next_to_agent(self, villager: Villager) -> tuple[str, str, str, str]:
        return (self.__get_element_at_position(villager, Position(villager.position.x - 1, villager.position.y)),
                self.__get_element_at_position(villager, Position(villager.position.x + 1, villager.position.y)),
                self.__get_element_at_position(villager, Position(villager.position.x, villager.position.y + 1)),
                self.__get_element_at_position(villager, Position(villager.position.x, villager.position.y - 1)))

    def __get_direction_to_resource(self, villager: Villager) -> str:
        resource = villager.terrain.get_nearest_resource(villager.position)
        if resource is None:
            return 'O'
        return self.__get_direction(villager.position, resource.position)

    def __get_state(self, villager: Villager):
        direction_ally_town_center = self.__get_direction(villager.position,
                                                          self.__get_ally_town_center_position(villager))
        direction_nearest_enemy = self.__get_nearset_enemy_direction(villager)
        direction_to_nearest_resource = self.__get_direction_to_resource(villager)
        next_to_agent = self.__get_next_to_agent(villager)

        state = (direction_ally_town_center,
                 direction_nearest_enemy,
                 direction_to_nearest_resource,
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

    def chose_action(self, villager: Villager) -> Position | None:
        return self.__move_position(villager.position, self.__get_best_action(self.__get_state(villager)))

    def step(self, villager: Villager):
        current_state = self.__get_state(villager)
        current_state_action = self.__get_state_actions(current_state)
        max_reward = max(current_state_action.values())

        for previous_step in villager.step_history:
            previous_state_actions = self.__get_state_actions(previous_step[0])
            previous_state_actions[previous_step[1]] += self._alpha * (
                        previous_step[2] + self._gamma * max_reward - previous_state_actions[previous_step[1]])

        if len(villager.step_history) >= self._step_history_max:
            villager.step_history.pop(0)

        selected_action = self.__get_best_action(current_state)
        res = villager.on_action(self.chose_action(villager))
        reward = self._rewards[res]

        villager.step_history.append((current_state, selected_action, reward))

        self._score += reward
        self._nb_turn += 1

    def load(self, path: str):
        with open(path, 'rb') as file:
            self._qtable = pickle.load(file)

    def save(self, path: str):
        with open(path, 'wb') as file:
            pickle.dump(self._qtable, file)

    def save_histo(self, path: str):
        with open(path, 'a') as file:
            for h in self._score_history:
                file.write(str(h[0]) + " " + str(h[1]) + "\n")
        self._score_history = []

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

    @property
    def nb_turn(self):
        return self._nb_turn

    def reset(self):
        self._score_history.append((self._score, self._nb_turn))
        self._nb_turn = 0
        self._score = 0
        self._exploration = 0
