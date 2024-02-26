import random

def cached(func):
    cache = {}

    def inner(ttt):
        board_tuple = tuple(item for row in ttt.board for item in row)
        if board_tuple not in cache:
            cache[board_tuple] = func(ttt)
        return cache[board_tuple]
    return inner

def find_best_move(ttt):
    random.shuffle(ttt.valid_moves)
    score, best_move = find_move(ttt)
    return score, best_move

@cached
def find_move(ttt):
    if win := ttt.winned()[0]:
        return ttt.turn*win, ()

    if ttt.drow():
        return 0, ()

    best_move = ()
    max_score = -2
    valid_moves_copy = list(ttt.valid_moves)
    for move in valid_moves_copy:
        ttt.make_move(move)
        score = -find_move(ttt)[0]
        ttt.undo_move()
        if score > max_score:
            max_score = score
            best_move = move
        if max_score == 1:
            break

    return max_score, best_move


