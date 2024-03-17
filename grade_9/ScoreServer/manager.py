import sqlite3

DB = 'scores.db'


class Manager:
    def __init__(self):
        self.connection = sqlite3.connect('scores.db', check_same_thread=False)
        self.connection.execute('CREATE TABLE IF NOT EXISTS Scores('
                                 'id INTEGER PRIMARY KEY AUTOINCREMENT, '
                                 'lobby TEXT NOT NULL, '
                                 'player1 INT DEFAULT 0,'
                                 'player2 INT DEFAULT 0'
                                 ')')

    def insert_score(self, lobby: str):
        self.connection.execute('INSERT INTO Scores (lobby) VALUES (?)', (lobby,))
        self.connection.commit()

    def get_score(self, lobby: str):
        ret: sqlite3.Cursor = self.connection.execute('SELECT * FROM Scores WHERE lobby=?', (lobby,))
        obj = ret.fetchone()
        if obj is None:
            return None
        return [obj[2], obj[3]]

    def update_score(self, lobby: str, player: int, score: int) -> None:
        self.connection.execute(f'UPDATE Scores SET player{player + 1}=? WHERE lobby=?', (score, lobby))

    def __del__(self):
        self.connection.close()
