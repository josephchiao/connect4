from dataclasses import dataclass, field
import setup

@dataclass
class Game:

    board : list 
    side : int = 0
    red_wins : bool = False
    yellow_wins : bool = False
    draw: bool = False

    def square(self, placement):
        if (
            0 <= placement[0] <= 5 
            and 0 <= placement[1] <= 6
        ):
            return self.board[placement[0]][placement[1]]

        else:
            return None

    def player_placement(self, placement):

        if placement not in [i for i in range(7)]:
            return False

        hight = 0
        while self.board[hight][placement] is not None:
            hight += 1
            if hight == 6:
                return False
        
        return [hight, placement]

    
    def connect_4(self, placement, direction):
        placement_copy = list(placement)
        for x in range(3):
            placement_copy[0] += direction[0]
            placement_copy[1] += direction[1]
            if self.square(placement_copy) != self.side:
                return False

        return True


    def game_draw(self):
        for rows in self.board:
            if None in rows:
                return False

        return True


    def update_win_con(self, placement):
        for direction in [
            (1, 0), 
            (-1, 0), 
            (0, 1), 
            (0, -1),
            (1, 1), 
            (-1, 1),
            (-1, -1),
            (1, -1)
        ]:
            if self.connect_4(placement, direction):
                if self.side == 1:
                    self.yellow_wins = True

                elif self.side == 0:
                    self.red_wins = True

        if self.game_draw():
            self.draw = True

    def win_con_general_eval(self):
        for rows in range(6):
            for position in range(7):
                if self.board[rows][position] == self.side:
                    self.update_win_con([rows, position])
                elif self.board[rows][position] is not None:
                    self.side = 1 - self.side
                    self.update_win_con([rows, position])
                    self.side = 1 - self.side

                if self.yellow_wins or self.red_wins:
                    return True

    def player_movement(self, player_input):
            
        placement = self.player_placement(player_input)
        
        if not placement:
            return False

        self.board[placement[0]][placement[1]] = self.side
        self.update_win_con(placement)
        self.side = 1 - self.side
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
    
