import numpy as np
import alg_ai
from neuro import model
from engine import TicTacToe
def game():
    ttt = TicTacToe(np.array([[0,0,0],[0,0,0],[0,0,0]]), 1)
    res = None
    while True:
        if ttt.turn == -1:
            move = model.best_move(ttt)[1]
        else:
            move = alg_ai.find_best_move(ttt)[1]
        ttt.make_move(move)

        win_tuple = ttt.winned()
        if win_tuple[0]:
            res = win_tuple[0]
            break
        if ttt.drow():
            res = 0
            break
    return res
wins = 0
draws = 0
loses = 0
for i in range(10):
    res = game()
    match res:
        case 1:
            wins += 1
        case -1:
            loses += 1
        case 0:
            draws += 1
    print(res)
print('wins:', wins)
print('loses:', loses)
print('draws:', draws)
