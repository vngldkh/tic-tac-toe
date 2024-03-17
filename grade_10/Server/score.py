import requests

HOST = 'localhost'
PORT = 8080


def init_score(lobby: str):
    requests.post(f'http://{HOST}:{PORT}/score/{lobby}')


def get_score(lobby: str) -> list[int] | None:
    r = requests.get(f'http://{HOST}:{PORT}/score/{lobby}')
    if r.status_code != 200:
        return None
    return r.json()