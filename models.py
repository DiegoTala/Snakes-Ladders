import random
import numpy as np

from scipy.stats import binom
from math import floor

class Player:
    def __init__(self, id:int, name:str) -> None:
        self.id = id
        self.name = name
        self.score = 0
        self.pos = [0,0]

    def change_pos(self, move:int, board_x:int, board_y:int) -> None:
        self.pos = [(self.pos[0] + move) % board_x, ((self.pos[0]+move) // board_y) + self.pos[1]]
        
    def change_score(self, change: int) -> None:
        self.score += change

    def __repr__(self) -> str:
        return f'Player {self.id}: {self.name} | Position: {self.position} | Score: {self.score}'


class Board:
    def __init__(self, width:int, height:int) -> None:
        self.x = width
        self.y = height

    def generate_cells(self) -> list: 
        return [[Cell(x, y) for y in np.arange(0, self.height)] for x in np.arange(0, self.width)]

class Ladder:
    def __init__(self, board_x:int, board_y: int) -> None:
        self.path = self.generate_pos(board_x, board_y)

    def generate_pos(self, board_x:int, board_y:int) -> dict:
        # min board size -> x:10, y:10
        begin = [random.randint(1, board_x - 1), random.randint(0, board_y - 3)] # [x,y]
        end = [random.randint(0, board_x - 1), random.randint(begin[1] + 1, board_y - 1)]

        return {'begin': begin, 'end': end}
    
class Snake:
    def __init__(self, board_x:int, board_y: int) -> None:
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

class Game:
    def __init__(self, players:list, board:Board, dices:list, turn_limit:int, difficulty: str) -> None:
        self.players = players
        self.num_players = len(players)
        
        self.board = board
        self.dices = dices
        
        self.turn_limit = turn_limit
        self.difficulty = difficulty
        
        self.probability = {'Fácil': 0.85, 
                            'Normal': 0.5, 
                            'Difícil': 0.25, 
                            'Legendaria': 0.01}
        
        self.n_ladders = self.get_n_ladders(self, board = self.board, threshold = 0.9)
        self.n_snakes = self.get_n_snakes(self, board = self.board, threshold = 0.9)
        
        self.cells = self.board.generate_cells()
        
        #Put a special event on the first and last cell so we don't have snakes or ladders
        self.cells[0][0].has_object = True
        self.cells[-1][-1].has_object = True
        
        self.snakes = self.get_snake_ladders(Snake, self.n_snakes, self.board.width, self.board.height)
        self.ladders = self.get_snake_ladders(Ladder, self.n_ladders, self.board.width, self.board.height)

    def roll_dices(self, dices:list) -> int:
        final_roll = [dices[0].get_roll(), dices[1].get_roll()]

        # determine extra roll
        if final_roll[0] == final_roll[1]: return dices[0].get_roll() + sum(final_roll)
        else: return sum(final_roll)

    def get_n_snakes(self, board: Board, threshold: float = 0.9) -> int:
        n = round(threshold * ((self.board.width + self.board.height) / 2))
        q = 1 - self.probability[self.difficulty]
        
        return binom.rvs(n, q)
        
    def get_n_ladders(self, board: Board, threshold: float = 0.9) -> int:
        n = round(threshold * ((self.board.width + self.board.height) / 2))
        p = self.probability[self.difficulty]

        return binom.rvs(n, p)

    def get_bools(self, obj_pos: dict) -> bool:
        s1 = self.cells[obj_pos['begin'][0]][obj_pos['begin'][1]].has_object == False
        s2 = self.cells[obj_pos['end'][0]][obj_pos['end'][1]].has_object == False

        return s1 and s2

    def get_snake_ladders(self, Obj: Snake or Ladder, n_objs: int,  x: int, y: int) -> list:
        obj = Obj(x, y)
        obj_pos = obj.generate_pos(x, y)

        objs = []

        while len(objs) != n_objs: 
            if not self.get_bools(obj_pos):
                obj = Obj(x, y)
                obj_pos = obj.generate_pos(x, y)
            else:
                self.cells[obj_pos['begin'][0]][obj_pos['begin'][1]].has_object = True 
                self.cells[obj_pos['end'][0]][obj_pos['end'][1]].has_object = True
                objs.append(obj_pos)

        return sorted(objs, key = lambda x: x['begin'])
        

    
