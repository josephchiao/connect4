import gameplay as gp
import setup

Game = gp.Game(setup.board_generation())
# Game = gp.Game([[None, None, None, None, None, None, None], 
#                 [None, None, None, None, None, None, None], 
#                 [None, None, None, None, None, None, None], 
#                 [None, None, None, None, None, None, None], 
#                 [None, None, None, None, None, None, None], 
#                 [None, None, None, None, None, None, None]])
# Game = gp.Game([[None, None, None, None, None, None, None], 
#                 [None, None, None, None, None, None, None], 
#                 [0, None, None, None, None, None, None], 
#                 [0, None, None, None, None, None, None], 
#                 [0, None, None, None, None, None, None], 
#                 [0, None, None, None, None, None, None]])

Play = gp.Play(Game.board)

def display(board):

    board.reverse()
    if Play.side:
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
        Play.player_input()

        display(Game.board)

        if Game.game_draw():
            print("Game drawed")
            end = True

        if Game.game_won():
            end = True
            if Game.red_wins:
                print("Red wins")
            elif Game.yellow_wins:
                print("Yellow wins")

# player_vs_player()