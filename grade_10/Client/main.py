import requests

from common import URL
from game import Game
from lobby import join_lobby, select_lobby


if __name__ == '__main__':
    to_quit: bool = False
    while not to_quit:
        print('Welcome to Tick-Tac-Toe game!')
        print('Choose an action:')
        print('1. Create lobby')
        print('2. Join lobby')
        print('3. Quit')

        invalid_input: bool = True
        return_to_menu: bool = False
        token = None
        while invalid_input and not return_to_menu:
            try:
                x = int(input('>>> '))
            except ValueError:
                print('Invalid input')
                continue
            match x:
                case 1:
                    r = requests.post(f'{URL}/lobbies/create')
                    if r.status_code == 403:
                        print('Server is not active')
                        continue
                    lobby_id: str = r.json()["lobby_id"]
                    print(f'Lobby "{lobby_id}" created successfully')
                    token = join_lobby(lobby_id)
                    if token is None:
                        return_to_menu = True
                        continue
                    invalid_input = False
                case 2:
                    lobby = select_lobby()
                    if lobby is None:
                        return_to_menu = True
                        continue
                    token = join_lobby(lobby)
                    if token is None:
                        return_to_menu = True
                        continue
                    invalid_input = False
                case 3:
                    to_quit = True
                    invalid_input = False
                case _:
                    print('Invalid input')
        if to_quit or return_to_menu:
            continue

        quit_match: bool = False
        while not quit_match:
            game = Game(token)
            ret = game.play()

            if ret == Game.Response.DISCONNECTED:
                quit_match = True
                continue

            print('Write "quit" to quit or anything else to play another round')
            inp = input('>>> ')
            if inp == 'quit':
                quit_match = True
