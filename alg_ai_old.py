import random

cache = {}
def find_best_move(ttt):
    global cache
    random.shuffle(ttt.valid_moves)
    score, best_move = find_move(ttt, ttt.turn)
    return score, best_move


def find_move(ttt, turn):
    global cache
    board_tuple = tuple(item for row in ttt.board for item in row)
    if board_tuple in cache:
        return cache[board_tuple]

    if win := ttt.winned()[0]:
        return turn*win, ()

    if ttt.drow():
        return 0, ()

    best_move = ()
    max_score = -2
    valid_moves_copy = list(ttt.valid_moves)
    for move in valid_moves_copy:
        ttt.make_move(move)
        score = -find_move(ttt, -turn)[0]
        ttt.undo_move()
        if score > max_score:
            max_score = score
            best_move = move
        if max_score == 1:
            break
    cache[board_tuple] = (max_score, best_move)
    return max_score, best_move


