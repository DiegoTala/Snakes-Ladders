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
        
        #We need to ensure that the position of the player it's not bigger than the maximum Cell path.
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
        return f'Player {self.id}: {self.name} | Position: {self.pos} | Score: {self.score}'


class Board:

    """
    Board Class.

    Attributes:
        width (int): The width of the board.
        height (str): The height of the board.
    """
    def __init__(self, width:int, height:int) -> None:
        """
        Function that defines the board's size.

        Args:
            width (int)
            height (int)

        Returns:
            None
        """

        self.width = width
        self.height = height


    def generate_cells(self) -> list: 
        """
        Function that generates the cells according to the width and height.

        Args:
            None

        Returns:
            None
        """
        return [[Cell(x, y) for y in np.arange(0, self.height)] for x in np.arange(0, self.width)]


class Ladder:

    """
    Ladder Class.

    Attributes:
        n_ladders (int): The number of Ladders the game will have.
        ladders (list): A list with the path (initial and final position) of every Ladder of the game

    """

    def __init__(self, id:int, board_x:int, board_y: int) -> None:
        """
        Init method to build Ladder class.

        Args:
        board_x (int): Board's x position.
        board_y (int) : Board's y position.

        Returns:
            None
        """
        self.id = id
        self.path = self.generate_pos(board_x, board_y)

    def generate_pos(self, board_x:int, board_y:int) -> dict:

        """
        Function that defines where the Ladders can start and end.

        Args:
        None

        Returns:
            dict
        """
        # min board size -> x:10, y:10
        begin = [random.randint(1, board_x - 1), random.randint(0, board_y - 3)] # [x,y]
        end = [random.randint(0, board_x - 1), random.randint(begin[1] + 1, board_y - 1)]

        return {'begin': begin, 'end': end}
    
class Snake:
    """
    Snake Class.

    Attributes:
        n_snake (int): The number of Snakes the game will have.
        snakes (list): A list with the path (initial and final position) of every Snake of the game
        board_x (int): Board's x position.
        board_y (int) : Board's y position.
    """

    def __init__(self, id:int, board_x:int, board_y: int) -> None:
        """
        Init method to build Snake class.

        Args:
        board_x (int): Board's x position.
        board_y (int) : Board's y position.

        Returns:
            None
        """
        self.id = id
        self.path = self.generate_pos(board_x, board_y)

    def generate_pos(self, board_x:int, board_y:int) -> dict:
        """
        Function that defines where the Snakes can start and end.

        Args:
        None

        Returns:
            dict
        """
    
        # min board size -> x:10, y:10
        begin = [random.randint(0, board_x - 1), random.randint(1, board_y - 1)] # [x,y]
        end = [random.randint(0, board_x - 1), random.randint(0, begin[1] - 1)]

        return {'begin': begin, 'end': end}

class Dice:
    """
    Dice Class.

    Attributes:
        sides (int): The number of sides the Dice has.
        dices (list): A list of Dices Objects.
    """
    def __init__(self, sides:int = 6) -> None:
        """
        Init method to build Dice class.

        Args:
        sides (int): The number of sides the Dice has.

        Returns:
            None
        """
    
        self.sides = sides

    def get_roll(self) -> int:
        """
        Function that defines the result of the Dice roll.

        Args:
        None

        Returns:
            int
        """
        return random.randint(1, self.sides)
    
    
class Cell:
    """
    Cell Class.

    Attributes:
        x (int): The x coordinate of the cell.
        y (int): The y coordinate of the cell.
    """
    def __init__(self, x:int, y:int) -> None:
        """
        Init method to build Cell class.

        Args:
        x (int): The x coordinate of the cell.
        y (int): The y coordinate of the cell.

        Returns:
            None
        """
        self.x = x
        self.y = y
        self.has_object = False
        self.object = None

class Game:
    """
    The Class Game configurates the Snakes & Ladders Game.

    Attributes:
        players (list): A list of Players objects.
        board (Board): The Board object.
        dices (list): A list of Dices Objects.
        difficulty (str): The difficulty that the game will have, 
                          it helps to determine the number of Snakes & Ladders.
        probability (dict): A dictionary of probabilities according to the difficulty of the game, 
                            the probabilities will determine the parameter p or q of the Binomial
                            distribution it's used to generate the Snakes & Ladders.
        n_snakes (int): The number of Snakes the game will have.
        n_ladders (int): The number of Ladders the game will have.
        cells (list): A list with of Cell objects, it's generated by the board of the game.
        snakes (list): A list with the path (initial and final position) of every Snake of the game.
        ladders (list): A list with the path (initial and final position) of every Ladder of the game.
    """

    def __init__(self, players:list, board:Board, dices:list, difficulty: str) -> None:
        """
        Initialize Game Class.

        Args:
            players (list): A list of randomly shuffled Players objects.
            board (Board): The Board object.
            dices (list): A list of Dices Objects.
            difficulty (str): The difficulty that the game will have, it helps to determine the number of Snakes & Ladders.

        """

        #Apply a shuffle to determine the order of turns of the Players
        self.players = players
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
        
        #Generate the Snakes & Ladders as objects
        self.snakes = self.get_snake_ladders(Snake, self.n_snakes, self.board.width, self.board.height)
        self.ladders = self.get_snake_ladders(Ladder, self.n_ladders, self.board.width, self.board.height)

        #Get the position of the Snakes & Ladders
        self.snakes = [x.path for x in self.snakes]
        self.ladders = [x.path for x in self.ladders]

        #Sort the position of the Snakes & Ladders
        self.snakes = sorted(self.snakes, key = lambda x: x['begin'])
        self.ladders = sorted(self.ladders, key = lambda x: x['begin'])

    def roll_dices(self, dices:list) -> int:
        """
        Function to get the total number of Cells that the Player will move according to two Dices. 
        If the number of the two Dices it's the same, the player will get an extra roll.

        Args:
            dices (list)

        Returns:
            Int
        """
        #Get the roll for the two Dices
        final_roll = [dices[0].get_roll(), dices[1].get_roll()]

        #Determine extra roll
        if final_roll[0] == final_roll[1]:
            print('You Get an Extra Roll!!!')
            print(dices[0].get_roll() + sum(final_roll))
            return dices[0].get_roll() + sum(final_roll)
        else: 
            print(sum(final_roll))
            return sum(final_roll)

    def get_n_snakes(self, board: Board, threshold: float = 0.9) -> int:
        """
        Function that determines the number of Snakes the game will have according to the Board width, 
        Board length, a threshold and the difficulty. At the end, the number of Snakes is determined by
        a Binomial Distribution where:

            n = The number of times we're going to make a Bernoulli trial (The Binomial distribution can be seen
            as making 'n' times the Bernoulli trial), this is determined by the average of the width and the 
            length of the Board multiplied by a threshold (To 'minimize' the maximum amount of Snakes and Ladders
            we'll have if we put a Snake and a Ladder for every number of row and column of the Board).

            q = '1 - the difficulty probability', this because the probability was defined as 'the probability
            of having a ladder', so in this case, the probability of having a snake is the opposite.

        For more information of the Binomial Distribution you can go to https://en.wikipedia.org/wiki/Binomial_distribution
                
        Args:
            board (Board)
            threshold (float)

        Returns:
            int
        """
        n = round(threshold * ((board.width + board.height) / 2))
        q = 1 - self.probability[self.difficulty]
        
        return binom.rvs(n, q)
        
    def get_n_ladders(self, board: Board, threshold: float = 0.9) -> int:
        """
        Function that determines the number of Ladders the game will have according to the Board width, 
        Board length, a threshold and the difficulty. At the end, the number of Ladders is determined by
        a Binomial Distribution where:

            n = The number of times we're going to make a Bernoulli trial (The Binomial distribution can be seen
            as making 'n' times the Bernoulli trial), this is determined by the average of the width and the 
            length of the Board multiplied by a threshold (To 'minimize' the maximum amount of Snakes and Ladders
            we'll have if we put a Snake and a Ladder for every number of row and column of the Board).

            p = 'the difficulty probability', this because the probability was defined as 'the probability
            of having a ladder'.

        For more information of the Binomial Distribution you can go to https://en.wikipedia.org/wiki/Binomial_distribution
                
        Args:
            board (Board)
            threshold (float)

        Returns:
            int
        """
        n = round(threshold * ((board.width + board.height) / 2))
        p = self.probability[self.difficulty]

        return binom.rvs(n, p)

    def get_bools(self, obj_pos: dict) -> bool:
        """
        Function that evaluates if the Cell that contains a new generated Snake/Ladder path already 
        has another Snake/Ladder, this to ensure we don't have more than 1 object in 1 Cell.

        Args:
            obj_pos (dict)

        Returns:
            Bool
        """
        s1 = self.cells[obj_pos['begin'][0]][obj_pos['begin'][1]].has_object == False
        s2 = self.cells[obj_pos['end'][0]][obj_pos['end'][1]].has_object == False

        return s1 and s2

    def get_snake_ladders(self, Obj: Snake or Ladder, n_objs: int,  x: int, y: int) -> list:
        """
        Function that generates the path of every Snake & Ladder according of the number of elements we'll 
        need of every type of object and the width and length of the Board.

        Args:
            Obj (Snake or Ladder)
            n_objs (int)
            x (int)
            y (int)

        Returns:
            list
        """
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
        """
        Function that changes the position and score of the player.

        Args:
            player (Player)
            move (int)

        Returns:
            None
        """
        player.change_pos(move, self.board.width, self.board.height)
        print(f'landed on {player.pos}')
        cell = self.cells[player.pos[0]][player.pos[1]]

        if cell.has_object:
            try:
                new_pos = cell.object.path
                print(new_pos)
                player.pos = new_pos['end']

                if type(cell) == Ladder:
                    player.change_score((move * 10) + 1)

                elif type(cell) == Snake:
                    player.change_score((move * 10) - 1)

            except:
                pass
        else:
            player.change_score(move * 10)

    def win_game(self, player:Player) -> bool:
        """
        Function that determines if a Player wins the game or not.

        Args:
            player (Player)

        Returns:
            bool
        """
        last_cell = self.cells[-1][-1]
        
        return player.pos == [last_cell.x, last_cell.y]

