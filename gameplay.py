from dataclasses import dataclass, field
import setup

@dataclass
class Game:

    board : list 
    red_wins : bool = False
    yellow_wins : bool = False
    draw: bool = False


    def player_placement(self, placement):

        if placement not in [i for i in range(7)]:
            return False

        hight = 0
        while self.board[hight][placement] is not None:
            hight += 1
            if hight == 6:
                return False
        
        return (placement, hight)

    
    def connect_4(self, placement, direction):
        for x in range(3):
            if self.board[placement[0] + direction[0]][placement[1] + direction[1]] != self.side:
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
                [self.red_wins, self.yellow_wins][self.side] = True

        if self.game_draw():
            self.draw = True


@dataclass
class Play(Game):

    side : int = 0
    
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
    
