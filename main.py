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
BOX_SIZE = [330, 360]
FRAME_LENGTH = 60.0


#Character constants
WALK_SPEED = 12.0
SCALE = 5

ANIMATION_LIST = [
    
    [ #Idle
        ["sprites/Idle_0.gif", [-11.5,11.5,-25,14], None],
        ["sprites/Idle_0.gif", [-11.5,11.5,-25,14], None],
        ["sprites/Idle_1.gif", [-11.5,11.5,-25,14], None],
        ["sprites/Idle_2.gif", [-11.5,11.5,-25,14], None],
        ["sprites/Idle_2.gif", [-11.5,11.5,-25,14], None],
        ["sprites/Idle_3.gif", [-11.5,11.5,-25,14], None],
        ["sprites/Idle_4.gif", [-11.5,11.5,-25,14], None]
    ],
    [ #WalkF
        ["sprites/F00_Forward_0.gif", [-11.5,11.5,-25,14], None],
        ["sprites/F00_Forward_1.gif", [-11.5,11.5,-25,14], None],
        ["sprites/F00_Forward_2.gif", [-11.5,11.5,-25,14], None],
        ["sprites/F00_Forward_3.gif", [-11.5,11.5,-25,14], None],
        ["sprites/F00_Forward_4.gif", [-11.5,11.5,-25,14], None],
        ["sprites/F00_Forward_5.gif", [-11.5,11.5,-25,14], None]
    ],
    [ #WalkB
        ["sprites/F00_Backward_0.gif", [-11.5,11.5,-25,14], None],
        ["sprites/F00_Backward_1.gif", [-11.5,11.5,-25,14], None],
        ["sprites/F00_Backward_2.gif", [-11.5,11.5,-25,14], None],
        ["sprites/F00_Backward_3.gif", [-11.5,11.5,-25,14], None],
        ["sprites/F00_Backward_4.gif", [-11.5,11.5,-25,14], None],
        ["sprites/F00_Backward_5.gif", [-11.5,11.5,-25,14], None]
    ],
    [ #Crouch
        ["sprites/F00_Crouch_0.gif", [-11.5,11.5,-25,2], None],
        ["sprites/F00_Crouch_0.gif", [-11.5,11.5,-25,2], None],
        ["sprites/F00_Crouch_1.gif", [-11.5,11.5,-25,2], None]
    ],
    [ #CrouchWait
        ["sprites/F00_CrouchWait_0.gif", [-11.5,11.5,-25,2], None],
        ["sprites/F00_CrouchWait_0.gif", [-11.5,11.5,-25,2], None],
    ]
]

#Format for Frames= ["sprites/frame.gif", [hurtbox x1, hurtbox x2, hurtbox y1, hurtbox y2], [hitbox x1, hitbox x2, hitbox y1, hitbox y2, hitbox damage]]


ANIMATION_LIST_LABEL = [
    "Idle",
    "WalkF",
    "WalkB",
    "Crouch",
    "CrouchWait"
]

#Collisions!
PUSHBOXES = [11.5,-25,14]
char_pos = [[0,0], [0,0]]
hurtbox = []

def get_anim_ID(name: str) -> int:
        global ANIMATION_LIST_LABEL
        try:
            value = ANIMATION_LIST_LABEL.index(name)
            return value
        except ValueError:
            return -1
        

screen = turtle.Screen()
screen.setup(SCREEN_WIDTH, SCREEN_HEIGHT)
screen.bgcolor("white")
#screen.delay(17)
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
        self.isHitstun = False
        self.is_left = Left
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
        global ANIMATION_LIST
        anim = ANIMATION_LIST[self.animListID]
        anim_length = len(anim)
        sprite = anim[self.frame][0]
        if self.is_left == True:
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
        global ANIMATION_LIST
        global WALK_SPEED
        #print(f"[{self.x}, {self.y}]")
        if self.isJump == False:
            self.moveXThisFrame = WALK_SPEED
            if self.is_left == False: #If facing left
                if self.animListID in [get_anim_ID("Idle"), get_anim_ID("WalkB")]:
                    self.set_new_anim_by_ID(get_anim_ID("WalkF"))
                if self.animListID == get_anim_ID("WalkF") and self.frame >= len(ANIMATION_LIST[self.animListID])-1:
                    self.set_new_anim_by_ID(get_anim_ID("WalkF"))
            else:
                if self.animListID in [get_anim_ID("Idle"), get_anim_ID("WalkF")]:
                    self.set_new_anim_by_ID(get_anim_ID("WalkB"))
                if self.animListID == get_anim_ID("WalkB") and self.frame >= len(ANIMATION_LIST[self.animListID])-1:
                    self.set_new_anim_by_ID(get_anim_ID("WalkB"))


    def left(self):
        global ANIMATION_LIST
        global WALK_SPEED
        if self.isJump == False:
            self.moveXThisFrame = -WALK_SPEED
            if self.is_left == True: #If facing left
                if self.animListID in [get_anim_ID("Idle"), get_anim_ID("WalkB")]:
                    self.set_new_anim_by_ID(get_anim_ID("WalkF"))
                if self.animListID == get_anim_ID("WalkF") and self.frame >= len(ANIMATION_LIST[self.animListID])-1:
                    self.set_new_anim_by_ID(get_anim_ID("WalkF"))
            else:
                if self.animListID in [get_anim_ID("Idle"), get_anim_ID("WalkF")]:
                    self.set_new_anim_by_ID(get_anim_ID("WalkB"))
                if self.animListID == get_anim_ID("WalkB") and self.frame >= len(ANIMATION_LIST[self.animListID])-1:
                    self.set_new_anim_by_ID(get_anim_ID("WalkB"))
    
    def check_correct_side(self):
        global ANIMATION_LIST
        global PUSHBOXES
        #print(f"[{self.x}, {self.y}]")
        if self.isJump == False:
            if self.is_left == True and self.x < char_pos[-(self.playerNum)][0]:
                self.is_left = False
                self.set_new_anim_by_ID()
            if self.is_left == False and self.x > char_pos[-(self.playerNum)][0]:
                self.is_left = True
                self.set_new_anim_by_ID()
    
    def update(self):
            global PUSHBOXES

            self.check_correct_side()
            self.animate()

            if keyboard.is_pressed(self.controls[0]):
                self.left()
            elif (self.animListID == get_anim_ID("WalkF") and self.is_left != False) or (self.animListID == get_anim_ID("WalkB") and self.is_left != True):
                self.set_new_anim_by_ID()


            if keyboard.is_pressed(self.controls[1]):
                self.right()
            elif (self.animListID == get_anim_ID("WalkF") and self.is_left != True) or (self.animListID == get_anim_ID("WalkB") and self.is_left != False):
                self.set_new_anim_by_ID()


            if self.moveXThisFrame != 0 or self.moveYThisFrame != 0:
                x = self.x
                y = self.y
                newXVal = x
                newYVal = y
                if abs(x+self.moveXThisFrame) < BOX_SIZE[0]:
                    newXVal = x+self.moveXThisFrame
                if y+self.moveXThisFrame >= 0:
                    newYVal = y+self.moveYThisFrame
                #print(f"{newXVal}, {newYVal}")

                #Pushbox
                left_pushbox = (char_pos[-(self.playerNum)][0] - PUSHBOXES[0]) - self.x  < 105 and self.is_left == False
                right_pushbox = self.x - (char_pos[-(self.playerNum)][0] + PUSHBOXES[0])  < 105 and self.is_left
                top_pushbox = self.y - (char_pos[-(self.playerNum)][1] + PUSHBOXES[2])  < 105
                bottom_pushbox =  (char_pos[-(self.playerNum)][1] + PUSHBOXES[1]) - self.y  < 105
                if top_pushbox and bottom_pushbox:
                    print(f"same height: [{(char_pos[-(self.playerNum)][0] - PUSHBOXES[0]) - self.x}, {self.x - (char_pos[-(self.playerNum)][0] + PUSHBOXES[0])}]")
                    print(f"X Pos for other one: {char_pos[-(self.playerNum)][0]}")
                if (left_pushbox or right_pushbox) and (top_pushbox and bottom_pushbox):
                    print("pushing!")
                    if (self.moveXThisFrame > 0 and left_pushbox) or (self.moveXThisFrame < 0 and right_pushbox):
                        newXVal = x
                    

                self.x = newXVal
                self.y = newYVal
                self.turtle.setpos(self.x, self.y)
                self.moveXThisFrame = 0.0
                self.moveYThisFrame = 0.0

            char_pos[self.playerNum - 1][0] = self.x 
            char_pos[self.playerNum - 1][1] = self.y 
            #print(char_pos)

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
    2,
    150, 0,
    ["j", "l", "k", "i", ";", "'"],
    False
)
prev_delay = 0.0
while True:
    if prev_delay > FRAME_LENGTH*2:
        pass
        print("Frame Skip! Performance aint looking good")
    start = time.time()
    p1.update()
    p2.update()
    end = time.time()
    new_delay = (end-start)*10**3
    #print(f"Time taken: {new_delay}ms, normalise: {FRAME_LENGTH - (new_delay)}ms")
    if (new_delay/1000) < FRAME_LENGTH/1000:
        time.sleep(FRAME_LENGTH/1000 - (new_delay/1000))
    prev_delay = new_delay
screen.mainloop()