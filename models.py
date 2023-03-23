import random
import numpy as np

from scipy.stats import binom
from math import floor

class Player:
    """
    Player Class.

    Attributes:
        id (str): The unique identifier for every Player.
        name (str): The name of the Player.
        score (int): The total points that the Player has.
        pos (list): The current position of the Player in the Board. 
    """

    def __init__(self, id:int, name:str) -> None:
        """
        Initialize Player Class, the default score and position is 0.  

        Args:
            id (str): The unique identifier for every Player.
            name (str): The name of the Player.
        """

        self.id = id
        self.name = name
        self.score = 0
        self.pos = [0,0]

    def change_pos(self, move:int, board_x:int, board_y:int) -> None:
        """
        Function that changes the attribute Position of the Player.

        Args:
            move (int)
            board_x (int)
            board_y (int)

        Returns:
            None
        """

        self.pos = [(self.pos[0] + move) % board_x, ((self.pos[0] + move) // board_y) + self.pos[1]]
        
        if self.pos[1] > board_y - 1:
            self.pos = [board_x - 1, board_y - 1]

    def change_score(self, change: int) -> None:
        """
        Function that changes the attribute Score of the Player.

        Args:
            change (int)

        Returns:
            None
        """

        self.score += change

    def __repr__(self) -> str:
        """
        Create the string representation of the Player Class.
        """
        return f'Player {self.id}: {self.name} | Position: {self.position} | Score: {self.score}'


class Board:
    def __init__(self, width:int, height:int) -> None:
        self.width = width
        self.height = height

    def generate_cells(self) -> list: 
        return [[Cell(x, y) for y in np.arange(0, self.height)] for x in np.arange(0, self.width)]

class Ladder:
    def __init__(self, id:int, board_x:int, board_y: int) -> None:
        self.id = id
        self.path = self.generate_pos(board_x, board_y)

    def generate_pos(self, board_x:int, board_y:int) -> dict:
        # min board size -> x:10, y:10
        begin = [random.randint(1, board_x - 1), random.randint(0, board_y - 3)] # [x,y]
        end = [random.randint(0, board_x - 1), random.randint(begin[1] + 1, board_y - 1)]

        return {'begin': begin, 'end': end}
    
class Snake:
    def __init__(self, id:int, board_x:int, board_y: int) -> None:
        self.id = id
        self.path = self.generate_pos(board_x, board_y)

    def generate_pos(self, board_x:int, board_y:int) -> dict:
        # min board size -> x:10, y:10
        begin = [random.randint(0, board_x - 1), random.randint(1, board_y - 1)] # [x,y]
        end = [random.randint(0, board_x - 1), random.randint(0, begin[1] - 1)]

        return {'begin': begin, 'end': end}

class Dice:
    def __init__(self, sides:int = 6) -> None:
        self.sides = sides

    def get_roll(self) -> int:
        return random.randint(1, self.sides)
    
class Cell:
    def __init__(self, x:int, y:int) -> None:
        self.x = x
        self.y = y
        self.has_object = False
        self.object = None

class Game:
    def __init__(self, players:list, board:Board, dices:list, difficulty: str) -> None:
        self.players = random.shuffle(players)
        self.board = board
        self.dices = dices
        self.difficulty = difficulty
        
        self.probability = {'Fácil': 0.85, 
                            'Normal': 0.5, 
                            'Difícil': 0.25, 
                            'Legendaria': 0.01}
        
        #Determine the number of Snakes & Ladders the game will have according to the difficulty
        self.n_ladders = self.get_n_ladders(board = self.board, threshold = 0.9)
        self.n_snakes = self.get_n_snakes(board = self.board, threshold = 0.9)
        
        #Generate all the Cells of the Board
        self.cells = self.board.generate_cells()
        
        #Put a special event on the first and last cell so we don't have snakes or ladders
        self.cells[0][0].has_object = True
        self.cells[-1][-1].has_object = True
        
        #Generate the Snakes & Ladders
        self.snakes = self.get_snake_ladders(Snake, self.n_snakes, self.board.width, self.board.height)
        self.ladders = self.get_snake_ladders(Ladder, self.n_ladders, self.board.width, self.board.height)

        #Get the position of the Snakes & Ladders
        self.snakes = [x.path for x in self.snakes]
        self.ladders = [x.path for x in self.ladders]

        #Sort the position of the Snakes & Ladders
        self.snakes = sorted(self.snakes, key = lambda x: x['begin'])
        self.ladders = sorted(self.ladders, key = lambda x: x['begin'])

    def roll_dices(self, dices:list) -> int:
        final_roll = [dices[0].get_roll(), dices[1].get_roll()]

        #Determine extra roll
        if final_roll[0] == final_roll[1]:
            print('You Get an Extra Roll!!!')

            return dices[0].get_roll() + sum(final_roll)
        else: 
            
            return sum(final_roll)

    def get_n_snakes(self, board: Board, threshold: float = 0.9) -> int:
        n = round(threshold * ((board.width + board.height) / 2))
        q = 1 - self.probability[self.difficulty]
        
        return binom.rvs(n, q)
        
    def get_n_ladders(self, board: Board, threshold: float = 0.9) -> int:
        n = round(threshold * ((board.width + board.height) / 2))
        p = self.probability[self.difficulty]

        return binom.rvs(n, p)

    def get_bools(self, obj_pos: dict) -> bool:
        s1 = self.cells[obj_pos['begin'][0]][obj_pos['begin'][1]].has_object == False
        s2 = self.cells[obj_pos['end'][0]][obj_pos['end'][1]].has_object == False

        return s1 and s2

    def get_snake_ladders(self, Obj: Snake or Ladder, n_objs: int,  x: int, y: int) -> list:
        obj = Obj(0, x, y)
        obj_pos = obj.generate_pos(x, y)

        objs = []
        i = 1

        while len(objs) != n_objs: 
            if not self.get_bools(obj_pos):
                obj = Obj(0, x, y)
                obj_pos = obj.generate_pos(x, y)
            else:
                obj.id = i

                self.cells[obj_pos['begin'][0]][obj_pos['begin'][1]].has_object = True 
                self.cells[obj_pos['end'][0]][obj_pos['end'][1]].has_object = True
                self.cells[obj_pos['end'][0]][obj_pos['end'][1]].object = obj

                objs.append(obj)

                i += 1

        return objs
    
    def change_player_pos_and_score(self, player: Player, move:int) -> None:
        player.change_pos(move, self.board.x, self.board.y)
        cell = self.cells[player.pos[0]][player.pos[1]]

        if cell.has_object:
            try:
                new_pos = cell.object.path
                player.pos = [new_pos['begin'], new_pos['end']]

                if type(cell) == Ladder:
                    player.change_score((move * 10) + 1)

                elif type(cell) == Snake:
                    player.change_score((move * 10) - 1)

            except:
                pass
        else:
            player.change_score(move * 10)

    def win_game(self, player:Player) -> bool:
        last_cell = self.cells[-1][-1]
        
        return player.pos == [last_cell.x, last_cell.y]

