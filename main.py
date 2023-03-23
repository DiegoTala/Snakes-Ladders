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
globals.idxs = {}

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
    
    globals.idxs = {user+1:[0,0] for user in range(globals.num_users)}
    globals.idxs[1] = [0,1]
    globals.idxs[2] = [3,0]
    print(request.form['num_users'], request.form['board_width'], request.form['board_height'], globals.idxs)
    return redirect(url_for('board'))

@app.get('/board')
def board():
    return render_template('board.html', board_x=globals.board_x, board_y=globals.board_y, num_users=globals.num_users, idxs=globals.idxs)

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
    print(globals.board_x, globals.board_y)

if __name__ == '__main__':
    app.run(Debug = True)