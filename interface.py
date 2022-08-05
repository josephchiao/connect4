import gameplay as gp
import setup

Play = gp.Play(setup.board_generation())

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
    display(Play.board)
    while not end:
        Play.player_input()

        display(Play.board)
        if Play.draw:
            print("Game drawed")
            end = True
        elif Play.red_wins:
            print("Red wins")
            end = True
        elif Play.yellow_wins:
            print("Yellow wins")
            end = True

player_vs_player()