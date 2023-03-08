############################
####### Dependencies #######
############################
#Arrays & data managing libraries
import pandas as pd
import numpy as np

#Various libraries 
import os, re
import datetime
import random

from functools import reduce

#Functions for the web app
from flask import Flask
from flask import render_template, url_for
from flask import request, redirect

#######################
####### Classes #######
#######################

class Dice:
    def __init__(self, size:int):
        self.size = size

    def roll(self) -> int:
        return random.choice(np.arange(1, self.size + 1))

class Player:
    def __init__(self, id:int, name:str, position:int = 0, score:int = 0):
        self.id = id
        self.name = name
        self.position = position
        self.score = score

    def change_position(self, change: int) -> None:
        self.position += change

    def change_score(self, change: int) -> None:
        self.score += change

    def __repr__(self) -> str:
        return f'Player {self.id}: {self.name} - Position: {self.position} - Score: {self.score}'

class Snake_Ladder:
    def __init__(self, type:str, start: int, end: int):
        self.type = type
        self.start = start
        self.end = end

class Box:
    def __init__(self, has_snake_ladder: bool, has_special_event: bool):
        self.has_snake_ladder = has_snake_ladder
        self.has_special_event = has_special_event

class Board:
    def __init__(self, num_boxes:int, length: int, width: int):
        self.num_boxes = num_boxes
        self.length = length
        self.width = width

class Game():
    def __init__(self, x:str):
        self.x = 'x'

####################
####### Game #######
####################




#######################
####### Web App #######
#######################
#Creating the Flask object
app = Flask(__name__)

@app.route('/')
def index():
     return render_template('index.html')

if __name__ == "__main__":
    app.run(debug = True)