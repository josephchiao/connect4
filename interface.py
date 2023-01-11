import gameplay as gp
import setup
import tree_search as ts
import branch
import numpy as np
import time


def display(board, side):

    board.reverse()
    if side:
        print("\nYellow")
    else:
        print("\nRed")
    print("1 2 3 4 5 6 7")
    for rows in board:
        
        row = ""
        for position in rows:

            if position is None:
                row += "- "
            
            elif position == 1:
                row += "Y "
            
            elif position == 0:
                row += "R "
        
        print(row)
    board.reverse()

def player_vs_player(Game):

    end = False
    display(Game.board)
    while not end:

        Game.player_input()

        display(Game.board)
        if Game.draw:
            print("Game drawed")
            end = True
        elif Game.red_wins:
            print("Red wins")
            end = True
        elif Game.yellow_wins:
            print("Yellow wins")
            end = True

def player_vs_computer(nn_depth):

    Game = gp.Game(setup.board_generation())

    thetas = np.load(f'/Users/joseph_chiao/Desktop/Advance Research/Machine Learning/Connect 4 Neural network(Kai)/connect4/genetic_elite_data/nn_theta_set_0.npz')
    theta_1 = thetas['Theta1']
    theta_2 = thetas['Theta2']
    theta_3 = thetas['Theta3']

    player_side = None

    while player_side is None:
        player_color = input("What color would you like to play as?").lower()

        if player_color == "red" or player_color == "r":
            player_side = 0
            computer_side = 1

        elif player_color == "yellow" or player_color == "y":
            player_side = 1
            computer_side = 0

    end = False
    # display(Game.board, Game.side)
    
    while not end:
        display(Game.board, Game.side)

        if Game.side == player_side:
            Game.player_input()


        elif Game.side == computer_side:
            start = time.time()
            best_move = ts.alpha_beta_tree_search(Game, nn_depth, "nn", theta_1 = theta_1, theta_2 = theta_2, theta_3 = theta_3)
            end = time.time()
            elapse = (end - start)
            print(elapse)
            Game.computer_movement(best_move)

        end = game_interval(Game)

def connect_4_cheater(nn_depth):

    Game = gp.Game([[1, None, 1, 0, 1, 0, 0], 
                    [0, None, 0, 0, 0, 1, None],
                    [None, None, 1, 1, 1, 0, None],
                    [None, None, None, 1, None, 0, None],
                    [None, None, None, 1, None, 0, None],
                    [None, None, None, 0, None, 1, None]])

    thetas = np.load(f'/Users/joseph_chiao/Desktop/Advance Research/Machine Learning/Connect 4 Neural network(Kai)/connect4/genetic_elite_data/nn_theta_set_0.npz')
    theta_1 = thetas['Theta1']
    theta_2 = thetas['Theta2']
    theta_3 = thetas['Theta3']

    player_side = None

    while player_side is None:
        player_color = input("What color would you like to play as?").lower()

        if player_color == "red" or player_color == "r":
            player_side = 0
            computer_side = 1
            Game.side = 1

        elif player_color == "yellow" or player_color == "y":
            player_side = 1
            computer_side = 0
            Game.side = 0


    end = False
    display(Game.board, Game.side)
    
    while not end:

        if Game.side == player_side:
            Game.player_input()


        elif Game.side == computer_side:
            best_move = ts.alpha_beta_tree_search(Game, nn_depth, "nn", theta_1 = theta_1, theta_2 = theta_2, theta_3 = theta_3)
        
            Game.computer_movement(best_move)

        display(Game.board, Game.side)
        end = game_interval(Game)

def nn_vs_random(theta_set, nn_depth, random_depth):
    
    Game = gp.Game(setup.board_generation())

    thetas = np.load(f'/Users/joseph_chiao/Desktop/Advance Research/Machine Learning/Connect 4 Neural network(Kai)/connect4/genetic_training_data/nn_theta_set_{theta_set}.npz')
    theta_1 = thetas['Theta1']
    theta_2 = thetas['Theta2']
    theta_3 = thetas['Theta3']

    end = False
    
    while not end:

        if Game.side == 0:
            best_move = ts.alpha_beta_tree_search(Game, random_depth)
        elif Game.side == 1:
            best_move = ts.alpha_beta_tree_search(Game, nn_depth, "nn", theta_1 = theta_1, theta_2 = theta_2, theta_3 = theta_3)
        # print(best_move)

        Game.computer_movement(best_move)
        
        end = game_interval(Game)
    
    return(Game.red_wins, Game.yellow_wins, Game.draw)


def nn_vs_nn(player_1, player_2, nn_depth, trainer_depth):

    Game = gp.Game(setup.board_generation())

    p1_thetas = np.load(f'/Users/joseph_chiao/Desktop/Advance Research/Machine Learning/Connect 4 Neural network(Kai)/connect4/genetic_training_data/nn_theta_set_{player_1}.npz')
    p1_theta_1 = p1_thetas['Theta1']
    p1_theta_2 = p1_thetas['Theta2']
    p1_theta_3 = p1_thetas['Theta3']

    p2_thetas = np.load(f'/Users/joseph_chiao/Desktop/Advance Research/Machine Learning/Connect 4 Neural network(Kai)/connect4/genetic_training_data/nn_theta_set_{player_2}.npz')
    p2_theta_1 = p2_thetas['Theta1']
    p2_theta_2 = p2_thetas['Theta2']
    p2_theta_3 = p2_thetas['Theta3']

    end = False
    
    while not end:

        if Game.side == 0:
            best_move = ts.alpha_beta_tree_search(Game, nn_depth, "nn", theta_1 = p1_theta_1, theta_2 = p1_theta_2, theta_3 = p1_theta_3)
        elif Game.side == 1:
            best_move = ts.alpha_beta_tree_search(Game, trainer_depth, "nn", theta_1 = p2_theta_1, theta_2 = p2_theta_2, theta_3 = p2_theta_3)
        # print(best_move)

        Game.computer_movement(best_move)
        
        end = game_interval(Game)
    
    return(Game.red_wins, Game.yellow_wins, Game.draw)


def nn_result_testing():

    Game = gp.Game(setup.board_generation())

    thetas = np.load(f'/Users/joseph_chiao/Desktop/Advance Research/Machine Learning/Connect 4 Neural network(Kai)/connect4/genetic_elite_data/nn_theta_set_0.npz')
    theta_1 = thetas['Theta1']
    theta_2 = thetas['Theta2']
    theta_3 = thetas['Theta3']

    end = False
    
    while not end:

        if Game.side == 0:
            best_move = ts.alpha_beta_tree_search(Game, 2, 'nn', theta_1 = theta_1, theta_2 = theta_2, theta_3 = theta_3)
        elif Game.side == 1:
            best_move = ts.alpha_beta_tree_search(Game, 2)
        # print(best_move)

        Game.computer_movement(best_move)
        
        end = game_interval(Game)
    
    return(Game.red_wins, Game.yellow_wins, Game.draw)

def game_interval(Game):
    
    # display(Game.board, Game.side)
    # Game.win_con_general_eval()
    if Game.draw:
        print("Game drawed")
        display(Game.board, Game.side)
        return True
    elif Game.red_wins:
        print("Red wins")
        display(Game.board, Game.side)
        return True
    elif Game.yellow_wins:
        print("Yellow wins")
        display(Game.board, Game.side)
        return True
    
    return False
  
# Game = gp.Game([[1, 0, 1, 0, 1, 0, 1], [0, 0, 0, None, 1, 0, None], [0, 0, 1, None, 0, 1, None], [1, 1, 1, None, 0, 0, None], [1, 1, 1, None, 0, 1, None], [0, 0, 1, None, 1, 0, None]], side= 1)
# Game.update_win_con((5,2))
# print(Game)
# computer_vs_computer()
player_vs_computer(7)
# player_vs_player()
# best_line = ts.tree_search(Game, 4)
# print(f"eval: {best_line[0]}")
# for game in best_line[1]:
#     display(game.board)
# red = 0
# yellow = 0
# for i in range(100):
#     red_w, yellow_w , draw= nn_result_testing()
#     if red_w:
#         red += 1
#     elif yellow_w:
#         yellow += 1

# print(red, yellow)

# connect_4_cheater(7)
