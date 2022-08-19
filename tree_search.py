import branch
import gameplay
import random

def eval(game):
    eval = 0
    for x in range(6):
        for y in range(7):
            if game.square([x, y]) is not None:
                eval += x

    return eval



def tree_search(game, depth, level = 0):
    if level == depth:
        return [eval(game), [game]]

    lines = []
    for future_game in branch.branch_playable(game):
        lines.append(tree_search(future_game, depth, level = level + 1))

    function = [max, min][game.side]
    best_line = function(
        lines, 
        key=lambda line: line[0]
    )
    best_line[1].insert(0, game)
    return best_line


