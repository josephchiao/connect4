import interface as ui
import gameplay as gp
import setup
from dataclasses import dataclass
import copy

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

    def branch(self):

        possible_boards = []

        legal_moves = self.branch_avalibilities()

        for move in legal_moves:
            new_board = copy.deepcopy(self.board)
            new_board[move[0]][move[1]] = self.side
            possible_boards.append(new_board)

        return possible_boards

for i in range(len(branches(setup.board_generation(), 1).branch())):
    ui.display(branches(setup.board_generation(), 1).branch()[i])