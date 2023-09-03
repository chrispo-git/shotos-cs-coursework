import os
import time
import sys
import run_game
import turtle
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 450

MAX_Y = -18
MIN_Y = -104
OFFLINE = [-330,-180]
ONLINE = [-170,-20]
TRAINING = [0,150]
SETTINGS = [160,310]

screen_instance = 0

def check_click_pos(x,y):
    if y < MIN_Y or y > MAX_Y:
        return 
    if x >= OFFLINE[0] and x <= OFFLINE[1]:
        try:
            run_game.run()
        except Exception:
            sys.exit()
    elif x >= ONLINE[0] and x <= ONLINE[1]:
        dummy = 0
    elif x >= TRAINING[0] and x <= TRAINING[1]:
        dummy = 0
    elif x >= SETTINGS[0] and x <= SETTINGS[1]:
        dummy = 0

def run(auto=False):
    turtle.TurtleScreen._RUNNING=True
    screen = turtle.Screen()
    screen.setup(SCREEN_WIDTH, SCREEN_HEIGHT)
    screen.title("Jumpsies")
    screen.bgcolor("white")
    screen.addshape("menu/main.gif")
    screen.clearscreen()
    if auto:
        try:
            run_game.run()
        except Exception:
            sys.exit()
    menuUI = turtle.Turtle()
    menuUI.shape("menu/main.gif")
    screen.onscreenclick(check_click_pos)
    screen.mainloop()
