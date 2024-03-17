import requests

from common import URL


def select_lobby() -> str | None:
    # Print out list of lobbies
    r = requests.get(f'{URL}/lobbies')
    lobbies: list = r.json()
    print(lobbies)

    # Enter desired lobby
    print('Write the name of the lobby or "quit" to return to main menu')
    while True:
        selected_lobby = input('>>> ')
        if selected_lobby == 'quit':
            return None
        if selected_lobby not in lobbies:
            print('Do not exists')
            continue
        return selected_lobby


def join_lobby(selected_lobby: str) -> str | None:
    # Enter nickname
    print('Enter nickname or "quit" to return to main menu')
    nickname = input('>>> ')
    if nickname == 'quit':
        return None

    # Join lobby
    r = requests.post(f'{URL}/lobbies/join/{selected_lobby}', params={"nickname": nickname})
    if r.status_code != 200:
        print(r.content.decode())
        return None
    return r.json()["token"]
