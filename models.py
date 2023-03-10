import random

class Player:
    def __init__(self, id:int, name:str) -> None:
        self.id = id
        self.name = name
        self.score = 0
        self.pos = [0,0]

    def change_pos(self, move:int, board_x:int, board_y:int) -> list:
        return [0,0]

class Board:
    def __init__(self, width:int, height:int) -> None:
        self.x = width
        self.y = height

class Ladder:
    def __init__(self, board_x:int, board_y: int) -> None:
        self.path = self.generate_pos(board_x, board_y)

    def generate_pos(self, board_x:int, board_y:int) -> dict:
        # min board size -> x:1, y:3
        begin = [random.randint(1, board_x-1), random.randint(0, board_y-3)]
        end = [random.randint(0, board_x-1), random.randint(begin[1]+1, board_y-1)]
        return {
            'begin': begin,
            'end': end
        }
    
class Snake:
    def __init__(self, board_x:int, board_y: int) -> None:
        self.path = self.generate_pos(board_x, board_y)

    def generate_pos(self, board_x:int, board_y:int) -> dict:
        # min board size -> x:1, y:3
        begin = [random.randint(0, board_x-1), random.randint(1, board_y-1)]
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
    
class Game:
    def __init__(self, players:list, board:Board, dice:Dice) -> None:
        self.players = players
        self.num_players = len(players)
        self.board = board
        self.dice = dice