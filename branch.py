import gameplay as gp
import setup
from dataclasses import dataclass
import copy


def branch_avalibilities(board):
    
    legal_moves = []
    for move in range(7):
        if gp.Game(board).player_placement(move):
            placement = gp.Game(board).player_placement(move)
            legal_moves.append(placement)

    return legal_moves

def board_branch(board, side):

    possible_boards = []

    legal_moves = branch_avalibilities(board)

    for move in legal_moves:
        new_board = copy.deepcopy(board)
        new_board[move[0]][move[1]] = side
        possible_boards.append(new_board)

    return possible_boards

def branch_playable(game):
    '''Returns a list of possible future branches'''

    playable_branch = []
    legal_moves = branch_avalibilities(game.board)
    for possible_position in legal_moves:
        branch = copy.deepcopy(game)
        branch.computer_movement(possible_position)
        playable_branch.append(branch)
    
    return playable_branch