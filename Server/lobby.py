import string
import random
import threading
from datetime import datetime
from time import sleep

from board import Board


class Lobby:
    class Response:
        OK = 0
        FINISHED = 1
        ALREADY_EXISTS = 2
        ALREADY_FULL = 3
        TAKEN_CELL = 4
        INVALID_ARGUMENTS = 5

    def __init__(self):
        self.id: str = "".join(random.choices(string.ascii_letters + string.digits, k=5))
        self.players = []
        self.current_board = None
        self.score = [0, 0]
        self.last_request = []
        self.finished = False
        self.last_winner = None
        self.created_at = datetime.now()

    def add_player(self, player_name: str) -> int:
        if len(self.players) == 2:
            return Lobby.Response.ALREADY_FULL

        if player_name in self.players:
            return Lobby.Response.ALREADY_EXISTS

        self.players.append(player_name)
        self.last_request.append(datetime.now())

        if len(self.players) == 2:
            self.current_board = Board()

        return Lobby.Response.OK

    def update_time(self, player: int):
        self.last_request[player] = datetime.now()

    def started(self) -> bool:
        return self.current_board is not None

    def check_player(self, num: int) -> bool:
        return self.current_board.get_player() == num

    def validate(self, player: str, num: int) -> bool:
        return player in self.players and self.players.index(player) == num

    def start_new_board(self):
        sleep(15)
        self.current_board = Board()
        self.finished = False
        print(f'{self.id}: New round initiated')

    def take_turn(self, x: int, y: int) -> int:
        ret = self.current_board.make_turn(x, y)
        match ret:
            case Board.Response.OK:
                return Lobby.Response.OK
            case Board.Response.FINISHED:
                threading.Thread(target=self.start_new_board).start()
                self.score[self.current_board.get_player()] += 1
                self.finished = True
                self.last_winner = self.current_board.get_player()
                return Lobby.Response.FINISHED
            case Board.Response.TAKEN_CELL:
                return Lobby.Response.TAKEN_CELL
            case Board.Response.INVALID_ARGUMENTS:
                return Lobby.Response.INVALID_ARGUMENTS
