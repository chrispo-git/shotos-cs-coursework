import os
import time
import sys
import run_game
import turtle
import keyboard
import image_reverser
import menu
from tkinter import PhotoImage
from turtle import Shape
import random

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 450
FRAME_LENGTH = 5.0
SCALE = 5

CHARACTER_AMOUNT = 3

image_reverser.reverse()

def update(turtle, controls,char_pos_x,char_pos_y) -> int:
    if keyboard.is_pressed(controls[0]) and not keyboard.is_pressed(controls[1]): #Similar logic to left/right in run_game.py
        turtle.goto(turtle.xcor()-2, turtle.ycor())

    if keyboard.is_pressed(controls[1]) and not keyboard.is_pressed(controls[0]):
        turtle.goto(turtle.xcor()+2, turtle.ycor())

    if keyboard.is_pressed(controls[2]) and not keyboard.is_pressed(controls[3]):
        turtle.goto(turtle.xcor(), turtle.ycor()+2)

    if keyboard.is_pressed(controls[3]) and not keyboard.is_pressed(controls[2]):
        turtle.goto(turtle.xcor(), turtle.ycor()-2)
    
    if keyboard.is_pressed(controls[5]): #Cancel button is the heavy button
        return None
    
    if keyboard.is_pressed(controls[4]): #Attack button is the light button
        x = turtle.xcor()
        y = turtle.ycor()
        for i in range(0, len(char_pos_x)):
            if abs(char_pos_x[i]-x) < 50 and abs(char_pos_y[i]-y) < 50:
                return i #returns char_id based on cursort pos when accept button is pressed
    
    return -1


def run(training_settings=[False,False,False,0,0], cpu=False):
    #Screen setup
    turtle.TurtleScreen._RUNNING=True
    screen = turtle.Screen()
    screen.setup(SCREEN_WIDTH, SCREEN_HEIGHT)
    screen.title("Shotos")
    screen.bgcolor("white")
    screen.clearscreen()
    for i in ["sprites", "reverse_sprites"]:
        for root, dirs, files in os.walk(i):
            #print(files)
            for filename in files:
                if filename.endswith(".gif"):
                    #print(filename)
                    #Handles scaling up and stuff
                    larger = PhotoImage(file=f"{i}/{filename}").zoom(SCALE, SCALE)
                    screen.addshape(f"{i}/{filename}", Shape("image", larger))
    for root, dirs, files in os.walk("menu"):
        for filename in files:
            if filename.endswith(".gif"):
                screen.addshape(f"menu/{filename}")
    screen.tracer(0)
    
    chosen_chars = [None,None]

    bg = turtle.Turtle()
    bg.penup()
    bg.shape(f"menu/css.gif")

    char_turtle = []
    char_pos_x = []
    char_pos_y = []
    for i in range(0,CHARACTER_AMOUNT):
        f = turtle.Turtle()
        f.penup()
        f.goto(-100 +((i/(CHARACTER_AMOUNT-1))*200), 25) #Programatically prints out their heads with equal spacing
        f.shape(f"sprites/F0{i}_Head.gif")
        char_turtle.append(f)
        char_pos_x.append(char_turtle[i].xcor())
        char_pos_y.append(char_turtle[i].ycor())
    screen.tracer(10)

    p1_show = turtle.Turtle()
    p1_show.penup()
    p1_show.goto(-200,-50)
    p1_show.hideturtle()

    p1_name = turtle.Turtle()
    p1_name.penup()
    p1_name.goto(-200,-200)
    p1_name.hideturtle()

    p2_show = turtle.Turtle()
    p2_show.penup()
    p2_show.goto(200,-50)
    p2_show.hideturtle()

    p2_name = turtle.Turtle()
    p2_name.penup()
    p2_name.goto(200,-200)
    p2_name.hideturtle()

    p1_cursor = turtle.Turtle()
    p1_cursor.penup()
    p1_cursor.goto(-100,-50)
    p1_cursor.shape("menu/P2_Cursor.gif")
    p2_cursor = turtle.Turtle()
    p2_cursor.penup()
    p2_cursor.goto(100,-50)
    p2_cursor.shape("menu/P1_Cursor.gif")

    controls = run_game.get_controls_from_txt()

    if cpu:
        rand_val = random.randint(0,CHARACTER_AMOUNT)
        chosen_chars[1] = rand_val
        p2_cursor.goto(char_pos_x[rand_val],char_pos_y[rand_val]-20)
    screen.update()
    prev_delay = 0
    while True:
            #try:
                if prev_delay > FRAME_LENGTH*2:
                    pass
                    #print("Frame Skip! Performance aint looking good")

                start = time.time()
                p1 = update(p1_cursor, controls[0], char_pos_x, char_pos_y)
                p2 = update(p2_cursor, controls[1], char_pos_x, char_pos_y)

                if p1 != -1:
                    chosen_chars[0] = p1
                if p2 != -1:
                    chosen_chars[1] = p2
                if chosen_chars[0] != None: #If they have a character selected, show that character
                    p1_show.showturtle()
                    p1_show.shape(f"sprites/F0{chosen_chars[0]}_Idle_0.gif") #We can do this because the sprites are properly named!
                    p1_name.showturtle()
                    p1_name.shape(f"menu/F0{chosen_chars[0]}_Name.gif")
                else:
                    p1_show.hideturtle()
                    p1_name.hideturtle()
                if chosen_chars[1] != None:
                    p2_show.showturtle()
                    p2_show.shape(f"reverse_sprites/F0{chosen_chars[1]}_Idle_0.gif")
                    p2_name.showturtle()
                    p2_name.shape(f"menu/F0{chosen_chars[1]}_Name.gif")
                else:
                    p2_show.hideturtle()
                    p2_name.hideturtle()
                if None not in chosen_chars:
                    screen.update()
                    cancel = True
                    for i in range(0,10):
                        time.sleep(0.1)
                        if keyboard.is_pressed(controls[0][5]) or keyboard.is_pressed(controls[1][5]):
                            cancel = False
                            break
                    if cancel:
                        break
                screen.update()
                if keyboard.is_pressed("escape"):
                    menu.run()
                end = time.time()
                new_delay = (end-start)*10**3
                #print(f"Time taken: {new_delay}ms, normalise: {FRAME_LENGTH - (new_delay)}ms")
                if (new_delay/1000) < FRAME_LENGTH/1000:
                    time.sleep(FRAME_LENGTH/1000 - (new_delay/1000))
                prev_delay = new_delay
            #except Exception as exc:
                #print(exc)
                #sys.exit()
    run_game.run(training_settings, chosen_chars, cpu)