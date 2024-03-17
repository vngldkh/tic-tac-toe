import threading

import flask
import jwt
from flask import Flask, json, request

from clean import clean_job
from common import lobbies
from lobby import Lobby


clean_thread = threading.Thread(target=clean_job)
clean_thread.start()
app = Flask(__name__)


@app.route('/lobbies/create', methods=['POST'])
def create():
    lobby = Lobby()
    lobbies[lobby.id] = lobby
    return {"lobby_id": lobby.id}


@app.route('/lobbies', methods=['GET'])
def get_lobbies():
    return json.dumps(list(lobbies.keys()))


@app.route('/lobbies/join/<lobby_id>', methods=['POST'])
def join(lobby_id: str):
    nickname = request.args['nickname']
    if nickname is None:
        return flask.Response(response='Nickname must not be empty', status=400)

    if lobby_id not in lobbies:
        return flask.Response(response='Lobby does not exist', status=404)

    lobby = lobbies[lobby_id]

    ret = lobby.add_player(nickname)
    if ret == Lobby.Response.ALREADY_EXISTS:
        return flask.Response(response='Player with the same name is already in the lobby', status=403)
    if ret == Lobby.Response.ALREADY_FULL:
        return flask.Response(response='Lobby is already full', status=403)

    encoded_jwt = jwt.encode(
        {
            "lobby_id": lobby_id,
            "nickname": nickname,
            "player_turn": len(lobby.players) - 1
        },
        "secret",
        algorithm="HS256"
    )
    return {"token": encoded_jwt}


@app.route('/get_board', methods=['GET'])
def get_board():
    token = request.args['token']
    if token is None:
        return flask.Response(status=400)

    try:
        jwt_decoded = jwt.decode(token, "secret", algorithms=["HS256"])
        lobby = lobbies[jwt_decoded["lobby_id"]]
        lobby.update_time(jwt_decoded["player_turn"])
        board = lobby.current_board
        if board is None:
            return flask.Response(
                response='Not started',
                status=400
            )
        return {"board": board.get_board(), "finished": lobby.finished}
    except:
        return flask.Response(status=404)


@app.route('/info', methods=["GET"])
def get_token_info():
    token = request.args['token']
    info = jwt.decode(token, "secret", algorithms=["HS256"])
    return info


@app.route('/score', methods=["GET"])
def get_score():
    token = request.args['token']
    info = jwt.decode(token, "secret", algorithms=["HS256"])
    lobby = lobbies[info["lobby_id"]]
    result: str | None = None
    match lobby.last_winner:
        case 0:
            result = f'Player {lobby.players[0]} won!'
        case 1:
            result = f'Player {lobby.players[1]} won!'
        case -1:
            result = f'Draw!'
        case _:
            result = None
    return {
        "score": lobby.score,
        "result": result
    }


@app.route('/turn', methods=["POST"])
def take_turn():
    x: int = int(request.args['x'])
    y: int = int(request.args['y'])
    token = request.args['token']
    if token is None or x is None or y is None:
        return flask.Response(status=400)

    data = None
    try:
        data = jwt.decode(token, "secret", algorithms=["HS256"])
        if data["lobby_id"] is None or data["player_turn"] is None or data["nickname"] is None:
            return flask.Response(status=400)
    except:
        return flask.Response(status=400)

    if data["lobby_id"] not in lobbies.keys():
        return flask.Response(status=404)

    lobby = lobbies[data["lobby_id"]]
    lobby.update_time(data["player_turn"])
    if not lobby.started():
        return flask.Response(
            response='Not started',
            status=400
        )
    if not lobby.check_player(data["player_turn"]):
        return flask.Response(
            response="Opponent's turn",
            status=403
        )
    if not lobby.validate(data["nickname"], data["player_turn"]):
        return flask.Response(
            response='Wrong token',
            status=400
        )

    ret = lobby.take_turn(x, y)
    match ret:
        case Lobby.Response.OK:
            return flask.Response(status=204)
        case Lobby.Response.INVALID_ARGUMENTS:
            return flask.Response(
                response='Invalid arguments',
                status=400
            )
        case Lobby.Response.TAKEN_CELL:
            return flask.Response(
                response='Cell already taken',
                status=400
            )
        case Lobby.Response.FINISHED:
            return flask.Response(
                response=json.dumps(lobby.score),
                status=200
            )


if __name__ == '__main__':
    pass
