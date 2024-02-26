import numpy as np
import itertools as it
from engine import TicTacToe
from alg_ai import find_best_move

class dataset:
    def __init__(self):
        ttts = self._ttts_creating()
        self.inputs = np.array([ttt.board.flatten() for ttt in ttts])
        self.inputs = np.random.permutation(self.inputs)
        self.outputs = self._output_creating(ttts)

    @staticmethod
    def _output_creating(ttts):
        outputs = np.array([])
        for ttt in ttts:
            cur_output = []
            for x in range(3):
                for y in range(3):
                    if (x, y) in ttt.valid_moves:
                        ttt.make_move((x,y))
                        res = -find_best_move(ttt)[0]
                        ttt.undo_move()
                    else:
                        res = -1
                    cur_output.append(res)
            outputs = outputs.append(outputs,dataset._normalization(cur_output))
        return outputs

    @staticmethod
    def _ttts_creating():
        boards = np.array(list(it.product([0,1,-1], repeat=9)))
        ttt_classes = np.array([dataset._reshape(board) for board in boards])
        not_finished = []
        for ttt in ttt_classes:
            if (not ttt.winned()[0]) and (not ttt.drow()):
                if (one := np.count_nonzero(ttt.board == 1)) == (minusone := np.count_nonzero(ttt.board == -1)) \
                        or one == minusone+1:
                    not_finished.append(ttt)
        return np.array(not_finished)

    @staticmethod
    def _reshape(board_to_reshape):
        return TicTacToe(board_to_reshape.reshape(3,3))

    @staticmethod
    def _normalization(lst):
        return [x if x == 1 else 0.5 if x == 0 else 0 for x in lst]
    """
    def _randomization(self):
        np.random.seed(1)
        self.inputs = np.random.permutation(self.inputs)
        np.random.seed(1)
        self.outputs = np.random.permutation(self.outputs)
    """
