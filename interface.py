import gameplay as gp
import setup
import tree_search as ts


Game = gp.Game(setup.board_generation())

def display(board):

    board.reverse()
    if Game.side:
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

def player_vs_player():

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

def player_vs_computer():

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
    display(Game.board)
    
    while not end:

        if Game.side == player_side:
            Game.player_input()
            
        elif Game.side == computer_side:
            best_line = ts.tree_search(Game, 4)
            new_game_state = best_line[1][1]
            Game.board = new_game_state.board
            Game.side = 1 - Game.side 

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
    

player_vs_computer()
# player_vs_player()
# best_line = ts.tree_search(Game, 4)
# print(f"eval: {best_line[0]}")
# for game in best_line[1]:
#     display(game.board)