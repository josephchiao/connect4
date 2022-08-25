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

def tree_search(game, depth, theta_1 = None, theta_2 = None, theta_3 = None, level = 0, move = None):

    '''Searches through all possible game states, and output the best one as a list of game states'''
    
    #If branch result in game conclusion, return as the end of branch
    if game.win_con_eval() is not None:
        return [game.win_con_eval(), move]

    #If branch reached deapth, return as the end of branch
    elif level == depth:
        return [eval(game), move]

    #Recursive search function
    lines = []
    for future_move in branch.branch_avalibilities(game.board):
        
        game.computer_movement(future_move)
        lines.append(tree_search(game, depth, theta_1, theta_2, theta_3, level = level + 1, move = future_move))
        game.movement_undo(future_move)


    #Search for optimal branch in each depth
    function = [min, max][game.side]
    best_line = function(
        lines, 
        key=lambda line: line[0])
    
    if level != 0:

        best_line.insert(1, move)
        return best_line
    
    print(best_line)
    return best_line[1]

