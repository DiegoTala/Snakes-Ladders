from flask import Flask, render_template, request, redirect, url_for, globals
from flask.views import View
import random

from .models import Board, Dice, Player, Game, Snake, Ladder, Cell

app = Flask(__name__)

#Global Vartiables to indicate the minimum numbers
globals.num_users = 2
globals.board_x = 10
globals.board_y = 10
globals.turns = 10
globals.difficulty = 'Normal'
globals.current_turn = 1
globals.idxs = {}
globals.game = None
globals.player_check = 0

@app.get('/')
def home():
    return render_template('home.html')

@app.post('/')
def data():
    globals.num_users = int(request.form['num_users'])
    globals.board_x = int(request.form['board_width'])
    globals.board_y = int(request.form['board_height'])

    globals.turns = request.form['num_turns']
    globals.difficulty = request.form['difficulty']

    globals.idxs = {user+1:[0,0] for user in range(globals.num_users)}
    # globals.idxs[3] = [0,4]
    # globals.idxs[1] = [0,1]
    # globals.idxs[2] = [3,0]

    # game start with Game()

    print(request.form['num_users'], request.form['board_width'], request.form['board_height'], globals.idxs, globals.turns, globals.difficulty)
    return redirect(url_for('board'))

@app.get('/board')
def board():
    return render_template('board.html', board_x=globals.board_x, board_y=globals.board_y, num_users=globals.num_users, idxs=globals.idxs, game=create_game())

def create_game():
    players = [Player(x, f'Player {x}') for x in list(range(1, globals.num_users + 1))]
    print(players)
    dices = [Dice(), Dice()]
    board = Board(globals.board_x, globals.board_y)

    globals.game = Game(players = players, dices = dices, board = board, difficulty = globals.difficulty)

    print(globals.game.players)

    print(globals.game.snakes)
    print(globals.game.ladders)

    return globals.game

@app.post('/game')
def game():
    players = [Player(x, 'Name') for x in list(range(1, globals.num_users + 1))]
    dices = [Dice, Dice]
    board = Board(globals.board_x, globals.board_y)

    game = Game(players = players, dices = dices, board = board, difficulty = globals.difficulty)

    if globals.current_turn < globals.turns:
        for player in game.players:
            increase = game.roll_dices(dices = game.dices)
            game.change_player_pos_and_score(player, increase)
            
            if game.win_game(player):
                print(f'El jugador {player.name} ha ganado')

        globals.current_turn += 1

    else:
        print('The game have ended')
        max_score = max([player.score for player in game.players])
        winners = [player.name for player in game.players if player.score == max_score]
        print(f'El jugador(es) ganador(es) es(son){winners}')

    print(globals.board_x, globals.board_y)

# game logic

@app.get('/move_players')
def move_players():
    if globals.player_check >= globals.num_users:
        globals.current_turn += 1
        globals.player_check = 0

    player = globals.game.players[globals.player_check]
    increase = globals.game.roll_dices(dices = globals.game.dices)
    globals.game.change_player_pos_and_score(player, increase)
    print(player)

    globals.player_check += 1

    return {
        'id': player.id,
        'score': player.score,
        'pos': player.pos
    }

if __name__ == '__main__':
    app.run(Debug = True)