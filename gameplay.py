from dataclasses import dataclass, field
import setup

@dataclass
class Game:

    board : list 
    red_wins : bool = False
    yellow_wins : bool = False

    def player_placement(self, placement):

        if placement not in [i for i in range(7)]:
            return False

        hight = 0
        while self.board[hight][placement] is not None:
            hight += 1
            if hight == 6:
                return False
        
        return (hight, placement) 

    def winning_conditions(self, position, side): 

        if position[0] <= 2:
            if all([self.board[position[0] + i][position[1]] == side for i in range(4)]):
                return True
        if position[1] <= 3:
            if all([self.board[position[0]][position[1] + i] == side for i in range(4)]):
                return True
        if position[0] <= 2 and position[1] <= 3:
            if all([self.board[position[0] + i][position[1] + i] == side for i in range(4)]):
                return True
        if position[0] >= 2 and position[1] <= 3:
            if all([self.board[position[0] - i][position[1] + i] == side for i in range(4)]):
                return True

    def game_draw(self):

        for rows in self.board:
            if None in rows:
                return False
        return True

    def game_won(self):

        for row in self.board:
            for side in row:
                if side is not None and self.winning_conditions((self.board.index(row), row.index(side)), side):
                    if side == 0:
                        self.red_wins = True
                        return True
                    elif side == 1:
                        self.yellow_wins = True
                        return True
        return False

@dataclass
class Play(Game):

    side : int = 0
    
    def player_movement(self, player_input):
            
        placement = self.player_placement(player_input)
        
        if not placement:
            return False

        self.board[placement[0]][placement[1]] = self.side
        return True

    def player_input(self):

        player_input = -1
        
        while not self.player_movement(player_input):
            player_input = input("Input: ")
            if player_input not in ['1', '2', '3', '4', '5', '6', '7']:
                player_input = -1
            else:
                player_input = int(player_input) - 1

        return player_input
    
