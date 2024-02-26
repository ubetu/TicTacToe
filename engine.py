import numpy as np
class TicTacToe:
    def __init__(self, board=np.array([[0,0,0],[0,0,0],[0,0,0]]), turn=None):
        if turn is None:
            turn = 1 if np.count_nonzero(board == 1) == np.count_nonzero(board == -1) else -1

        self.board = board
        self.turn = turn
        self.valid_moves = [(x,y) for x, col in enumerate(self.board)\
                            for y, square in enumerate(col) if not square]
        self.move_log = []
        self.symb_meaning = {1: 'x', 0: '_', -1: '0'}

    def make_move(self, move):
        self.move_log.append(move)
        self.board[move[0]][move[1]] = self.turn
        self.turn = -self.turn
        self.valid_moves.remove(move)

    def undo_move(self):
        if len(self.move_log) > 0:
            self.board[self.move_log[-1][0]][self.move_log[-1][1]] = 0
            self.valid_moves.append(self.move_log.pop())
            self.turn = -self.turn
    """
    def get_valid_moves(self):
        moves = [(x,y) for x, col in enumerate(self.board) for y, square in enumerate(col) if not square]
        return moves
    """
    def _row_win(self):
        for row in range(3):
            if self.board[row][0] == self.board[row][1] == self.board[row][2] != 0:
                return self.board[row][0], row, 'row'
        return 0, 0, 0

    def _col_win(self):
        for col in range(3):
            if self.board[0][col] == self.board[1][col] == self.board[2][col] != 0:
                return self.board[0][col], col, 'col'
        return 0, 0, 0

    def _diagonal_win(self):
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != 0:
            return self.board[0][0], 1, 'diagonal'
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != 0:
            return self.board[2][0], 2, 'diagonal'
        return 0, 0, 0

    def drow(self):
        return self.valid_moves == []

    def winned(self):
        if (col := self._col_win())[0]:
            return col
        elif (row := self._row_win())[0]:
            return row
        elif (dg := self._diagonal_win())[0]:
            return dg
        return 0, 0, 0

    """
    def reshape(self, board_to_reshape):
        if np.count_nonzero(board_to_reshape==1) == np.count_nonzero(board_to_reshape==-1):
            turn = 1
        else:
            turn = -1
        return TicTacToe(board_to_reshape.reshape(3,3), turn)
    def all_ttts(self):
        boards = np.array(list(it.product([0,1,-1], repeat=9)))
        ttt_classes = np.array([self.reshape(board) for board in boards])
        not_finished = []
        for ttt in ttt_classes:
            if (not ttt.winned()[0]) and (not ttt.drow()):
                if (one:=np.count_nonzero(ttt.board==1)) == (minusone:=np.count_nonzero(ttt.board==-1)) or one==minusone+1:
                    not_finished.append(ttt)

        return np.array(not_finished)
    """
    def print_board(self):
        for row in self.board:
            for el in x:
                print(self.symb_meaning[el], end=' ')
            print()
