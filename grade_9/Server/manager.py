import sqlite3

DB = 'scores.db'


class Manager:
    def __init__(self):
        self.connection = sqlite3.connect('scores.db', check_same_thread=False)
        self.connection.execute('CREATE TABLE IF NOT EXISTS Scores('
                                 'player1 TEXT NOT NULL,'
                                 'score1 INT NOT NULL DEFAULT 0, '
                                 'player2 TEXT NOT NULL, '
                                 'score2 INT NOT NULL DEFAULT 0,'
                                 'PRIMARY KEY (player1, player2)'
                                 ')')

    def insert_score(self, player1: str, player2: str):
        try:
            self.connection.execute('INSERT INTO Scores (player1, player2) VALUES (?, ?)',
                                    (player1, player2))
            self.connection.commit()
        except:
            pass

    def get_score(self, player1: str, player2: str):
        ret: sqlite3.Cursor = self.connection.execute('SELECT * FROM Scores WHERE player1=? AND player2=?',
                                                      (player1, player2))
        obj = ret.fetchone()
        if obj is None:
            return None
        return [obj[1], obj[3]]

    def inc_score(self, player1: str, player2: str, winner: int) -> list[int]:
        score = self.get_score(player1, player2)
        score[winner] += 1
        self.connection.execute(f'UPDATE Scores SET score1 = ?, score2 = ? WHERE player1=? AND player2=?',
                                (score[0], score[1], player1, player2))
        self.connection.commit()

    def __del__(self):
        self.connection.close()


manager = Manager()
