import turtle
import os
import time
import keyboard
from tkinter import PhotoImage
from turtle import Shape
from PIL import Image, ImageTk
import image_reverser
from shapely.geometry import Polygon
import numpy as np
import random

image_reverser.reverse()

#CONSTANTS
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 450
BOX_SIZE = [330, 360]
FRAME_LENGTH = 60.0


#Character constants
SCALE = 5

WALK_SPEED = 12.0
FDASH_SPEED = 35.0
FDASH_DECEL = 8.0
BDASH_SPEED = 30.0
BDASH_DECEL = 8.0
DASH_WINDOW = 4

JUMP_INITAL = 50.0
GRAVITY = 8.0
MAX_FALL = 40.0
AIR_MOVE = 15.0

BUFFER_FRAMES = 1

ANIMATION_LIST = [
    
    [ #Idle
        ["sprites/Idle_0.gif", [-11.5,11.5,-25,14], None, None, None],
        ["sprites/Idle_0.gif", [-11.5,11.5,-25,14], None, None, None],
        ["sprites/Idle_1.gif", [-11.5,11.5,-25,14], None, None, None],
        ["sprites/Idle_2.gif", [-11.5,11.5,-25,14], None, None, None],
        ["sprites/Idle_2.gif", [-11.5,11.5,-25,14], None, None, None],
        ["sprites/Idle_3.gif", [-11.5,11.5,-25,14], None, None, None],
        ["sprites/Idle_4.gif", [-11.5,11.5,-25,14], None, None, None]
    ],
    [ #WalkF
        ["sprites/F00_Forward_0.gif", [-11.5,11.5,-25,14], None, None, None],
        ["sprites/F00_Forward_1.gif", [-11.5,11.5,-25,14], None, None, None],
        ["sprites/F00_Forward_2.gif", [-11.5,11.5,-25,14], None, None, None],
        ["sprites/F00_Forward_3.gif", [-11.5,11.5,-25,14], None, None, None],
        ["sprites/F00_Forward_4.gif", [-11.5,11.5,-25,14], None, None, None],
        ["sprites/F00_Forward_5.gif", [-11.5,11.5,-25,14], None, None, None]
    ],
    [ #WalkB
        ["sprites/F00_Backward_0.gif", [-11.5,11.5,-25,14], None, None, None],
        ["sprites/F00_Backward_1.gif", [-11.5,11.5,-25,14], None, None, None],
        ["sprites/F00_Backward_2.gif", [-11.5,11.5,-25,14], None, None, None],
        ["sprites/F00_Backward_3.gif", [-11.5,11.5,-25,14], None, None, None],
        ["sprites/F00_Backward_4.gif", [-11.5,11.5,-25,14], None, None, None],
        ["sprites/F00_Backward_5.gif", [-11.5,11.5,-25,14], None, None, None]
    ],
    [ #Crouch
        ["sprites/F00_Crouch_0.gif", [-11.5,11.5,-25,2], None, None, None],
        ["sprites/F00_Crouch_1.gif", [-11.5,11.5,-25,2], None, None, None]
    ],
    [ #CrouchWait
        ["sprites/F00_CrouchWait_0.gif", [-11.5,11.5,-25,2], None, None, None],
        ["sprites/F00_CrouchWait_0.gif", [-11.5,11.5,-25,2], None, None, None],
        ["sprites/F00_CrouchWait_0.gif", [-11.5,11.5,-25,2], None, None, None],
        ["sprites/F00_CrouchWait_0.gif", [-11.5,11.5,-25,2], None, None, None],
        ["sprites/F00_CrouchWait_1.gif", [-11.5,11.5,-25,2], None, None, None],
        ["sprites/F00_CrouchWait_1.gif", [-11.5,11.5,-25,2], None, None, None],
        ["sprites/F00_CrouchWait_1.gif", [-11.5,11.5,-25,2], None, None, None],
        ["sprites/F00_CrouchWait_1.gif", [-11.5,11.5,-25,2], None, None, None]
    ],
    [ #CrouchRv
        ["sprites/F00_Crouch_1.gif", [-11.5,11.5,-25,2], None, None, None],
        ["sprites/F00_Crouch_0.gif", [-11.5,11.5,-25,14], None, None, None],
        ["sprites/Idle_0.gif", [-11.5,11.5,-25,14], None, None, None]
    ],
    [ #JumpSquat
        ["sprites/F00_JumpSquat_0.gif", [-11.5,11.5,-25,14], None, None, None],
        ["sprites/F00_JumpSquat_0.gif", [-11.5,11.5,-25,14], None, None, None]
    ],
    [ #ForwardDash
        ["sprites/F00_ForwardDash_0.gif", [-11.5,11.5,-25,14], None, None, None],
        ["sprites/F00_ForwardDash_1.gif", [-11.5,11.5,-25,14], None, None, None],
        ["sprites/F00_ForwardDash_2.gif", [-11.5,11.5,-25,14], None, None, None],
        ["sprites/F00_ForwardDash_3.gif", [-11.5,11.5,-25,14], None, None, None]
    ],
    [ #BackDash
        ["sprites/F00_BackwardDash_0.gif", None, None, None, None],
        ["sprites/F00_BackwardDash_0.gif", None, None, None, None],
        ["sprites/F00_BackwardDash_1.gif", [-11.5,11.5,-25,14], None, None, None],
        ["sprites/F00_BackwardDash_2.gif", [-11.5,11.5,-25,14], None, None, None]
    ],
    [ #Air
        ["sprites/F00_Air_0.gif", [-11.5,11.5,-25,14], None, None, None],
        ["sprites/F00_Air_0.gif", [-11.5,11.5,-25,14], None, None, None],
        ["sprites/F00_Air_1.gif", [-11.5,11.5,-25,14], None, None, None],
        ["sprites/F00_Air_2.gif", [-11.5,11.5,-25,14], None, None, None],
        ["sprites/F00_Air_2.gif", [-11.5,11.5,-25,14], None, None, None],
        ["sprites/F00_Air_1.gif", [-11.5,11.5,-25,14], None, None, None]
    ],
    [ #Attack
        ["sprites/F00_Attack_0.gif", [-11.5,11.5,-25,14], None, None, None],
        ["sprites/F00_Attack_1.gif", [-11.5,11.5,-25,14], None, None, None],
        ["sprites/F00_Attack_2.gif", [-11.5,11.5,-25,14], None, None, None],
        ["sprites/F00_Attack_3.gif", [-11.5,11.5,-25,14], [9, 32, -10, 6], [0, 1, 6, 30, 0], [9, 26, -10, 7]],
        ["sprites/F00_Attack_3.gif", [-11.5,11.5,-25,14], [9, 32, -10, 6], [0, 1, 6, 30, 0], [9, 26, -10, 7]],
        ["sprites/F00_Attack_2.gif", [-11.5,11.5,-25,14], None, None, None],
        ["sprites/F00_Attack_4.gif", [-11.5,11.5,-25,14], None, None, None],
        ["sprites/F00_Attack_5.gif", [-11.5,11.5,-25,14], None, None, None]
    ],
    [ #AttackLw
        ["sprites/F00_AttackLw_0.gif", [-11.5,11.5,-25,2], None, None, None],
        ["sprites/F00_AttackLw_1.gif", [-11.5,11.5,-25,2], None, None, None],
        ["sprites/F00_AttackLw_2.gif", [-11.5,11.5,-25,2], [3, 28, -25, -12], [-1, 1, 4, 10, 0], [3, 30, -25, -12]],
        ["sprites/F00_AttackLw_2.gif", [-11.5,11.5,-25,2], [3, 28, -25, -12], [-1, 1, 4, 10, 0], [3, 30, -25, -12]],
        ["sprites/F00_AttackLw_3.gif", [-11.5,11.5,-25,2], None, None, [3, 30, -25, -12]],
        ["sprites/F00_AttackLw_4.gif", [-11.5,11.5,-25,2], None, None, None]
    ],
    [ #AttackAir
        ["sprites/F00_AttackAir_0.gif", [-11.5,11.5,-20,12], None, None, None],
        ["sprites/F00_AttackAir_1.gif", [-11.5,11.5,-20,12], None, None, None],
        ["sprites/F00_AttackAir_2.gif", [-11.5,11.5,-20,12], [-5, 28, -10, 3], [1, 1, 4, 15, 0], [-5, 28, -10, 3]],
        ["sprites/F00_AttackAir_2.gif", [-11.5,11.5,-20,12], [-5, 28, -10, 3], [1, 1, 4, 15, 0], [-5, 28, -10, 3]],
        ["sprites/F00_AttackAir_2.gif", [-11.5,11.5,-20,12], [-5, 28, -10, 3], [1, 1, 4, 15, 0], [-5, 28, -10, 3]],
        ["sprites/F00_AttackAir_2.gif", [-11.5,11.5,-20,12], [-5, 28, -10, 3], [1, 1, 4, 15, 0], [-5, 28, -10, 3]],
        ["sprites/F00_AttackAir_2.gif", [-11.5,11.5,-20,12], [-5, 28, -10, 3], [1, 1, 4, 15, 0], [-5, 28, -10, 3]],
        ["sprites/F00_AttackAir_0.gif", [-11.5,11.5,-20,12], None, None, None],
        ["sprites/F00_Air_0.gif", [-11.5,11.5,-25,14], None, None, None]
    ],
    [ #Hitstun
        ["sprites/F00_Hitstun_0.gif", [-11.5,11.5,-25,14], None, None, None],
        ["sprites/F00_Hitstun_0.gif", [-11.5,11.5,-25,14], None, None, None],
        ["sprites/F00_Hitstun_1.gif", [-11.5,11.5,-25,14], None, None, None]
    ]
]


#Format for Frames= ["sprites/frame.gif", [hurtbox x1, hurtbox x2, hurtbox y1, hurtbox y2]
# , [hitbox x1, hitbox x2, hitbox y1, hitbox y2]
# , [hit_height, damage, hitstun, kb_speed_x, kb_speed_y] - hit height is (-1 Low, 1 High, 0 Mid)
# , [hurtbox x1, hurtbox x2, hurtbox y1, hurtbox y2] Second set of hurtboxess, used for hurtbox extensions on moves
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
    "ForwardDash",
    "BackDash",
    "Air",
    "Attack",
    "AttackLw",
    "AttackAir",
    "Hitstun"
]

ACTIONABLE_LIST = [
    get_anim_ID("Idle"), get_anim_ID("WalkF"), get_anim_ID("WalkB"), 
    get_anim_ID("Crouch"), get_anim_ID("CrouchWait"), get_anim_ID("CrouchRv"),
    get_anim_ID("Air")
]

#Collisions!
PUSHBOXES = [11.5,-25,14]
PUSHING_FORCE = 5
char_pos = [[0,0], [0,0]]

#hitbox hurtbox interactions
DEFAULT_Y_KNOCKBACK = 20 + GRAVITY
KB_DECAY_MULTIPLIER = 0.8
force_hit_now = False

hurtbox = [
    [0,0,0,0], 
    [0,0,0,0]
]
hurtbox_2 = [
    [0,0,0,0], 
    [0,0,0,0]
]


hitbox = [
    [0,0,0,0], 
    [0,0,0,0]
]


hitbox_properties = [ 
    [0,0,0,0,0], 
    [0,0,0,0,0]
]

#Debug options
ENABLE_HITBOXES = True
FRAME_STEP = False


#Hitbox/Hurtbox Drawing

if ENABLE_HITBOXES:
    p1_hurtbox_draw = turtle.Turtle()
    p1_hurtbox_draw.color("green")
    p1_hurtbox_draw.hideturtle()
    p1_hurtbox_draw2 = turtle.Turtle()
    p1_hurtbox_draw2.color("green")
    p1_hurtbox_draw2.hideturtle()
    p1_hitbox_draw = turtle.Turtle()
    p1_hitbox_draw.color("red")
    p1_hitbox_draw.hideturtle()
    p2_hurtbox_draw = turtle.Turtle()
    p2_hurtbox_draw.color("green")
    p2_hurtbox_draw.hideturtle()
    p2_hurtbox_draw2 = turtle.Turtle()
    p2_hurtbox_draw2.color("green")
    p2_hurtbox_draw2.hideturtle()
    p2_hitbox_draw = turtle.Turtle()
    p2_hitbox_draw.color("red")
    p2_hitbox_draw.hideturtle()

def rectangle(turtle, points):
    points = [
        [points[0], points[2]],
        [points[1], points[2]],
        [points[1], points[3]],
        [points[0], points[3]],
        [points[0], points[2]]
    ]
    turtle.clear()
    turtle.penup()
    turtle.speed(0)
    turtle.goto(points[0][0], points[0][1])
    turtle.pendown()
    for i in points:
        turtle.goto(i[0], i[1])
    turtle.penup()

def draw_boxes():
    screen.tracer(0)
    rectangle(p1_hurtbox_draw, hurtbox[0])
    rectangle(p2_hurtbox_draw, hurtbox[1])
    rectangle(p1_hurtbox_draw2, hurtbox_2[0])
    rectangle(p2_hurtbox_draw2, hurtbox_2[1])
    rectangle(p1_hitbox_draw, hitbox[0])
    rectangle(p2_hitbox_draw, hitbox[1])
    screen.update()
    screen.tracer(10)
        

screen = turtle.Screen()
screen.setup(SCREEN_WIDTH, SCREEN_HEIGHT)
screen.bgcolor("white")
#screen.delay(17)
for i in ["sprites", "reverse_sprites"]:
    for root, dirs, files in os.walk(i):
        #print(files)
        for filename in files:
            if filename.endswith(".gif"):
                #print(filename)
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

        #Attack Stuff
        self.attackPressed = False
        self.specialPressed = False
        self.attackBuffer = 0
        self.jumpBuffer = 0
        self.specialBuffer = 0

        #Hitstun
        self.isHitstun = False
        self.hitstunFrames = 0

        
        self.leftPressed = False
        self.rightPressed = False
        self.backdashTimer = 0
        self.forwarddashTimer = 0

        #Turtle Setup
        self.turtle = turtle.Turtle()
        self.turtle.speed(0)
        self.turtle.penup()
        self.turtle.goto(x, y)
        self.turtle.shape(self.sprite)
        self.animate()

        self.controls = controls

    def update_hit_hurt(self):
        global ANIMATION_LIST
        global JUMP_INITAL
        anim = ANIMATION_LIST[self.animListID]
        direction_mul = 1.0
        if self.is_left:
            direction_mul = -1.0
        
        x = self.turtle.xcor()
        y = self.turtle.ycor()


        hurtbox[self.playerNum - 1] = [0,0,0,0]
        hurtbox_pos = [x,x,y,y]
        if anim[self.frame][1] != None:
            hurtbox_pos[0] += anim[self.frame][1][0]*SCALE
            hurtbox_pos[1] += anim[self.frame][1][1]*SCALE
            hurtbox_pos[2] += anim[self.frame][1][2]*SCALE
            hurtbox_pos[3] += anim[self.frame][1][3]*SCALE
            hurtbox[self.playerNum - 1] = hurtbox_pos
        else:
            hurtbox[self.playerNum - 1] = [9990, 10000, 9990, 10000]

        hurtbox_2[self.playerNum - 1] = [0,0,0,0]
        hurtbox2_pos = [x,x,y,y]
        if anim[self.frame][4] != None:
            if direction_mul > 0:
                hurtbox2_pos[0] += anim[self.frame][4][0]*SCALE* direction_mul
                hurtbox2_pos[1] += anim[self.frame][4][1]*SCALE* direction_mul
            else:
                hurtbox2_pos[1] += anim[self.frame][4][0]*SCALE* direction_mul
                hurtbox2_pos[0] += anim[self.frame][4][1]*SCALE* direction_mul
            hurtbox2_pos[2] += anim[self.frame][4][2]*SCALE
            hurtbox2_pos[3] += anim[self.frame][4][3]*SCALE
            hurtbox_2[self.playerNum - 1] = hurtbox2_pos
        else:
            hurtbox_2[self.playerNum - 1] = [999, 1000, 999, 1000]

        
        hitbox[self.playerNum - 1] = [0,0,0,0]
        hitbox_pos = [x,x,y,y]
        if anim[self.frame][2] != None and not self.hasHit:
            if direction_mul > 0:
                hitbox_pos[0] += (anim[self.frame][2][0] * direction_mul)*SCALE
                hitbox_pos[1] += (anim[self.frame][2][1] * direction_mul)*SCALE
            else:
                hitbox_pos[1] += (anim[self.frame][2][0] * direction_mul)*SCALE
                hitbox_pos[0] += (anim[self.frame][2][1] * direction_mul)*SCALE
            hitbox_pos[2] += anim[self.frame][2][2]*SCALE
            hitbox_pos[3] += anim[self.frame][2][3]*SCALE
            hitbox[self.playerNum - 1] = hitbox_pos
            #print(f"Hitboxes out! Hurtbox: {hurtbox_pos}  Hitbox: {hitbox_pos}")
            #print(f"pos [{x}, {y}]")
        else:
            hitbox[self.playerNum - 1] = [9990, 10000, 9990, 10000]
            self.hasHit = False

        
        hitbox_properties[self.playerNum - 1] = anim[self.frame][3]

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

        #Report Hitboxes and Hurtboxes
        self.update_hit_hurt()
        
        if self.frame+1 >= anim_length: #Returns to default anim for state
            self.frame = 0
            self.set_new_anim_by_ID()
        else:
            self.frame += 1

    def overlap(self, rect1, rect2):
        r1x1 = rect1[0]
        r1x2 = rect1[1]
        r1y1 = rect1[2]
        r1y2 = rect1[3]
        r2x1 = rect2[0]
        r2x2 = rect2[1]
        r2y1 = rect2[2]
        r2y2 = rect2[3]
        if r1x1 > r2x2 or r2x1 > r1x2:
            return False
        if r1y1 > r2y2 or r2y1 > r1y2:
            return False
        
        print("Overlaps!")
        return True
        
    def check_is_hurt(self):
        global ANIMATION_LIST
        global ACTIONABLE_LIST
        #print(f"[{self.x}, {self.y}]")
        enemy_hitbox = hitbox[-(self.playerNum)]
        my_hurtbox = hurtbox[self.playerNum - 1]
        my_hurtbox2 = hurtbox_2[self.playerNum - 1]

        enemy_properties = hitbox_properties[-(self.playerNum)]
        #if enemy_hitbox[0] < 9000:
            #print(f"hurtbox [{my_hurtbox[0]} - {my_hurtbox[1]}], hitbox [{enemy_hitbox[0]} - {enemy_hitbox[1]}]")
        if not enemy_properties == None and enemy_hitbox[0] < 9000 and (self.overlap(enemy_hitbox, my_hurtbox) or self.overlap(enemy_hitbox, my_hurtbox2)):
            print("Hitstun!")
            self.isHitstun = True
            self.hitstunFrames = enemy_properties[2]
            self.moveXThisFrame = enemy_properties[3]
            if self.is_left == True:
                self.moveXThisFrame *= -1
            
            self.moveYThisFrame = enemy_properties[4]
            if enemy_properties[4] == 0 and self.isJump:
                self.moveYThisFrame = DEFAULT_Y_KNOCKBACK
            self.lastmoveX = self.moveXThisFrame * -1
            self.lastmoveY = self.moveYThisFrame
            self.set_new_anim_by_ID(get_anim_ID("Hitstun"))
    
    def hitstun_movement(self):
        if self.isHitstun:
            self.moveXThisFrame = self.lastmoveX * KB_DECAY_MULTIPLIER
            self.moveYThisFrame = self.lastmoveY * KB_DECAY_MULTIPLIER
            self.lastmoveY = self.moveYThisFrame
            self.lastmoveX = self.moveXThisFrame

    def check_is_hitting(self):
        global ANIMATION_LIST
        global ACTIONABLE_LIST
        global force_hit_now
        #print(f"[{self.x}, {self.y}]")
        enemy_hurtbox = hurtbox[-(self.playerNum)]
        enemy_hurtbox2 = hurtbox_2[-(self.playerNum)]
        my_hitbox = hitbox[self.playerNum - 1]

        if my_hitbox[0] < 9000 and (self.overlap(enemy_hurtbox, my_hitbox) or self.overlap(enemy_hurtbox2, my_hitbox)):
            if not self.hasHit:
                force_hit_now = True
                self.hasHit = True
    
    
    def set_new_anim_by_ID(self, id=-2, frame=0):
        if id == -1:
            return
        if id == -2:
            self.frame = frame
            if self.isHitstun:
                    self.animListID = get_anim_ID("Hitstun")
                    return
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
        if self.isJump == False and not self.isHitstun:
            if self.animListID in [get_anim_ID("Idle"), get_anim_ID("WalkF"), get_anim_ID("WalkB")]:
                self.moveXThisFrame = WALK_SPEED
            if self.is_left == False: #If facing left
                if self.animListID in [get_anim_ID("Idle"), get_anim_ID("WalkB")]:
                    self.set_new_anim_by_ID(get_anim_ID("WalkF"))
                if self.animListID == get_anim_ID("WalkF") and self.frame >= len(ANIMATION_LIST[self.animListID])-1:
                    self.set_new_anim_by_ID(get_anim_ID("WalkF"))
                
                if self.rightPressed == False:
                    if self.forwarddashTimer == 0:
                        self.forwarddashTimer = DASH_WINDOW
                    else:
                        self.forwarddashTimer = 0
                        self.set_new_anim_by_ID(get_anim_ID("ForwardDash"))
                        self.moveXThisFrame = FDASH_SPEED
            else:
                if self.animListID in [get_anim_ID("Idle"), get_anim_ID("WalkF")]:
                    self.set_new_anim_by_ID(get_anim_ID("WalkB"))
                if self.animListID == get_anim_ID("WalkB") and self.frame >= len(ANIMATION_LIST[self.animListID])-1:
                    self.set_new_anim_by_ID(get_anim_ID("WalkB"))

                if self.rightPressed == False:
                    if self.backdashTimer == 0:
                        self.backdashTimer = DASH_WINDOW
                    else:
                        self.backdashTimer = 0
                        self.set_new_anim_by_ID(get_anim_ID("BackDash"))
                        self.moveXThisFrame = BDASH_SPEED


    def left(self):
        global ANIMATION_LIST
        global WALK_SPEED
        if self.isJump == False and not self.isHitstun:
            if self.animListID in [get_anim_ID("Idle"), get_anim_ID("WalkF"), get_anim_ID("WalkB")]:
                self.moveXThisFrame = -WALK_SPEED
            if self.is_left == True: #If facing left
                if self.animListID in [get_anim_ID("Idle"), get_anim_ID("WalkB")]:
                    self.set_new_anim_by_ID(get_anim_ID("WalkF"))
                if self.animListID == get_anim_ID("WalkF") and self.frame >= len(ANIMATION_LIST[self.animListID])-1:
                    self.set_new_anim_by_ID(get_anim_ID("WalkF"))
                
                if self.leftPressed == False:
                    if self.forwarddashTimer == 0:
                        self.forwarddashTimer = DASH_WINDOW
                    else:
                        self.forwarddashTimer = 0
                        self.set_new_anim_by_ID(get_anim_ID("ForwardDash"))
                        self.moveXThisFrame = -FDASH_SPEED
            else:
                if self.animListID in [get_anim_ID("Idle"), get_anim_ID("WalkF")]:
                    self.set_new_anim_by_ID(get_anim_ID("WalkB"))
                if self.animListID == get_anim_ID("WalkB") and self.frame >= len(ANIMATION_LIST[self.animListID])-1:
                    self.set_new_anim_by_ID(get_anim_ID("WalkB"))

                if self.leftPressed == False:
                    if self.backdashTimer == 0:
                        self.backdashTimer = DASH_WINDOW
                    else:
                        self.backdashTimer = 0
                        self.set_new_anim_by_ID(get_anim_ID("BackDash"))
                        self.moveXThisFrame = -BDASH_SPEED
                    
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
            if self.animListID in [get_anim_ID("Idle"), get_anim_ID("WalkF"), get_anim_ID("WalkB"), get_anim_ID("CrouchRv")]:
                self.isJump = True
                self.set_new_anim_by_ID(get_anim_ID("JumpSquat"))
            else:
                self.jumpBuffer = BUFFER_FRAMES
            
    
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
                    
                    if (keyboard.is_pressed(self.controls[4]) and not keyboard.is_pressed(self.controls[5])):
                        self.attackBuffer = 1
                else:
                    self.moveYThisFrame = self.lastmoveY - GRAVITY
                    if not self.isHitstun:
                        self.moveXThisFrame = self.jumpDir * AIR_MOVE * -1.0
                    
    def attack(self):
        global ANIMATION_LIST
        global ACTIONABLE_LIST
        if not self.animListID in ACTIONABLE_LIST:
            self.attackBuffer = BUFFER_FRAMES
        else:
            self.attackBuffer = 0

        if not self.isJump:
            if self.animListID in ACTIONABLE_LIST:
                if keyboard.is_pressed(self.controls[3]) and not keyboard.is_pressed(self.controls[2]):
                    self.set_new_anim_by_ID(get_anim_ID("AttackLw"))
                else:
                    self.set_new_anim_by_ID(get_anim_ID("Attack"))
        else:
            if self.animListID in ACTIONABLE_LIST:
                    self.set_new_anim_by_ID(get_anim_ID("AttackAir"))

                    
    def dash(self):
        global ANIMATION_LIST
        global ACTIONABLE_LIST
        if self.isJump or self.isCrouch or self.isHitstun:
            return
        
        side_mul = 1
        if self.is_left:
            side_mul = -1

        if self.animListID == get_anim_ID("ForwardDash"):
            if self.lastmoveX != 0:
                self.moveXThisFrame = self.lastmoveX - (FDASH_DECEL*side_mul)
                
                if abs(self.lastmoveX) - BDASH_DECEL < 0:
                    self.moveXThisFrame = 0

        if self.animListID == get_anim_ID("BackDash"):
            if self.lastmoveX != 0:
                self.moveXThisFrame = self.lastmoveX + (BDASH_DECEL*side_mul)

                if abs(self.lastmoveX) - BDASH_DECEL < 0:
                    self.moveXThisFrame = 0


    
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
            global force_hit_now

            if force_hit_now and not self.hasHit and not hitbox_properties[-(self.playerNum)] == None:
                enemy_properties = hitbox_properties[-(self.playerNum)]
                force_hit_now = False
                print("Has Forced a hit")
                self.isHitstun = True
                self.hitstunFrames = enemy_properties[2]
                self.moveXThisFrame = enemy_properties[3]
                if self.is_left == True:
                    self.moveXThisFrame *= -1
                
                self.moveYThisFrame = enemy_properties[4]
                if enemy_properties[4] == 0 and self.isJump:
                    self.moveYThisFrame = DEFAULT_Y_KNOCKBACK
                self.lastmoveX = self.moveXThisFrame * -1
                self.lastmoveY = self.moveYThisFrame
                self.set_new_anim_by_ID(get_anim_ID("Hitstun"))

            self.check_correct_side()
            self.check_is_hurt()
            self.check_is_hitting()
            self.hitstun_movement()
            self.air()
            self.dash()
            self.animate()


            if keyboard.is_pressed(self.controls[0]) and not keyboard.is_pressed(self.controls[1]):
                self.left()
            elif (self.animListID == get_anim_ID("WalkF") and self.is_left != False) or (self.animListID == get_anim_ID("WalkB") and self.is_left != True):
                if  not self.isHitstun:
                    self.set_new_anim_by_ID()
            
            if keyboard.is_pressed(self.controls[0]) and not keyboard.is_pressed(self.controls[1]):
                self.leftPressed = True
            else:
                self.leftPressed = False

            if keyboard.is_pressed(self.controls[1]) and not keyboard.is_pressed(self.controls[0]):
                self.right()
            elif (self.animListID == get_anim_ID("WalkF") and self.is_left != True) or (self.animListID == get_anim_ID("WalkB") and self.is_left != False):
                self.set_new_anim_by_ID()
                
                
            if keyboard.is_pressed(self.controls[1]) and not keyboard.is_pressed(self.controls[0]):
                self.rightPressed = True
            else:
                self.rightPressed = False

                
            if keyboard.is_pressed(self.controls[3]) and not keyboard.is_pressed(self.controls[2]):
                self.down()
            elif self.isCrouch:
                self.uncrouch()
            if (keyboard.is_pressed(self.controls[2]) and not keyboard.is_pressed(self.controls[3])) or self.jumpBuffer > 0:
                self.up()
                
            if (keyboard.is_pressed(self.controls[4]) and not keyboard.is_pressed(self.controls[5]) and not self.attackPressed) or self.attackBuffer > 0:
                self.attackPressed = True
                self.attack()
            
            if self.attackBuffer > 0:
                self.attackBuffer -= 1
                
            if self.jumpBuffer > 0:
                self.jumpBuffer -= 1
                
            if self.hitstunFrames > 0:
                print("still in hitstun")
                self.hitstunFrames -= 1
                
            if self.backdashTimer > 0:
                self.backdashTimer -= 1
            if self.forwarddashTimer > 0:
                self.forwarddashTimer -= 1

            if self.hitstunFrames <= 0:
                self.isHitstun = False
                if self.y < 5:
                    self.y = 0

            if not keyboard.is_pressed(self.controls[4]):
                self.attackPressed = False


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

                if self.x > BOX_SIZE[0]:
                    self.x = BOX_SIZE[0]
                if self.x < -BOX_SIZE[0]:
                    self.x = -BOX_SIZE[0]
                if self.y < 0:
                    self.y = 0
                self.turtle.setpos(self.x, self.y)
                self.lastmoveX = newXVal - x
                self.lastmoveY = newYVal - y
                #print(f"{self.lastmoveX}, {self.lastmoveY}")
                self.moveXThisFrame = 0.0
                self.moveYThisFrame = 0.0

            
            self.update_hit_hurt()
            if ENABLE_HITBOXES:
                draw_boxes()

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
    turn_order = bool(random.getrandbits(1))
    if not FRAME_STEP or keyboard.is_pressed("space"):
        if turn_order:
            p1.update()
            p2.update()
        else:
            p2.update()
            p1.update()
    end = time.time()
    new_delay = (end-start)*10**3
    #print(f"Time taken: {new_delay}ms, normalise: {FRAME_LENGTH - (new_delay)}ms")
    if (new_delay/1000) < FRAME_LENGTH/1000:
        time.sleep(FRAME_LENGTH/1000 - (new_delay/1000))
    prev_delay = new_delay
screen.mainloop()