import random

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
        self.num_cells = self.x * self.y

class Ladder:
    def __init__(self, board_x:int, board_y: int) -> None:
        self.path = self.generate_pos(board_x, board_y)

    def generate_pos(self, board_x:int, board_y:int) -> dict:
        # min board size -> x:10, y:10
        begin = [random.randint(1, board_x-1), random.randint(0, board_y-3)] # [x,y]
        end = [random.randint(0, board_x-1), random.randint(begin[1]+1, board_y-1)]
        return {
            'begin': begin,
            'end': end
        }
    
class Snake:
    def __init__(self, board_x:int, board_y: int) -> None:
        self.path = self.generate_pos(board_x, board_y)

    def generate_pos(self, board_x:int, board_y:int) -> dict:
        # min board size -> x:10, y:10
        begin = [random.randint(0, board_x-1), random.randint(1, board_y-1)] # [x,y]
        end = [random.randint(0, board_x-1), random.randint(0, begin[1]-1)]
        return {
            'begin': begin,
            'end': end
        }

class Dice:
    def __init__(self, sides:int=6) -> None:
        self.sides = sides

    def get_roll(self) -> int:
        return random.randint(1,self.sides)
    
class Cell:
    def __init__(self, has_snake_ladder: bool, has_special_event: bool) -> None:
        self.has_snake_ladder = has_snake_ladder
        self.has_special_event = has_special_event

class Game:
    def __init__(self, players:list, board:Board, dices:list, turn_limit:int, diff: str) -> None:
        self.players = players
        self.num_players = len(players)
        self.board = board
        self.dices = dices
        self.turn_limit = turn_limit

    def roll_dices(self, dices:list) -> int:
        final_roll = [dices[0].get_roll(), dices[1].get_roll()]

        # determine extra roll
        if final_roll[0] == final_roll[1]: return dices[0].get_roll() + sum(final_roll)
        else: return sum(final_roll)

    def generate_snakes_ladders(self, board: Board):
        n_objects = board.x
        board.y
        

    
