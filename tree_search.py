import branch
import gameplay
import random
import archive.feedforward_prop as feedforward_prop
import numpy as np
import neural_network


def eval(game):

    '''A fake evaluation, returning random value for evaluation. ***for testing***'''

    if game.red_wins:
        return 0
    elif game.yellow_wins:
        return 1
    elif game.draw:
        return 0.5
    
    return random.random()

def nn_eval(game, nn):
    
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
    return nn.feedforward(x)

def alpha_beta_tree_search(game, nn, depth, mode = "combinatorics", level = 0, move = None, beta = None):

    '''Searches through all possible game states, and output the best one as a list of game states'''
    
    #If branch result in game conclusion, return as the end of branch
    if game.win_con_eval() is not None:
        return [game.win_con_eval(), [move], level]

    #If branch reached deapth, return as the end of branch
    elif level == depth:
        if mode == "nn":
            return [nn_eval(game, nn), [move], level]
        else:
            return[eval(game), [move], level]

    #Recursive search function
    alpha = None
    i = 0
    futures = len(branch.branch_avalibilities(game.board)) - 1

    while alpha_compare(alpha, beta, game.side) and i <= futures:

        future_move = branch.branch_avalibilities(game.board)[i]
        i += 1

        game.computer_movement(future_move)
        line = alpha_beta_tree_search(game, nn, depth, mode, level = level + 1, move = future_move, beta = alpha)
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
        alpha[1].append(move)
        return alpha
    
    return (alpha[1][-1], alpha[0])

def alpha_compare(alpha, beta, side):

    '''Part of the alpha beta search algorithm'''

    if alpha == None or beta == None:
        return True

    if side:
        if beta[0] >= alpha[0]:
            return True
    
    if beta[0] <= alpha[0]:
        return True

    return False

def tree_search(game, nn, depth, mode = "combinatorics", level = 0, move = None):

    '''Searches through all possible game states, and output the best one as a list of game states'''
    
    #If branch result in game conclusion, return as the end of branch
    if game.win_con_eval() is not None:
        return [game.win_con_eval(), move, level]

    #If branch reached deapth, return as the end of branch
    elif level == depth:
        if mode == "nn":
            return [nn_eval(game, nn), move, level]
        else:
            return[eval(game), move, level]

    #Recursive search function
    lines = []
    for future_move in branch.branch_avalibilities(game.board):
        
        game.computer_movement(future_move)
        lines.append(tree_search(game, nn, depth, mode, level = level + 1, move = future_move))
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