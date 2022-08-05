import interface as ui
import gameplay as gp
import setup
from dataclasses import dataclass

@dataclass
class branches:

    board : list
    side : int

    def branch_avalibilities(self):
        
        legal_moves = []
        for move in range(7):
            if gp.Game(self.board).player_placement(move):
                placement = gp.Game(self.board).player_placement(move)
                legal_moves.append(placement)

            
        return legal_moves        


possible_positions = []
board = setup.board_generation()
test = branches(board, 0)
legal_moves = test.branch_avalibilities()
for move in legal_moves:
    print(move)
    print(test.branch_possibilities(move))
    possible_positions.append(test.branch_possibilities(move))
print(possible_positions)