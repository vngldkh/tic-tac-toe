from datetime import datetime
from time import sleep

from common import lobbies


def clean_lobbies():
    to_del = []
    for lobby in lobbies.values():
        last_request = lobby.last_request
        match len(last_request):
            case 0:
                diff = datetime.now() - lobby.created_at
                if diff.total_seconds() > 30:
                    to_del.append(lobby.id)
            case 1:
                diff = datetime.now() - last_request[0]
                if diff.total_seconds() > 30:
                    to_del.append(lobby.id)
            case 2:
                diff1 = (datetime.now() - last_request[0]).seconds
                diff2 = (datetime.now() - last_request[1]).seconds
                if diff1 > 30 or diff2 > 30:
                    to_del.append(lobby.id)
    for lobby in to_del:
        print(f"CLEAR LOBBY {lobby}")
        lobbies.pop(lobby)


def clean_job():
    while True:
        clean_lobbies()
        sleep(5)