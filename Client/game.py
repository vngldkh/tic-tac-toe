from time import sleep

import requests

from common import URL


class Game:
    class Response:
        OK = 0
        NOT_STARTED = 1
        DISCONNECTED = 2
        NO_UPDATES = 3

    def __init__(self, token):
        self.board: list | None = None
        self.token = token
        self.finished = False

    def check_update(self, check_finished: bool) -> Response.OK | Response.DISCONNECTED | Response.NO_UPDATES:
        # print("Checking for updates...")
        r = requests.get(f'{URL}/get_board', params={'token': self.token})
        if r.status_code == 404:
            return Game.Response.DISCONNECTED
        if r.status_code == 400:
            return Game.Response.NOT_STARTED
        if check_finished and r.json()["finished"]:
            return Game.Response.NOT_STARTED

        other = r.json()["board"]
        if self.board is None or not self.board.__eq__(other):
            self.board = other
            self.finished = r.json()["finished"]
            return Game.Response.OK
        return Game.Response.NO_UPDATES

    def wait_for_update(self, check_finished: bool = False) -> Response.OK | Response.DISCONNECTED:
        res = None
        while res != Game.Response.OK:
            res = self.check_update(check_finished=check_finished)
            if res == Game.Response.DISCONNECTED:
                return Game.Response.DISCONNECTED
            sleep(1)
        return res

    def display_board(self) -> None:
        if self.board is None:
            return
        for i in range(3):
            s = ' '
            line = self.board[i]
            for j in range(3):
                e = line[j]
                match e:
                    case 0:
                        s += '✕'
                    case 1:
                        s += '◯'
                    case -1:
                        s += ' '
                s += ' '
                if j < 2:
                    s += '| '
            print(s)
            if i < 2:
                print('---|---|---')

    def play(self) -> Response.OK | Response.DISCONNECTED:
        print('Waiting for the game to start...')
        ret = self.wait_for_update(check_finished=True)
        if ret == Game.Response.DISCONNECTED:
            print('Disconnected')
            return Game.Response.DISCONNECTED

        print('Game started!')
        self.display_board()

        r = requests.get(f'{URL}/info', params={'token': self.token})
        if r.status_code != 200:
            print('Unexpected error')
            return
        turn = r.json()['player_turn']

        if turn == 1:
            print('Waiting for opponent\'s turn...')
            res = self.wait_for_update()
            if res == Game.Response.DISCONNECTED:
                print('Disconnected')
                return Game.Response.DISCONNECTED
            self.display_board()
        finished: bool = False
        while not finished:
            try:
                print('Enter No of row')
                x = int(input('>>> '))
                x -= 1

                print('Enter No of column')
                y = int(input('>>> '))
                y -= 1
            except ValueError:
                print('Invalid input!')
                continue

            r = requests.post(f'{URL}/turn', params={'token': self.token, 'x': x, 'y': y})
            if r.status_code == 404:
                print('Disconnected')
                return Game.Response.DISCONNECTED

            if r.status_code > 204:
                print(r.content.decode())
                continue

            self.board[x][y] = turn
            self.display_board()
            finished = r.status_code == 200
            if finished:
                self.finished = True
                continue

            print('Waiting for opponent\'s turn...')
            res = self.wait_for_update()
            if res == Game.Response.DISCONNECTED:
                print('Disconnected')
                return Game.Response.DISCONNECTED
            self.display_board()

            finished = self.finished

        r = requests.get(f'{URL}/score', params={'token': self.token})
        print('Game finished!')
        print(f'Player {r.json()['last_winner']} won!')
        print(f'Total score: {r.json()["score"]}')
        return Game.Response.OK
