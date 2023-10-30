import os
import time
import sys
import run_game
import turtle
import keyboard
import css
from util import get_controls_from_txt
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 450

MAX_Y = -18
MIN_Y = -104
P2 = [-330,-180]
CPU = [-170,-20]
TRAINING = [0,150]
SETTINGS = [160,310]
VALID_KEYS = [
    "a", "b", "c", "d", "e", "f", "g",
    "h", "i", "j", "k", "l", "m", "n",
    "o", "p", "q", "r", "s", "t", "u",
    "v", "w", "x", "y", "z", "right", "left",
    "up", "down", "shift", "/", ".", ","
]

screen_instance = 0
is_controls = False

def check_click_pos(x,y):
    global is_controls
    global screen_instance
    if not is_controls:
        if y < MIN_Y or y > MAX_Y: #If outside of the Y area where you'd click buttons just dont run this
            return 
        if x >= P2[0] and x <= P2[1]: #Checks if your X value is in the button area, no need to check Y as its already done above
            try:
                css.run([False,False,False,0,0]) #Runs the CSS with arguments that the CSS will pass onto the run_game module
            except Exception:
                sys.exit() #Closes the game on errors so that it doesnt hang 
        elif x >= CPU[0] and x <= CPU[1]:
            try:
                css.run([False,False,False,0,0],True)
            except Exception:
                sys.exit()
        elif x >= TRAINING[0] and x <= TRAINING[1]:
            try:
                css.run([True,True,False,0,0])
            except Exception:
                sys.exit()
        elif x >= SETTINGS[0] and x <= SETTINGS[1]:
            is_controls = True
            run_settings_screen()
    else: #If you're in controls, changes your on click behaviour
        if x > 300 or x < -300 or y < -195 or y > 195:
            run() #Leaves controls
        if y < 85 or y > 135: #If not at the controls button height ignore
            return 
        if x < -70 and x > -250: #Player 1 controls
            update_controls(0)
        if x < 250 and x > 70: #P2 controls
            update_controls(1)


def update_controls(player):
    global screen_instance
    controls = get_controls_from_txt()
    new_control_set = controls[player]
    printer = turtle.Turtle()
    screen_instance.update()
    screen_instance.tracer(10)
    printer.showturtle()
    #Goes through each key and gets your binding for it
    keylist = VALID_KEYS
    printer.shape("menu/presskey_left.gif")
    screen_instance.update()
    button = wait_till_button(keylist)
    keylist.remove(button)
    new_control_set[0] = button
    printer.shape("menu/presskey_right.gif")
    screen_instance.update()
    button = wait_till_button(keylist)
    keylist.remove(button)
    new_control_set[1] = button
    printer.shape("menu/presskey_up.gif")
    screen_instance.update()
    button = wait_till_button(keylist)
    keylist.remove(button)
    new_control_set[2] = button
    printer.shape("menu/presskey_down.gif")
    screen_instance.update()
    button = wait_till_button(keylist)
    keylist.remove(button)
    new_control_set[3] = button
    printer.shape("menu/presskey_light.gif")
    screen_instance.update()
    button = wait_till_button(keylist)
    keylist.remove(button)
    new_control_set[4] = button
    printer.shape("menu/presskey_heavy.gif")
    screen_instance.update()
    button = wait_till_button(keylist)
    keylist.remove(button)
    new_control_set[5] = button
    printer.shape("menu/presskey_special.gif")
    screen_instance.update()
    button = wait_till_button(keylist)
    keylist.remove(button)
    new_control_set[6] = button

    controls[player] = new_control_set
    f = open("controls.txt","w")
    f.write("")
    f.close()
    f = open("controls.txt","a")
    f.write(" ".join(controls[0]) + "\n")
    f.write(" ".join(controls[1]))
    f.close()
    printer.hideturtle()
    run_settings_screen()

def wait_till_button(key_set):
    global screen_instance
    while True:
        for i in key_set:
            if keyboard.is_pressed(i):
                return i
        screen_instance.update() #Screen must continually be updated to prevent turtle freezing!
        time.sleep(0.2)



def run_settings_screen():
    global is_controls
    global screen_instance
    controls = get_controls_from_txt()
    screen_instance.clearscreen()
    screen_instance.tracer(0)
    menuUI = turtle.Turtle()
    menuUI.shape("menu/main.gif")
    controlsUI = turtle.Turtle()
    controlsUI.shape("menu/controls_menu.gif")
    printer = turtle.Turtle()
    printer.penup()
    printer.goto(-70, 55)
    for i in controls[0]:
        file = i
        file = file.replace(",", "comma")
        file = file.replace(".", "dot")
        file = file.replace("/", "fslash")
        file = file.replace("UP", "up")
        file = file.replace("RIGHT", "right")
        file = file.replace("Down", "down")
        file = file.replace("LEFT", "left")
        file = file.replace("SHIFT", "shift")
        printer.shape(f"text/{file}.gif")
        printer.stamp()
        printer.goto(-70, printer.ycor() - 33)
    printer.goto(200, 55)
    for i in controls[1]:
        file = i
        file = file.replace(",", "comma")
        file = file.replace(".", "dot")
        file = file.replace("/", "fslash")
        file = file.replace("UP", "up")
        file = file.replace("RIGHT", "right")
        file = file.replace("Down", "down")
        file = file.replace("LEFT", "left")
        file = file.replace("SHIFT", "shift")
        printer.shape(f"text/{file}.gif")
        printer.stamp()
        printer.goto(200, printer.ycor() - 33)
    
    printer.goto(200, -500)
    screen_instance.update()
    screen_instance.tracer(10)
    screen_instance.onscreenclick(check_click_pos)
    screen_instance.mainloop()


def run(auto=False,chars=[],cpu=False):
    global is_controls
    global screen_instance
    is_controls = False
    turtle.TurtleScreen._RUNNING=True
    screen = turtle.Screen()
    screen_instance = screen
    screen.setup(SCREEN_WIDTH, SCREEN_HEIGHT)
    screen.title("Shotos")
    screen.bgcolor("white")
    for root, dirs, files in os.walk("menu"):
        for filename in files:
            if filename.endswith(".gif"):
                screen.addshape(f"menu/{filename}")
    for root, dirs, files in os.walk("text"):
        for filename in files:
            if filename.endswith(".gif"):
                screen.addshape(f"text/{filename}")
    screen.clearscreen()
    if auto:
        try:
            run_game.run([False,False,False,0,0], chars, cpu)
        except Exception:
            sys.exit()
    menuUI = turtle.Turtle()
    menuUI.shape("menu/main.gif")
    screen.onscreenclick(check_click_pos)
    screen.mainloop()
