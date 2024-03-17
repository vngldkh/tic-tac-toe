class Board:
    class Response:
        OK = 0
        FINISHED = 1
        INVALID_ARGUMENTS = 2
        TAKEN_CELL = 3

    def __init__(self):
        self.__board = [[-1 for _ in range(3)] for _ in range(3)]
        self.__turn = 0
        self.draw = False

    def get_player(self) -> int:
        return self.__turn % 2

    def make_turn(self, x: int, y: int) -> int:
        if x < 0 or x >= 3 or y < 0 or y >= 3:
            return Board.Response.INVALID_ARGUMENTS

        if self.__board[x][y] != -1:
            return Board.Response.TAKEN_CELL

        player = self.get_player()
        self.__board[x][y] = player
        if self.check(player):
            return Board.Response.FINISHED
        if self.check_draw():
            self.draw = True
            return Board.Response.FINISHED

        self.__turn += 1
        return Board.Response.OK

    def check(self, player) -> bool:
        major_diagonal = True
        minor_diagonal = True
        for i in range(3):
            horizontal = True
            vertical = True
            for j in range(3):
                horizontal &= self.__board[i][j] == player
                vertical &= self.__board[j][i] == player
                if not horizontal and not vertical:
                    break
            if horizontal or vertical:
                return True
            major_diagonal &= self.__board[i][i] == player
            minor_diagonal &= self.__board[i][2 - i] == player
            if not major_diagonal and not minor_diagonal:
                break
        if major_diagonal or minor_diagonal:
            return True
        return False

    def check_draw(self) -> bool:
        for i in range(3):
            for j in range(3):
                if self.__board[i][j] == -1:
                    return False
        return True

    def get_board(self) -> list[list[int]]:
        return self.__board
