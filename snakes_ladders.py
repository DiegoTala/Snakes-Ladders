############################
####### Dependencies #######
############################
#Arrays & data managing libraries
import pandas as pd
import numpy as np

#Various libraries 
import os, re
import datetime

from functools import reduce

#Functions for the web app
from flask import Flask
from flask import render_template, url_for
from flask import request, redirect

#######################
####### Classes #######
#######################

class Dice():
    def ___init__(self, x:str):
        self.x = 'x'

class Player():
    def ___init__(self, x:str):
        self.x = 'x'
    
    def __repr__(self) -> str:
        return '<Task %r>' % self.id

class Snake_Ladder():
    def ___init__(self, x:str):
        self.x = 'x'

class Box():
    def ___init__(self, x:str):
        self.x = 'x'   

class Board():
    def ___init__(self, x:str):
        self.x = 'x' 

class Game():
    def ___init__(self, x:str):
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
    return 'Hello There!'

if __name__ == "__main__":
    app.run(debug = True)