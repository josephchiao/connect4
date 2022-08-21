import branch
import gameplay
import random

def eval(game):
    # eval = 0
    # for x in range(6):
    #     for y in range(7):
    #         if game.square([x, y]) is not None:
    #             eval += x

    if game.red_wins:
        return 0
    elif game.yellow_wins:
        return 1
    
    return random.random()


def tree_search(game, depth, level = 0):
    
    if game.win_con_general_eval():
        return [eval(game), [game]]

    elif level == depth:
        return [eval(game), [game]]

    lines = []
    for future_game in branch.branch_playable(game):
        lines.append(tree_search(future_game, depth, level = level + 1))

    function = [min, max][game.side]
    best_line = function(
        lines, 
        key=lambda line: line[0]
    )
    # if level == 1:
    #     print("best line = ", best_line)
        # print("lines are = ", lines)
    best_line[1].insert(0, game)
    return best_line