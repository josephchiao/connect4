import branch
import gameplay
import random

def eval(game):
    return random.random()


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
    best_line[1].insert(0, future_game)
    return best_line


