from flask import Flask, render_template, request, redirect, url_for, globals
from flask.views import View

from .models import Board, Dice, Player, Game, Snake, Ladder, Cell

app = Flask(__name__)

#Global Vartiables ot indicate the minimum numbers
globals.num_users = 2
globals.board_x = 10
globals.board_y = 10
globals.turns = 10
globals.difficulty = 'Normal'
globals.current_turn = 1


@app.get('/')
def home():
    return render_template('home.html')

@app.post('/')
def data():
    globals.num_users = request.form['num_users']
    globals.board_x = request.form['board_width']
    globals.board_y = request.form['board_height']

    #Added by Diego T.
    globals.turns = request.form['num_turns']
    globals.difficulty = request.form['difficulty']

    print(request.form['num_users'], request.form['board_width'], request.form['board_height'], request.form['num_turns'], request.form['difficulty'])
    return redirect(url_for('board'))

@app.get('/board')
def board():
    return f'{globals.num_users} {globals.board_x} {globals.board_y} {globals.turns} {globals.difficulty}'

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
            
        globals.current_turn += 1

    else:
        print('The have have ended')

if __name__ == '__main__':
    app.run(Debug = True)