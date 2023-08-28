import turtle
import os
import time
import keyboard
from tkinter import PhotoImage
from turtle import Shape
from PIL import Image, ImageTk
import image_reverser

image_reverser.reverse()

#CONSTANTS
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 450
BOX_SIZE = [640, 360]


#Character constants
WALK_SPEED = 12.0
SCALE = 5

ANIMATION_LIST = [
    
    [ #Idle
        ["sprites/Idle_0.gif", [18,41,0,36], None],
        ["sprites/Idle_0.gif", [18,41,0,36], None],
        ["sprites/Idle_1.gif", [18,41,0,36], None],
        ["sprites/Idle_2.gif", [18,41,0,36], None],
        ["sprites/Idle_2.gif", [18,41,0,36], None],
        ["sprites/Idle_3.gif", [18,41,0,36], None],
        ["sprites/Idle_4.gif", [18,41,0,36], None]
    ],
    [ #WalkF
        ["sprites/F00_Forward_0.gif", [18,41,0,36], None],
        ["sprites/F00_Forward_1.gif", [18,41,0,36], None],
        ["sprites/F00_Forward_2.gif", [18,41,0,36], None],
        ["sprites/F00_Forward_3.gif", [18,41,0,36], None],
        ["sprites/F00_Forward_4.gif", [18,41,0,36], None],
        ["sprites/F00_Forward_5.gif", [18,41,0,36], None]
    ],
]

#Format for Frames= ["sprites/frame.gif", [hurtbox x1, hurtbox x2, hurtbox y1, hurtbox y2], [hitbox x1, hitbox x2, hitbox y1, hitbox y2]]


ANIMATION_LIST_LABEL = [
    "Idle",
    "WalkF",
    "WalkB"
]
def get_anim_ID(name: str) -> int:
        try:
            value = ANIMATION_LIST_LABEL.index(name)
            return value
        except ValueError:
            return -1
        

screen = turtle.Screen()
screen.setup(SCREEN_WIDTH, SCREEN_HEIGHT)
screen.bgcolor("white")
for i in ["sprites", "reverse_sprites"]:
    for root, dirs, files in os.walk(i):
        print(files)
        for filename in files:
            if filename.endswith(".gif"):
                print(filename)
                #Handles scaling up and stuff
                larger = PhotoImage(file=f"{i}/{filename}").zoom(SCALE, SCALE)
                screen.addshape(f"{i}/{filename}", Shape("image", larger))
#print(screen.getshapes())

class player:
    def __init__(self, 
        playerNum: int,
        x: int, y: int,
        #sprite, frame, animList,
        controls: list, #Controls expressed as [left, right, up, down, attack, special]
        Left: bool
    ):
        self.playerNum = playerNum
        self.x = x
        self.y = y
        self.isJump = False
        self.Left = Left
        self.moveXThisFrame = 0.0
        self.moveYThisFrame = 0.0

        #Sprite Init
        self.frame = 0
        self.animListID = 0
        self.sprite = "sprites/Idle_0.gif"

        #Turtle Setup
        
        self.turtle = turtle.Turtle()
        self.turtle.speed(0)
        self.turtle.penup()
        self.turtle.goto(x, y)
        self.turtle.shape(self.sprite)
        self.animate()

        self.controls = controls

    def animate(self):
        anim = ANIMATION_LIST[self.animListID]
        anim_length = len(anim)
        sprite = anim[self.frame][0]
        if self.Left == True:
            sprite = sprite.replace("sprites", "reverse_sprites")
        self.sprite = sprite
        #print(self.sprite)
        self.turtle.shape(self.sprite)
        #print(self.turtle.shape())
        
        if self.frame+1 >= anim_length:
            self.frame = 0
            if self.isJump == False:
                self.set_new_anim_by_ID()
        else:
            self.frame += 1

    
    
    def set_new_anim_by_ID(self, id=0, frame=0):
        if id == -1:
            return
        self.frame = frame
        self.animListID = id


    
    def right(self):
        #print(f"[{self.x}, {self.y}]")
        if self.isJump == False:
            self.moveXThisFrame = WALK_SPEED
            if self.animListID in [get_anim_ID("Idle"), get_anim_ID("WalkB")]:
                self.set_new_anim_by_ID(get_anim_ID("WalkF"))
            if self.animListID == get_anim_ID("WalkF") and self.frame >= len(ANIMATION_LIST[self.animListID])-1:
                self.set_new_anim_by_ID(get_anim_ID("WalkF"))


    def left(self):
        if self.isJump == False:
            self.moveXThisFrame = -WALK_SPEED
    
    def update(self):
            self.animate()


            if keyboard.is_pressed(self.controls[0]):
                self.left()
            elif (self.animListID == get_anim_ID("WalkF") and self.Left == True) or (self.animListID == get_anim_ID("WalkB") and self.Left == False):
                self.set_new_anim_by_ID()


            if keyboard.is_pressed(self.controls[1]):
                self.right()
            elif (self.animListID == get_anim_ID("WalkF") and self.Left == False) or (self.animListID == get_anim_ID("WalkB") and self.Left == True):
                self.set_new_anim_by_ID()


            if self.moveXThisFrame != 0 or self.moveYThisFrame != 0:
                newXVal = 0
                newYVal = 0
                x = self.x
                y = self.y
                if abs(x+self.moveXThisFrame) < BOX_SIZE[0]:
                    newXVal = x+self.moveXThisFrame
                    self.turtle.goto(newXVal, newYVal)
                if abs(y+self.moveXThisFrame) < BOX_SIZE[0]:
                    newYVal = y+self.moveYThisFrame
                #print(f"{newXVal}, {newYVal}")
                self.x = newXVal
                self.y = newYVal
                self.turtle.setpos(self.x, self.y)
                self.moveXThisFrame = 0.0
                self.moveYThisFrame = 0.0

def init_controls(players: list):
    for i in players:
        screen.onkey(i.left(), i.controls[0])
        screen.onkey(i.right(), i.controls[1])



p1 = player(
    1,
    -150, 0,
    ["a", "d", "w", "s", "f", "g"],
    False
)
p2 = player(
    1,
    150, 0,
    ["j", "l", "k", "i", ";", "'"],
    True
)
while True:
    p1.update()
    p2.update()
    time.sleep(1.0/60.0)
screen.mainloop()