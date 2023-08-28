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
SCALE = 5

WALK_SPEED = 12.0

JUMP_DURATION_MUL = 1.5
JUMP_INITAL = 20.0*JUMP_DURATION_MUL
GRAVITY = 2.0*JUMP_DURATION_MUL
MAX_FALL = 20.0*JUMP_DURATION_MUL
AIR_MOVE = 10.0*JUMP_DURATION_MUL

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
        ["sprites/F00_Crouch_1.gif", [-11.5,11.5,-25,2], None]
    ],
    [ #CrouchWait
        ["sprites/F00_CrouchWait_0.gif", [-11.5,11.5,-25,2], None],
        ["sprites/F00_CrouchWait_0.gif", [-11.5,11.5,-25,2], None],
        ["sprites/F00_CrouchWait_0.gif", [-11.5,11.5,-25,2], None],
        ["sprites/F00_CrouchWait_0.gif", [-11.5,11.5,-25,2], None],
        ["sprites/F00_CrouchWait_1.gif", [-11.5,11.5,-25,2], None],
        ["sprites/F00_CrouchWait_1.gif", [-11.5,11.5,-25,2], None],
        ["sprites/F00_CrouchWait_1.gif", [-11.5,11.5,-25,2], None],
        ["sprites/F00_CrouchWait_1.gif", [-11.5,11.5,-25,2], None]
    ],
    [ #CrouchRv
        ["sprites/F00_Crouch_1.gif", [-11.5,11.5,-25,2], None],
        ["sprites/F00_Crouch_0.gif", [-11.5,11.5,-25,14], None],
        ["sprites/Idle_0.gif", [-11.5,11.5,-25,14], None]
    ],
    [ #JumpSquat
        ["sprites/F00_JumpSquat_0.gif", [-11.5,11.5,-25,14], None],
        ["sprites/F00_JumpSquat_0.gif", [-11.5,11.5,-25,14], None]
    ],
    [ #Air
        ["sprites/F00_Air_0.gif", [-11.5,11.5,-25,14], None],
        ["sprites/F00_Air_0.gif", [-11.5,11.5,-25,14], None],
        ["sprites/F00_Air_1.gif", [-11.5,11.5,-25,14], None],
        ["sprites/F00_Air_2.gif", [-11.5,11.5,-25,14], None],
        ["sprites/F00_Air_2.gif", [-11.5,11.5,-25,14], None],
        ["sprites/F00_Air_1.gif", [-11.5,11.5,-25,14], None]
    ]
]

#Format for Frames= ["sprites/frame.gif", [hurtbox x1, hurtbox x2, hurtbox y1, hurtbox y2], [hitbox x1, hitbox x2, hitbox y1, hitbox y2, hitbox damage]]

def get_anim_ID(name: str) -> int:
        global ANIMATION_LIST_LABEL
        try:
            value = ANIMATION_LIST_LABEL.index(name)
            return value
        except ValueError:
            return -1

ANIMATION_LIST_LABEL = [
    "Idle",
    "WalkF",
    "WalkB",
    "Crouch",
    "CrouchWait",
    "CrouchRv",
    "JumpSquat",
    "Air"
]

ACTIONABLE_LIST = [
    get_anim_ID("Idle"), get_anim_ID("WalkF"), get_anim_ID("WalkB"), 
    get_anim_ID("Crouch"), get_anim_ID("CrouchWait"), get_anim_ID("CrouchRv")
]

#Collisions!
PUSHBOXES = [11.5,-25,14]
PUSHING_FORCE = 5
char_pos = [[0,0], [0,0]]
hurtbox = []

        

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
        self.isHitstun = False
        self.is_left = Left
        self.isCrouch = False
        self.moveXThisFrame = 0.0
        self.moveYThisFrame = 0.0

        #Sprite Init
        self.frame = 0
        self.animListID = 0
        self.sprite = "sprites/Idle_0.gif"

        #Jump Attributes
        self.isJump = False
        self.lastmoveY = 0.0
        self.lastmoveX = 0.0
        self.lastmoveX = 0.0
        self.jumpDir = 0.0 #-1.0 is back, 0.0 is neutral, 1.0 is forwards

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
        global JUMP_INITAL
        anim = ANIMATION_LIST[self.animListID]
        anim_length = len(anim)
        sprite = anim[self.frame][0]
        if self.is_left == True:
            sprite = sprite.replace("sprites", "reverse_sprites")
        self.sprite = sprite
        #print(self.sprite)
        self.turtle.shape(self.sprite)
        #print(self.turtle.shape())
        
        if self.frame+1 >= anim_length: #Returns to default anim for state
            self.frame = 0
            self.set_new_anim_by_ID()
        else:
            self.frame += 1

    
    
    def set_new_anim_by_ID(self, id=-2, frame=0):
        if id == -1:
            return
        if id == -2:
            self.frame = frame
            if self.isJump:
                if self.animListID == get_anim_ID("JumpSquat"):
                    self.moveYThisFrame = JUMP_INITAL
                self.animListID = get_anim_ID("Air")
                return
            elif self.isCrouch:
                    self.animListID = get_anim_ID("CrouchWait")
                    return
            else:
                    self.animListID = get_anim_ID("Idle")
                    return
        self.frame = frame
        self.animListID = id


    
    def right(self):
        global ANIMATION_LIST
        global WALK_SPEED
        #print(f"[{self.x}, {self.y}]")
        if self.isJump == False:
            if self.animListID in [get_anim_ID("Idle"), get_anim_ID("WalkF"), get_anim_ID("WalkB")]:
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
            if self.animListID in [get_anim_ID("Idle"), get_anim_ID("WalkF"), get_anim_ID("WalkB")]:
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
                    
    def down(self):
        global ANIMATION_LIST
        #print(f"[{self.x}, {self.y}]")
        if self.isJump == False:
            if self.isCrouch == False and self.animListID in [get_anim_ID("Idle"), get_anim_ID("WalkF"), get_anim_ID("WalkB")]:
                self.isCrouch = True
                self.set_new_anim_by_ID(get_anim_ID("Crouch"))

                
    def uncrouch(self):
        global ANIMATION_LIST
        #print(f"[{self.x}, {self.y}]")
        if self.isCrouch == True and self.animListID in [get_anim_ID("CrouchWait")]:
                self.isCrouch = False
                self.set_new_anim_by_ID(get_anim_ID("CrouchRv"))

                
    def up(self):
        global ANIMATION_LIST
        #print(f"[{self.x}, {self.y}]")
        if self.isJump == False:
            if self.animListID in [get_anim_ID("Idle"), get_anim_ID("WalkF"), get_anim_ID("WalkB")]:
                self.isJump = True
                self.set_new_anim_by_ID(get_anim_ID("JumpSquat"))
    
    def air(self):
        global ANIMATION_LIST
        global JUMP_INITAL
        global GRAVITY
        global MAX_FALL
        global AIR_MOVE
        #print(f"[{self.x}, {self.y}]")
        if self.isJump == True:
            if self.y <= 0.0 and self.lastmoveY < 0.0:
                self.isJump = False
                if self.y < 0.0:
                    self.moveYThisFrame = -self.y
                self.set_new_anim_by_ID()
            else:
                if self.animListID == get_anim_ID("JumpSquat"):
                    if keyboard.is_pressed(self.controls[0]) and not keyboard.is_pressed(self.controls[1]):
                        self.jumpDir = 1.0
                    elif keyboard.is_pressed(self.controls[1]) and not keyboard.is_pressed(self.controls[0]):
                        self.jumpDir = -1.0
                    else:
                        self.jumpDir = 0.0
                else:
                    self.moveYThisFrame = self.lastmoveY - GRAVITY
                    self.moveXThisFrame = self.jumpDir * AIR_MOVE * -1.0

    
    def check_correct_side(self):
        global ANIMATION_LIST
        global ACTIONABLE_LIST
        #print(f"[{self.x}, {self.y}]")
        if self.isJump == False and self.animListID in ACTIONABLE_LIST:
            if self.is_left == True and self.x < char_pos[-(self.playerNum)][0]:
                self.is_left = False
                self.set_new_anim_by_ID()
            if self.is_left == False and self.x > char_pos[-(self.playerNum)][0]:
                self.is_left = True
                self.set_new_anim_by_ID()
    
    def update(self):
            global PUSHBOXES
            global PUSHING_FORCE

            self.check_correct_side()
            self.air()
            self.animate()

            if keyboard.is_pressed(self.controls[0]) and not keyboard.is_pressed(self.controls[1]):
                self.left()
            elif (self.animListID == get_anim_ID("WalkF") and self.is_left != False) or (self.animListID == get_anim_ID("WalkB") and self.is_left != True):
                self.set_new_anim_by_ID()


            if keyboard.is_pressed(self.controls[1]) and not keyboard.is_pressed(self.controls[0]):
                self.right()
            elif (self.animListID == get_anim_ID("WalkF") and self.is_left != True) or (self.animListID == get_anim_ID("WalkB") and self.is_left != False):
                self.set_new_anim_by_ID()

                
            if keyboard.is_pressed(self.controls[3]) and not keyboard.is_pressed(self.controls[2]):
                self.down()
            elif self.isCrouch:
                self.uncrouch()
            if keyboard.is_pressed(self.controls[2]) and not keyboard.is_pressed(self.controls[3]):
                self.up()


            if True:#self.moveXThisFrame != 0 or self.moveYThisFrame != 0:
                x = self.x
                y = self.y
                newXVal = x
                newYVal = y
                #print(f"{newXVal}, {newYVal}")

                #Forces players to stay within fighting area
                if abs(x+self.moveXThisFrame) < BOX_SIZE[0]:
                    newXVal = x+self.moveXThisFrame
                if y+self.moveXThisFrame >= 0:
                    newYVal = y+self.moveYThisFrame

                #Pushbox
                left_pushbox = (char_pos[-(self.playerNum)][0] - PUSHBOXES[0]) - self.x  < 105 and self.is_left == False
                right_pushbox = self.x - (char_pos[-(self.playerNum)][0] + PUSHBOXES[0])  < 105 and self.is_left
                top_pushbox = self.y - (char_pos[-(self.playerNum)][1] + PUSHBOXES[2])  < 55
                bottom_pushbox =  (char_pos[-(self.playerNum)][1] + PUSHBOXES[1]) - self.y  < 105
                #if top_pushbox and bottom_pushbox:
                    #print(f"same height: [{(char_pos[-(self.playerNum)][0] - PUSHBOXES[0]) - self.x}, {self.x - (char_pos[-(self.playerNum)][0] + PUSHBOXES[0])}]")
                    #print(f"X Pos for other one: {char_pos[-(self.playerNum)][0]}")
                if (left_pushbox or right_pushbox) and (top_pushbox and bottom_pushbox):
                    #print("pushing!")
                    if ((self.moveXThisFrame > 0 and left_pushbox) or (self.moveXThisFrame < 0 and right_pushbox)):
                        newXVal = x

                    if (abs(char_pos[0][0]- char_pos[1][0]) < 104):
                        push_off = PUSHING_FORCE
                        if not self.is_left:
                            push_off *= -1
                        newXVal = x
                        newXVal += push_off
                
                    

                self.x = newXVal
                self.y = newYVal
                self.turtle.setpos(self.x, self.y)
                self.lastmoveX = newXVal - x
                self.lastmoveY = newYVal - y
                #print(f"{self.lastmoveX}, {self.lastmoveY}")
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
    ["j", "l", "i", "k", ";", "'"],
    True
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