from flask import Flask, render_template, request, redirect, url_for, globals
from flask.views import View

from .models import Board, Dice, Player, Game, Snake, Ladder

app = Flask(__name__)

# min vals
globals.num_users = 2
globals.board_x = 1
globals.board_y = 3

@app.get('/')
def home():
    return render_template('home.html')

@app.post('/')
def data():
    globals.num_users = request.form['num_users']
    globals.board_x = request.form['board_width']
    globals.board_y = request.form['board_height']
    print(request.form['num_users'], request.form['board_width'], request.form['board_height'])
    return redirect(url_for('board'))

@app.get('/board')
def board():
    return f'{globals.num_users} {globals.board_x} {globals.board_y}'

if __name__ == '__main__':
    app.run(Debug=True)