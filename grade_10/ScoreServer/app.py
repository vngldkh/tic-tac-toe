import json

import flask
from flask import Flask

from common import HOST, PORT
from manager import Manager

app = Flask(__name__)
manager = Manager()


@app.route('/score/<string:lobby_name>', methods=['GET', 'POST'])
def score(lobby_name: str):
    if flask.request.method == 'POST':
        manager.insert_score(lobby_name)
        return flask.Response(status=204)
    obj = manager.get_score(lobby_name)
    if obj is None:
        return flask.Response(status=404)
    return json.dumps(obj)


@app.route('/score/<string:lobby_name>/inc', methods=['POST'])
def increment_score(lobby_name: str):
    try:
        num = int(flask.request.args["num"])
    except ValueError:
        return flask.Response(status=400)
    if num is None and num != 0 and num != 1:
        return flask.Response(status=400)
    obj = manager.get_score(lobby_name)
    if obj is None:
        return flask.Response(status=404)
    manager.update_score(lobby_name, num, obj[num] + 1)
    return flask.Response(status=204)


if __name__ == '__main__':
    app.run(host=HOST, port=PORT)
