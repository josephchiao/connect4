import branch
import gameplay
import random
import feedforward_prop
import numpy as np

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
    elif game.draw:
        return 0.5
    
    return random.random()

def nn_eval(game, theta_1, theta_2, theta_3):
    
    '''Evaluate board position value using neural network, takes in game state and thetas to produce a float output'''

    #Winning/ losing conditions, no computation required
    if game.red_wins:
        return 0
    elif game.yellow_wins:
        return 1

    #Transforming the board into readable array for the neural network
    red_board = np.array([i for j in game.board for i in j])
    
    yellow_board = np.where(red_board == 1, None, red_board)
    yellow_board = np.where(yellow_board == 0, 1, yellow_board)
    
    complete_board = np.concatenate((red_board, yellow_board))

    x = np.where(complete_board == None, 0, complete_board).astype(float)
    

    return feedforward_prop.feedforward_prop(x, theta_1, theta_2, theta_3)[0]

def tree_search(game, depth, mode = "combinatorics", theta_1 = None, theta_2 = None, theta_3 = None, level = 0, move = None):

    '''Searches through all possible game states, and output the best one as a list of game states'''
    
    #If branch result in game conclusion, return as the end of branch
    if game.win_con_eval() is not None:
        return [game.win_con_eval(), move, level]

    #If branch reached deapth, return as the end of branch
    elif level == depth:
        if mode == "nn":
            return [nn_eval(game, theta_1, theta_2, theta_3), move, level]
        else:
            return[eval(game), move, level]

    #Recursive search function
    lines = []
    for future_move in branch.branch_avalibilities(game.board):
        
        game.computer_movement(future_move)
        lines.append(tree_search(game, depth, mode, theta_1, theta_2, theta_3, level = level + 1, move = future_move))
        game.movement_undo(future_move)

    #If there is an absolute win, then take the fastest win sequence
    comfirmed_win_lines = []
    for line in lines:
        if line[0] == game.side:
            comfirmed_win_lines.append(line)

    if len(comfirmed_win_lines):
        best_line = min(comfirmed_win_lines, key=lambda line: line[-1])

    #If there is an absolute defeat, take the longest lost sequence possible
    elif all(line[0] == (1 - game.side) for line in lines):
        best_line = max(lines, key=lambda line: line[-1])

    #Search for optimal branch in each depth if there is no absolute end game
    else:
        function = [min, max][game.side]
        best_line = function(
            lines, 
            key=lambda line: line[0])
    
    if level != 0:
        best_line.insert(1, move)
        return best_line
    
    print(best_line)
    return best_line[1]


def alpha_beta_tree_search(game, depth, mode = "combinatorics", theta_1 = None, theta_2 = None, theta_3 = None, level = 0, move = None, beta = None):

    '''Searches through all possible game states, and output the best one as a list of game states'''
    
    #If branch result in game conclusion, return as the end of branch
    if game.win_con_eval() is not None:
        return [game.win_con_eval(), move, level]

    #If branch reached deapth, return as the end of branch
    elif level == depth:
        if mode == "nn":
            return [nn_eval(game, theta_1, theta_2, theta_3), move, level]
        else:
            return[eval(game), move, level]

    #Recursive search function
    lines = []
    alpha = None
    i = 0
    futures = len(branch.branch_avalibilities(game.board)) - 1
    while alpha_compare(alpha, beta, game.side) and i <= futures:
       
        future_move = branch.branch_avalibilities(game.board)[i]
        i += 1

        game.computer_movement(future_move)
        line = alpha_beta_tree_search(game, depth, mode, theta_1, theta_2, theta_3, level = level + 1, move = future_move, beta = alpha)
        game.movement_undo(future_move)

        if alpha is None:
            alpha = line

        elif game.side:
            if line[0] > alpha[0]:
                alpha = line
        
        elif game.side == 0:
            if line[0] < alpha[0]:
                alpha = line
    
    if level != 0:
        alpha.insert(1, move)
        return alpha
    
    print(alpha)
    return alpha[1]


def alpha_compare(alpha, beta, side):
    if alpha == None or beta == None:
        return True

    if side:
        if beta[0] >= alpha[0]:
            return True
    
    if beta[0] <= alpha[0]:
        return True

    return False

def branch_priority(game, theta_1, theta_2, theta_3):
    interst_level = {i: None for i in range(7)}
    i = 0
    for future_move in branch.branch_avalibilities(game.board):
        interst_level.append(tree_search(game, 0, "nn", theta_1, theta_2, theta_3, level = 0, move = future_move))
        i += 1


