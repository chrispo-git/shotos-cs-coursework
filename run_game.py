import turtle
import os
import time
import keyboard
from tkinter import PhotoImage
from turtle import Shape
import random
import math
import sys
import menu
import cpu_data
import animations
import stats
from util import get_anim_ID
from util import get_controls_from_txt


#CONSTANTS
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 450
BOX_SIZE = [325, 360]
FRAME_LENGTH = 60.0 #Game runs at 16.667 fps

#Character constants
SCALE = 5

DASH_WINDOW = 4

JUMP_INITAL = 50.0
GRAVITY = 8.0
MAX_FALL = 40.0
AIR_MOVE = 15.0

SPECIAL_LW_INIT_Y = 45.0
SPECIAL_LW_INIT_X = 10.0

SPECIAL_S_X = 20.0

BUFFER_FRAMES = 1


#Collisions!
PUSHBOXES = [11.5,-25,14]
PUSHING_FORCE = 5
char_pos = [[0,0], [0,0]]

#hitbox hurtbox interactions
HP_RESTORE_DURATION = 45
BLOCK_TIME = 11
DEFAULT_Y_KNOCKBACK = 20 + GRAVITY
KB_DECAY_MULTIPLIER = 0.8
force_hit_now = False
PUSHBACK = 15
BLOCK_KB_MUL = 0.5
AIR_BLOCK_HITSTUN_MUL = 1.5

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
    [0,0,0,0,0,0], 
    [0,0,0,0,0,0]
]

players_x = [0,0]
players_y = [0,0]



#Format for Frames= ["sprites/frame.gif", [hurtbox x1, hurtbox x2, hurtbox y1, hurtbox y2]
# , [hitbox x1, hitbox x2, hitbox y1, hitbox y2]
# , [hit_height, damage, hitstun, kb_speed_x, kb_speed_y, blockstun] - hit height is (-1 Low, 1 High, 0 Mid, 2 unblockable)
# , [hurtbox x1, hurtbox x2, hurtbox y1, hurtbox y2] Second set of hurtboxess, used for hurtbox extensions on moves


#Lists of anims in a certain category
ACTIONABLE_LIST = [
    get_anim_ID("Idle"), get_anim_ID("WalkF"), get_anim_ID("WalkB"), 
    get_anim_ID("Crouch"), get_anim_ID("CrouchWait"), get_anim_ID("CrouchRv"),
    get_anim_ID("Air")
]

SPECIAL_CANCEL_LIST = [
    get_anim_ID("Attack"), get_anim_ID("AttackLw"), get_anim_ID("AttackAir"),
    get_anim_ID("Heavy"), get_anim_ID("HeavyLw"), get_anim_ID("HeavyAir")

]

BLOCKING_LIST = [
    get_anim_ID("Guard"), get_anim_ID("CrouchGuard"), get_anim_ID("GuardAir")
]


#Debug options
FRAME_STEP = False
SPACE_TO_PAUSE = True


#Hitbox/Hurtbox Drawing


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

def draw_boxes(screen, p1hurt, p1hurt2, p1hit, p2hurt, p2hurt2, p2hit): #Used for hurtbox/hitbox display in training mode
    screen.tracer(0)
    rectangle(p1hurt, hurtbox[0])
    rectangle(p2hurt, hurtbox[1])
    rectangle(p1hurt2, hurtbox_2[0])
    rectangle(p2hurt2, hurtbox_2[1])
    rectangle(p1hit, hitbox[0])
    rectangle(p2hit, hitbox[1])
    screen.update()
    screen.tracer(10)
        
CHAR_ANIMS = [animations.RYU, animations.KEN, animations.SEAN, animations.AKUMA]
#print(screen.getshapes())

class player:
    def __init__(self, 
        playerNum: int,
        x: int, y: int,
        #sprite, frame, animList,
        controls: list, #Controls expressed as [left, right, up, down, light, heavy, special]
        Left: bool,
        Training_settings: list,
        character: int,
        alt: int,
        read_log = False,
        is_cpu = False
    ):
        self.playerNum = playerNum
        self.x = x
        self.y = y
        self.char_id = character
        self.accessOtherPlayer = []
        self.is_left = Left
        self.isCrouch = False
        self.moveXThisFrame = 0.0
        self.moveYThisFrame = 0.0

        #Sprite Init
        self.frame = 0
        self.animList = CHAR_ANIMS[self.char_id]
        self.animListID = 0
        self.alt = alt
        self.sprite = f"sprites/F0{self.char_id}_Idle_0.gif"
        self.training_settings = Training_settings
        self.start_blocking_now = 0

        #Jump Attributes
        self.isJump = False
        self.lastmoveY = 0.0
        self.lastmoveX = 0.0
        self.lastmoveX = 0.0
        self.jumpDir = 0.0 #-1.0 is back, 0.0 is neutral, 1.0 is forwards

        #Attack Stuff
        self.attackPressed = False
        self.specialPressed = False
        self.heavyPressed = False
        self.attackBuffer = 0
        self.jumpBuffer = 0
        self.specialBuffer = 0
        self.heavyBuffer = 0
        self.doPushback = False
        self.buttoncheck = [False,False,False,False,False,False,False]

        #Hitstun
        self.isHitstun = False
        self.isBlockstun = False
        self.isLeaveBlockstun = False
        self.isBlocking = False
        self.hitstunFrames = 0
        self.maxHitstun = 0
        self.hp = stats.HEALTH[self.char_id]
        self.decreaseHp = 0

        
        self.leftPressed = False
        self.rightPressed = False
        self.backdashTimer = 0
        self.forwarddashTimer = 0
        self.disableJostle = False

        #For Hadouken
        self.hadouTimer = 0

        #Turtle Setup
        self.turtle = turtle.Turtle()
        self.turtle.speed(0)
        self.turtle.penup()
        self.turtle.goto(x, y)
        self.turtle.shape(self.sprite)
        self.animate()

        self.isCpu = is_cpu
        self.cpuQueue = []

        self.controls = controls
        self.readLog = read_log
        self.logFrame = 0
        self.log = []
        if self.readLog: #Debug logging stuff, to check if you can take full control of the player using code rather than buttons
            try:
                f = open("test_log.txt")
                text = f.readlines()
                f.close()
                for i in text:
                    line = i.replace(" ", "")
                    line = line.replace("\n", "")
                    line = line.replace("[", "")
                    line = line.replace("]", "")
                    line = line.split(",")
                    line = [ele.lower().capitalize() == "True" for ele in line] #Converts strings into real booleans
                    self.log.append(line)
            except Exception:
                print("failed to read log")
                self.log = []
                self.readLog = False
        
        self.logLength = len(self.log)

    
    def update_other_list(self, new): #Used to access opponent's attributes and methods
        self.accessOtherPlayer = new

    def update_hit_hurt(self): #Updates hitbox and hurtbox placement
        global JUMP_INITAL
        anim = self.animList[self.animListID]
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
            hurtbox_2[self.playerNum - 1] = [9990, 10000, 9990, 10000]

        
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
        global JUMP_INITAL
        anim = self.animList[self.animListID]
        anim_length = len(anim)
        sprite = anim[self.frame][0]
        if self.is_left == True:
            sprite = sprite.replace("sprites", "reverse_sprites") #If facing left, replace them with their reversed variant

        if self.alt != 0:
            sprite = sprite.replace("sprites/", f"sprites{self.alt+1}/")
            sprite = sprite.replace("reverse_sprites/", f"reverse_sprites{self.alt+1}/")
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

    def overlap(self, rect1, rect2): #Checks if 2 rectangles in space overlap! If they do reports as true. Used to check if hitboxes overlap hurtboxes
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
        
        #print("Overlaps!")
        return True
    
    def did_i_block_that(self): #The blocking checker
        enemy_properties = hitbox_properties[-(self.playerNum)]
        high_low = enemy_properties[0]
        if high_low == 2: #Unblockable! Used for throws
            return False
        
        if self.isHitstun and not self.isBlockstun: #You can't block while you're in hitstun!
            return False
        
        if (self.training_settings[3] == 1 or self.start_blocking_now > 0) and (self.animListID in ACTIONABLE_LIST or self.animListID in BLOCKING_LIST) and self.playerNum == 2:
            if self.training_settings[3] == 2: #Training mode block all or block after first hit type behaviour
                self.start_blocking_now = BLOCK_TIME

            self.isBlocking = True
            if high_low == -1:
                self.isCrouch = True
            return True
        if self.isCpu: #CPU behaviour
            if random.randint(0, 100) < cpu_data.BLOCK_CHANCE and (self.animListID in ACTIONABLE_LIST or self.animListID in BLOCKING_LIST):
                self.isBlocking = True
                if high_low == -1:
                    self.isCrouch = True
                return True

        if self.isBlocking: #Regular behaviour
            if high_low == 0:
                return True 
            if high_low == -1 and self.isCrouch:
                return True 
            if high_low == 1 and not self.isCrouch:
                return True 
        
        return False

    def start_hitstun(self):
            #print("start")
            enemy_properties = hitbox_properties[-(self.playerNum)]
            self.hitstunFrames = enemy_properties[2]
            #print(self.hitstunFrames)
            self.moveXThisFrame = enemy_properties[3]
            if self.is_left == True:
                self.moveXThisFrame *= -1
            
            self.moveYThisFrame = enemy_properties[4]
            if enemy_properties[4] == 0 and self.isJump:
                self.moveYThisFrame = DEFAULT_Y_KNOCKBACK
            
            
            if self.did_i_block_that():
                self.isBlockstun = True
                self.moveXThisFrame *= BLOCK_KB_MUL
                self.moveYThisFrame = 0
                self.hitstunFrames = int(math.floor(enemy_properties[5]))
                if self.isJump:
                    self.hitstunFrames = int(math.floor(enemy_properties[5]*AIR_BLOCK_HITSTUN_MUL))
                
            self.isHitstun = True

            self.lastmoveX = self.moveXThisFrame * -1
            self.lastmoveY = self.moveYThisFrame
            if not self.did_i_block_that():
                self.jumpDir = 0
                if self.training_settings[3] == 2:
                    self.start_blocking_now = BLOCK_TIME
                if enemy_properties[4] > 0 and not self.isJump:
                    self.isJump = True
                    self.lastmoveY = self.moveYThisFrame + GRAVITY

                if self.maxHitstun != self.hitstunFrames:
                    self.maxHitstun = self.hitstunFrames
                    #print("Hurting")
                    self.decreaseHp = enemy_properties[1]
                self.set_new_anim_by_ID()
            else:
                if self.isCrouch:
                    self.set_new_anim_by_ID()
                else:
                    self.set_new_anim_by_ID()

    def check_is_hurt(self):
        global ACTIONABLE_LIST
        #print(f"[{self.x}, {self.y}]")
        enemy_hitbox = hitbox[-(self.playerNum)]
        my_hurtbox = hurtbox[self.playerNum - 1]
        my_hurtbox2 = hurtbox_2[self.playerNum - 1]

        enemy_properties = hitbox_properties[-(self.playerNum)]
        #if enemy_hitbox[0] < 9000:
            #print(f"hurtbox [{my_hurtbox[0]} - {my_hurtbox[1]}], hitbox [{enemy_hitbox[0]} - {enemy_hitbox[1]}]")
        if not enemy_properties == None and enemy_hitbox[0] < 9000 and (self.overlap(enemy_hitbox, my_hurtbox) or self.overlap(enemy_hitbox, my_hurtbox2)):
            #print("Hitstun!")
            self.start_hitstun()
            
    
    def hitstun_movement(self):
        if self.isHitstun: #Governs where they be going during hitstun
            self.moveXThisFrame = self.lastmoveX * KB_DECAY_MULTIPLIER #Knockback decays at a set rate so that it naturally stops
            self.moveYThisFrame = self.lastmoveY * KB_DECAY_MULTIPLIER
            self.lastmoveY = self.moveYThisFrame
            self.lastmoveX = self.moveXThisFrame


    def check_is_hitting(self):
        global ACTIONABLE_LIST
        global force_hit_now
        #print(f"[{self.x}, {self.y}]")
        enemy_hurtbox = hurtbox[-(self.playerNum)]
        enemy_hurtbox2 = hurtbox_2[-(self.playerNum)]
        my_hitbox = hitbox[self.playerNum - 1]

        if my_hitbox[0] < 9000 and (self.overlap(enemy_hurtbox, my_hitbox) or self.overlap(enemy_hurtbox2, my_hitbox)):
            if not self.hasHit:
                #print("Yeah")
                force_hit_now = True
                self.hasHit = True
                
                self.doPushback = True
    
    
    def set_new_anim_by_ID(self, id=-2, frame=0):
        if id == -1:
            return
        
        
        self.doPushback = False
        self.hasHit = False

        if id == -2:
            self.frame = frame
            if self.isHitstun:
                    if self.isBlockstun:
                        if self.isCrouch:
                            self.set_new_anim_by_ID(get_anim_ID("CrouchGuard"))
                        elif self.isJump:
                            self.set_new_anim_by_ID(get_anim_ID("GuardAir"))
                        else:
                            self.set_new_anim_by_ID(get_anim_ID("Guard"))
                    else:
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
        
        global force_hit_now

        force_hit_now = False
        self.frame = frame
        self.animListID = id


    
    def right(self):
        global SPECIAL_CANCEL_LIST
        #print(f"[{self.x}, {self.y}]")
        if self.isJump == False and not self.isHitstun:
            if self.animListID in [get_anim_ID("Idle"), get_anim_ID("WalkF"), get_anim_ID("WalkB")]:
                self.moveXThisFrame = stats.WALK_SPEED[self.char_id]
            if self.is_left == False: #If facing left
                if self.animListID in [get_anim_ID("Idle"), get_anim_ID("WalkB")]:
                    self.set_new_anim_by_ID(get_anim_ID("WalkF"))
                if self.animListID == get_anim_ID("WalkF") and self.frame >= len(self.animList[self.animListID])-1:
                    self.set_new_anim_by_ID(get_anim_ID("WalkF"))
                
                if self.rightPressed == False:
                    if self.forwarddashTimer == 0:
                        self.forwarddashTimer = DASH_WINDOW
                    else:
                        if self.animListID in ACTIONABLE_LIST:
                            self.forwarddashTimer = 0
                            self.set_new_anim_by_ID(get_anim_ID("ForwardDash"))
                            self.moveXThisFrame = stats.FDASH_SPEED[self.char_id]
            else:
                if self.animListID in [get_anim_ID("Idle"), get_anim_ID("WalkF")]:
                    self.set_new_anim_by_ID(get_anim_ID("WalkB"))
                if self.animListID == get_anim_ID("WalkB") and self.frame >= len(self.animList[self.animListID])-1:
                    self.set_new_anim_by_ID(get_anim_ID("WalkB"))

                if self.rightPressed == False:
                    if self.backdashTimer == 0:
                        self.backdashTimer = DASH_WINDOW
                    else:
                        if self.animListID in ACTIONABLE_LIST:
                            self.backdashTimer = 0
                            self.set_new_anim_by_ID(get_anim_ID("BackDash"))
                            self.moveXThisFrame = stats.BDASH_SPEED[self.char_id]


    def left(self):
        if self.isJump == False and not self.isHitstun:
            if self.animListID in [get_anim_ID("Idle"), get_anim_ID("WalkF"), get_anim_ID("WalkB")]:
                self.moveXThisFrame = -stats.WALK_SPEED[self.char_id]
            if self.is_left == True: #If facing left
                if self.animListID in [get_anim_ID("Idle"), get_anim_ID("WalkB")]:
                    self.set_new_anim_by_ID(get_anim_ID("WalkF"))
                if self.animListID == get_anim_ID("WalkF") and self.frame >= len(self.animList[self.animListID])-1:
                    self.set_new_anim_by_ID(get_anim_ID("WalkF"))
                
                if self.leftPressed == False:
                    if self.forwarddashTimer == 0:
                        self.forwarddashTimer = DASH_WINDOW
                    else:
                        if self.animListID in ACTIONABLE_LIST:
                            self.forwarddashTimer = 0
                            self.set_new_anim_by_ID(get_anim_ID("ForwardDash"))
                            self.moveXThisFrame = -stats.FDASH_SPEED[self.char_id]
            else:
                if self.animListID in [get_anim_ID("Idle"), get_anim_ID("WalkF")]:
                    self.set_new_anim_by_ID(get_anim_ID("WalkB"))
                if self.animListID == get_anim_ID("WalkB") and self.frame >= len(self.animList[self.animListID])-1:
                    self.set_new_anim_by_ID(get_anim_ID("WalkB"))

                if self.leftPressed == False:
                    if self.backdashTimer == 0:
                        self.backdashTimer = DASH_WINDOW
                    else:
                        if self.animListID in ACTIONABLE_LIST:
                            self.backdashTimer = 0
                            self.set_new_anim_by_ID(get_anim_ID("BackDash"))
                            self.moveXThisFrame = -stats.BDASH_SPEED[self.char_id]
                    
    def down(self):
        #print(f"[{self.x}, {self.y}]")
        if self.isJump == False:
            if self.isCrouch == False and self.animListID in [get_anim_ID("Idle"), get_anim_ID("WalkF"), get_anim_ID("WalkB")]:
                self.isCrouch = True
                self.set_new_anim_by_ID(get_anim_ID("Crouch"))

                
    def uncrouch(self):
        #print(f"[{self.x}, {self.y}]")
        if self.isCrouch == True and self.animListID in [get_anim_ID("CrouchWait")]:
                self.isCrouch = False
                self.set_new_anim_by_ID(get_anim_ID("CrouchRv"))

                
    def up(self):
        #print(f"[{self.x}, {self.y}]")
        if self.isJump == False:
            if self.animListID in [get_anim_ID("Idle"), get_anim_ID("WalkF"), get_anim_ID("WalkB"), get_anim_ID("CrouchRv")]:
                self.isJump = True
                self.set_new_anim_by_ID(get_anim_ID("JumpSquat")) #Jump time
            else:
                self.jumpBuffer = BUFFER_FRAMES
            
    
    def air(self):
        global JUMP_INITAL
        global GRAVITY
        global MAX_FALL
        global AIR_MOVE
        global force_hit_now
        #print(f"[{self.x}, {self.y}]")
        if self.isJump == True:
            if self.y <= 0.0 and self.lastmoveY < 0.0:
                self.isJump = False
                if self.y < 0.0:
                    self.moveYThisFrame = -self.y
                self.set_new_anim_by_ID()
            else:
                if self.animListID == get_anim_ID("JumpSquat"):
                    if self.buttoncheck[0] and not self.buttoncheck[1]:
                        self.jumpDir = 1.0 #Jump right
                    elif self.buttoncheck[1] and not self.buttoncheck[0]:
                        self.jumpDir = -1.0 #Jump left
                    else:
                        self.jumpDir = 0.0 #Jump straight
                    
                    #makes buffering rising aerials a breeze!
                    if self.buttoncheck[4] and not self.buttoncheck[5]:
                        self.attackBuffer = 1
                    if self.buttoncheck[5] and not self.buttoncheck[4]:
                        self.heavyBuffer = 1
                else:
                    #print("we running")
                    self.moveYThisFrame = self.lastmoveY - GRAVITY #Makes them fall
                    if not self.isHitstun:
                        self.moveXThisFrame = self.jumpDir * AIR_MOVE * -1.0
                    
    def attack(self):
        global ACTIONABLE_LIST
        if not self.animListID in ACTIONABLE_LIST: #Attack buffer
            self.attackBuffer = BUFFER_FRAMES
        else:
            self.attackBuffer = 0

        if not self.isJump:
            if self.animListID in ACTIONABLE_LIST:
                self.doPushback = False
                if self.buttoncheck[3] and not self.buttoncheck[2]:
                    self.set_new_anim_by_ID(get_anim_ID("AttackLw"))
                else:
                    self.set_new_anim_by_ID(get_anim_ID("Attack"))
        else:
            if self.animListID in ACTIONABLE_LIST:
                    self.set_new_anim_by_ID(get_anim_ID("AttackAir"))
                    
    def HeavyAir(self):
        global ACTIONABLE_LIST
        if not self.animListID == get_anim_ID("HeavyAir"):
            return
        
        if self.char_id == 3: #Akuma Divekick
            direction_mul = 1.0
            if self.is_left:
                direction_mul = -1.0

            if self.frame > 2:
                self.moveXThisFrame = 30 * direction_mul
                self.moveYThisFrame = -90
            else:
                self.moveXThisFrame = 0
                self.moveYThisFrame = 2
                    
    def attackLw(self):
        global ACTIONABLE_LIST
        if not self.animListID == get_anim_ID("AttackLw"):
            return
        
        if self.char_id == 2: #So sean can slide
            direction_mul = 1.0
            if self.is_left:
                direction_mul = -1.0

            if self.frame < 9:
                self.moveXThisFrame = 18 * direction_mul
            
    def heavyN(self):
        global ACTIONABLE_LIST
        if not self.animListID == get_anim_ID("Heavy"):
            return
        
        if self.char_id == 0: #So ryu can kick
            direction_mul = 1.0
            if self.is_left:
                direction_mul = -1.0

            if self.frame < 6:
                self.moveXThisFrame = 10 * direction_mul
            
            if self.frame == 6:
                self.moveXThisFrame = 25 * direction_mul
        
        if self.char_id == 3: #So akuma can kick
            direction_mul = 1.0
            if self.is_left:
                direction_mul = -1.0

            if self.frame < 4:
                self.moveXThisFrame = 10 * direction_mul
            elif self.frame == 4:
                self.moveXThisFrame = 32 * direction_mul
            elif self.frame < 8:
                self.moveXThisFrame = 10 * direction_mul


    def heavy(self):
        global ACTIONABLE_LIST
        if not self.animListID in ACTIONABLE_LIST:
            self.heavyBuffer = BUFFER_FRAMES
        else:
            self.heavyBuffer = 0

        if not self.isJump:
            if self.animListID in ACTIONABLE_LIST:
                self.doPushback = False
                if self.buttoncheck[3] and not self.buttoncheck[2]:
                    self.set_new_anim_by_ID(get_anim_ID("HeavyLw"))
                else:
                    self.set_new_anim_by_ID(get_anim_ID("Heavy"))
        else:
            if self.animListID in ACTIONABLE_LIST:
                    self.set_new_anim_by_ID(get_anim_ID("HeavyAir"))
                    
    def special(self):
        global ACTIONABLE_LIST
        global SPECIAL_CANCEL_LIST
        if not self.animListID in ACTIONABLE_LIST and not (self.animListID in SPECIAL_CANCEL_LIST and self.doPushback):
            self.specialBuffer = BUFFER_FRAMES
        else:
            self.specialBuffer = 0
            if self.isJump:
                if self.buttoncheck[1] or self.buttoncheck[0]: #Lets you specifically side special in the air!
                    self.set_new_anim_by_ID(get_anim_ID("SpecialS"))
                elif self.char_id == 3 and self.y > 80 : #Akuma Air Fireball
                    self.set_new_anim_by_ID(get_anim_ID("SpecialAirN"))
                return

            if self.buttoncheck[3] and not self.buttoncheck[2]:
                self.set_new_anim_by_ID(get_anim_ID("SpecialLw"))
            elif self.buttoncheck[1] or self.buttoncheck[0]:
                self.set_new_anim_by_ID(get_anim_ID("SpecialS"))
            else:
                self.set_new_anim_by_ID(get_anim_ID("SpecialN"))

                
    def throw(self):
        global ACTIONABLE_LIST
        global SPECIAL_CANCEL_LIST
        if self.animListID in ACTIONABLE_LIST and not self.isJump and not self.isCrouch:
            self.set_new_anim_by_ID(get_anim_ID("ThrowWhiff"))
            
    def throw_logic(self):
        global ACTIONABLE_LIST
        global SPECIAL_CANCEL_LIST
        if self.animListID != get_anim_ID("ThrowWhiff") and self.animListID != get_anim_ID("ThrowF"):
            return
        
        if self.doPushback and not self.hasHit and self.animListID == get_anim_ID("ThrowWhiff"):
            self.set_new_anim_by_ID(get_anim_ID("ThrowF")) # Goes into throw animation if the Grabbox hits
        
    
    def specialLw(self):
        if self.animListID != get_anim_ID("SpecialLw"):
            return
        
        direction_mul = 1.0
        if self.is_left:
            direction_mul = -1.0
        
        if self.char_id == 0: #all these are character specific behaviours
            if self.frame == 3:
                self.isJump = True
                self.jumpDir = 0
                self.moveYThisFrame = SPECIAL_LW_INIT_Y
                self.moveXThisFrame = SPECIAL_LW_INIT_X*direction_mul
            elif self.frame > 3:
                self.moveYThisFrame = self.lastmoveY - GRAVITY
                self.moveXThisFrame = self.lastmoveX * 0.8
        if self.char_id == 1:
            if self.frame == 4:
                self.isJump = True
                self.jumpDir = 0
                self.moveYThisFrame = SPECIAL_LW_INIT_Y
                self.moveXThisFrame = SPECIAL_LW_INIT_X*direction_mul
            elif self.frame > 4:
                self.moveYThisFrame = self.lastmoveY - GRAVITY
                self.moveXThisFrame = self.lastmoveX * 0.8
        if self.char_id == 2:
            if self.frame == 3:
                self.isJump = True
                self.jumpDir = 0
                self.moveYThisFrame = SPECIAL_LW_INIT_Y*0.9
                self.moveXThisFrame = SPECIAL_LW_INIT_X*direction_mul
            elif self.frame > 3:
                self.moveYThisFrame = self.lastmoveY - GRAVITY
                self.moveXThisFrame = self.lastmoveX * 0.7
        
        if self.char_id == 3: 
            if self.frame == 3:
                self.isJump = True
                self.jumpDir = 0
                self.moveYThisFrame = SPECIAL_LW_INIT_Y
                self.moveXThisFrame = SPECIAL_LW_INIT_X*direction_mul
            elif self.frame > 3:
                self.moveYThisFrame = self.lastmoveY - GRAVITY
                self.moveXThisFrame = self.lastmoveX * 0.8
            
    def specialS(self):
        direction_mul = 1.0
        if self.is_left:
            direction_mul = -1.0

        if self.animListID != get_anim_ID("SpecialS"):
            if self.char_id == 1:
                self.disableJostle = False
            return
        
        
        if self.char_id == 0: #all these are character specific behaviours
            if self.isJump:
                self.moveXThisFrame = SPECIAL_S_X*direction_mul*1.2
            else:
                self.moveXThisFrame = SPECIAL_S_X*direction_mul
        if self.char_id == 1:
            if self.isJump:
                self.moveXThisFrame = SPECIAL_S_X*direction_mul*1.2
                if self.frame < 2:
                    self.frame = 2
                if self.frame >= 2 and self.frame < 10:
                    self.disableJostle = True
                else:
                    self.disableJostle = False
                    if self.is_left == True and self.x < char_pos[-(self.playerNum)][0]:
                        self.is_left = False
                    if self.is_left == False and self.x > char_pos[-(self.playerNum)][0]:
                        self.is_left = True
            else:
                self.isCrouch = True
                if self.frame >= 2 and self.frame < 10:
                    self.moveXThisFrame = SPECIAL_S_X*direction_mul*1.2
                    self.disableJostle = True
                else:
                    self.disableJostle = False
                    if self.is_left == True and self.x < char_pos[-(self.playerNum)][0]:
                        self.is_left = False
                    if self.is_left == False and self.x > char_pos[-(self.playerNum)][0]:
                        self.is_left = True
        if self.char_id == 2:
            self.moveXThisFrame = SPECIAL_S_X*direction_mul*1.2
        if self.char_id == 3:
            if not self.doPushback:
                self.moveXThisFrame = SPECIAL_S_X*direction_mul
            if self.frame < 2 and not self.isJump:
                self.isJump = True
                self.jumpDir = 0.0
                self.moveYThisFrame = 45.0

    def specialN(self):
        # contains the projectile logic
        if self.animListID == get_anim_ID("SpecialS") and self.char_id == 3:
            return

        if self.animListID != get_anim_ID("SpecialN") and self.animListID != get_anim_ID("SpecialAirN"):
            self.hadouTimer = 0
            return
        
        if self.hadouTimer >= 1: # If you've hit the opponent with your projectile, switch to the version of the anim where the projectile sprite doesnt exist
            if self.isJump and self.char_id == 3:
                self.set_new_anim_by_ID(get_anim_ID("SpecialAirNEmpty"), self.frame)
            else:
                self.set_new_anim_by_ID(get_anim_ID("SpecialNEmpty"), self.frame)
        if self.doPushback:
            self.hadouTimer += 1
        
        if self.animListID == get_anim_ID("SpecialAirN"):
            if self.frame < 4:
                self.moveYThisFrame = 0
                self.moveXThisFrame*= 0.5
            
                    
    def set_pushback(self):
        #Prevents these moves having pushback per character
        if self.animListID == get_anim_ID("Heavy") and self.char_id == 0:
            return
        if self.animListID == get_anim_ID("AttackLw") and self.char_id == 2:
            return
        if self.animListID == get_anim_ID("HeavyLw") and self.char_id == 2:
            return
        if self.animListID == get_anim_ID("Attack") and self.char_id == 3:
            return
        if self.animListID == get_anim_ID("Heavy") and self.char_id == 3:
            return
        

        if self.animListID in [get_anim_ID("AttackLw"), get_anim_ID("Attack"), get_anim_ID("Heavy"), get_anim_ID("HeavyLw"), get_anim_ID("ThrowF")] or (
            (self.animListID in [get_anim_ID("SpecialS")] and self.char_id == 3)
        ):
            side_mul = 1
            if self.is_left:
                side_mul = -1

            if self.doPushback == True:
                self.moveXThisFrame = PUSHBACK * side_mul * -1
                if self.animListID == get_anim_ID("ThrowF"):
                   self.moveXThisFrame *= 0.7 
                
                if self.animListID == get_anim_ID("SpecialS") and self.char_id == 3:
                    self.moveXThisFrame *= 0.8


                    
    def dash(self):
        global ACTIONABLE_LIST
        if self.isJump or self.isCrouch or self.isHitstun:
            return
        
        side_mul = 1
        if self.is_left:
            side_mul = -1

        if self.animListID == get_anim_ID("ForwardDash"):
            if self.lastmoveX != 0:
                self.moveXThisFrame = self.lastmoveX - (stats.FDASH_DECEL[self.char_id]*side_mul)
                
                if abs(self.lastmoveX) - stats.FDASH_DECEL[self.char_id] < 0:
                    self.moveXThisFrame = 0

        if self.animListID == get_anim_ID("BackDash"):
            if self.lastmoveX != 0:
                self.moveXThisFrame = self.lastmoveX + (stats.BDASH_DECEL[self.char_id]*side_mul)

                if abs(self.lastmoveX) - stats.BDASH_DECEL[self.char_id] < 0:
                    self.moveXThisFrame = 0


    
    def check_correct_side(self):
        global ACTIONABLE_LIST
        if (self.isJump == False and self.animListID in ACTIONABLE_LIST) or self.animListID == get_anim_ID("JumpSquat"):
            #Flips you around and puts you into the default animation when crossed up
            if self.is_left == True and self.x < char_pos[-(self.playerNum)][0]:
                self.is_left = False
                self.set_new_anim_by_ID()
            if self.is_left == False and self.x > char_pos[-(self.playerNum)][0]:
                self.is_left = True
                self.set_new_anim_by_ID()
            if self.x == char_pos[-(self.playerNum)][0]:
                if self.playerNum == 2:
                    self.is_left = True
                    self.set_new_anim_by_ID()
                else:
                    self.is_left = False
                    self.set_new_anim_by_ID()
                
    def check_block(self):
        #if self.isJump:
            #self.isBlocking = False
        if self.isHitstun:
            return
        if self.hitstunFrames > 0:
            return
        if not (self.animListID in ACTIONABLE_LIST or self.animListID in BLOCKING_LIST):
            self.isBlocking = False
            return
        
        if not self.is_left:
            if self.buttoncheck[0] and not self.buttoncheck[1]:
                self.isBlocking = True
            else:
                self.isBlocking = False
        else:
            if self.buttoncheck[1] and not self.buttoncheck[0]:
                self.isBlocking = True
            else:
                self.isBlocking = False
    
    def runCpuQueue(self):
        if self.isHitstun:
            self.cpuQueue = []
            return
        
        if len(self.cpuQueue) < 1: #If queue is empty, try and fill it up again
            if self.animListID in ACTIONABLE_LIST and not self.isLeaveBlockstun:
                cpu_data.check_movement(self, players_x[self.playerNum - 1], players_x[-self.playerNum], players_y[self.playerNum - 1], players_y[-self.playerNum])
                if self.cpuQueue[0] in [get_anim_ID("ForwardDash"), get_anim_ID("Backdash")]:
                    self.cpuQueue.insert(0, cpu_data.WAIT)
                    self.cpuQueue.insert(0, cpu_data.WAIT)
                    self.cpuQueue.insert(0, cpu_data.WAIT)
            else:
                if self.animListID in [get_anim_ID("WalkF"), get_anim_ID("WalkB")]:
                    self.set_new_anim_by_ID()
                return
            
        if self.animListID == get_anim_ID("WalkF"): #Ensures they walk properly!
                if self.is_left:
                    self.moveXThisFrame = -stats.WALK_SPEED[self.char_id]
                else:
                    self.moveXThisFrame = stats.WALK_SPEED[self.char_id]
        if self.animListID == get_anim_ID("WalkB"):
                if self.is_left:
                    self.moveXThisFrame = stats.WALK_SPEED[self.char_id]
                else:
                    self.moveXThisFrame = -stats.WALK_SPEED[self.char_id]
                    
        next_command = self.cpuQueue[0]
        if next_command == self.animListID: #If the command is repeated just keep on doing what you been doing
            self.cpuQueue.pop(0)
            return
        
        if self.animListID in SPECIAL_CANCEL_LIST and self.doPushback:
                other = self.accessOtherPlayer[self.playerNum - 1]
                if not other.isBlockstun:
                    if random.randint(0, 100) < 30:
                        if not self.isJump:
                            self.set_new_anim_by_ID(cpu_data.SPECIAL_CANCEL[self.char_id])
                        else:
                            self.set_new_anim_by_ID(get_anim_ID("SpecialS"))
                else:
                    rand_val = random.randint(0, 100)
                    if rand_val < 5:
                        if not self.isJump:
                            self.set_new_anim_by_ID(cpu_data.SPECIAL_CANCEL_SAFE[self.char_id])
                        else:
                            self.set_new_anim_by_ID(get_anim_ID("SpecialS"))
                    elif rand_val < 8:
                        if not self.isJump:
                            self.set_new_anim_by_ID(cpu_data.SPECIAL_CANCEL[self.char_id])
                        else:
                            self.set_new_anim_by_ID(get_anim_ID("SpecialS"))
                    
        if self.animListID in ACTIONABLE_LIST and ((not self.isJump and next_command in cpu_data.GROUND_MOVE) or (self.isJump and next_command in cpu_data.AIR_MOVE)):
            if next_command == get_anim_ID("ForwardDash"):
                self.set_new_anim_by_ID(next_command)
                self.cpuQueue.pop(0)
                if self.is_left:
                    self.moveXThisFrame = -stats.FDASH_SPEED[self.char_id]
                else:
                    self.moveXThisFrame = stats.FDASH_SPEED[self.char_id]
            elif next_command == get_anim_ID("BackDash"):
                self.set_new_anim_by_ID(next_command)
                self.cpuQueue.pop(0)
                if self.is_left:
                    self.moveXThisFrame = stats.BDASH_SPEED[self.char_id]
                else:
                    self.moveXThisFrame = -stats.BDASH_SPEED[self.char_id]
            elif next_command == get_anim_ID("WalkF"):
                self.set_new_anim_by_ID(next_command)
                self.cpuQueue.pop(0)
                if self.is_left:
                    self.moveXThisFrame = -stats.WALK_SPEED[self.char_id]
                else:
                    self.moveXThisFrame = stats.WALK_SPEED[self.char_id]
            elif next_command == get_anim_ID("WalkB"):
                self.set_new_anim_by_ID(next_command)
                self.cpuQueue.pop(0)
                if self.is_left:
                    self.moveXThisFrame = stats.WALK_SPEED[self.char_id]
                else:
                    self.moveXThisFrame = -stats.WALK_SPEED[self.char_id]
            else:
                self.set_new_anim_by_ID(next_command)
                self.cpuQueue.pop(0)
            return
    
    def update(self): #Once per player frame
            global PUSHBOXES
            global PUSHING_FORCE
            global force_hit_now

            players_x[self.playerNum - 1] = self.x
            players_y[self.playerNum - 1] = self.y

            if force_hit_now and not self.hasHit and not hitbox_properties[-(self.playerNum)] == None:
                force_hit_now = False
                #print("Has Forced a hit")
                other = self.accessOtherPlayer[self.playerNum - 1]
                other.maxHitstun = hitbox_properties[-(self.playerNum)][2]
                self.start_hitstun()

            self.check_correct_side()
            self.check_block()
            self.check_is_hurt()
            self.check_is_hitting()
            self.hitstun_movement()
            self.air()
            self.dash()


            if self.readLog:
                self.buttoncheck = self.log[self.logFrame]
                self.logFrame += 1
                if self.logFrame >= self.logLength:
                    self.logFrame = 0
            elif self.isCpu:
                self.buttoncheck = [False,False,False,False,False,False,False]
            else:
                self.buttoncheck = [keyboard.is_pressed(self.controls[0]),keyboard.is_pressed(self.controls[1]),
                                    keyboard.is_pressed(self.controls[2]), keyboard.is_pressed(self.controls[3]),
                                    keyboard.is_pressed(self.controls[4]), keyboard.is_pressed(self.controls[5]),
                                    keyboard.is_pressed(self.controls[6])
                ]
            
            if self.isCpu:
                self.runCpuQueue()

            #Logs player 1 stuff
            if self.playerNum == 1:
                try:
                    f = open("log.txt","a")
                    f.write(str(self.buttoncheck))
                    f.write("\n")
                    f.close()
                except Exception as exc:
                    print(exc)
                    sys.exit()

            #Move specific code
            self.HeavyAir()
            self.attackLw()
            self.heavyN()
            self.specialLw()
            self.specialS()
            self.specialN()
            self.throw_logic()

            self.animate()
            
            if not self.isCpu:
                if self.buttoncheck[0] and not self.buttoncheck[1]:
                    self.left()
                elif self.animListID == get_anim_ID("WalkF") and (self.is_left != False) or (self.animListID == get_anim_ID("WalkB") and (self.is_left != True )):
                    if  not self.isHitstun:
                        self.set_new_anim_by_ID() #Resets you to standing when left no longer pressed
            
                if self.buttoncheck[0] and not self.buttoncheck[1]:
                    self.leftPressed = True
                else:
                    self.leftPressed = False

                if self.buttoncheck[1] and not self.buttoncheck[0]:
                    self.right()
                elif (self.animListID == get_anim_ID("WalkF") and (self.is_left != True)) or (self.animListID == get_anim_ID("WalkB") and (self.is_left != False )):
                    self.set_new_anim_by_ID() #Resets you to standing when right no longer pressed
                
                
            if self.buttoncheck[1] and not self.buttoncheck[0]:
                self.rightPressed = True #Set so it can be used to check if the button has just been pressed
            else:
                self.rightPressed = False

                
            if self.buttoncheck[3] and not self.buttoncheck[2]:
                self.down()
            elif self.isCrouch:
                self.uncrouch()
            if (self.buttoncheck[2] and not self.buttoncheck[3]) or self.jumpBuffer > 0:
                self.up()
                
            if (self.buttoncheck[4] and self.buttoncheck[5] and not self.buttoncheck[6]) and not(self.buttoncheck[0] or self.buttoncheck[1]):
                self.throw()

            if (self.buttoncheck[4] and not self.buttoncheck[5] and not self.buttoncheck[6] and not self.attackPressed) or self.attackBuffer > 0:
                self.attackPressed = True
                self.attack()
                
            if (self.buttoncheck[6] and not self.buttoncheck[4] and not self.buttoncheck[5] and not self.specialPressed) or self.specialBuffer > 0:
                self.specialPressed = True
                self.special()

            if (self.buttoncheck[5] and not self.buttoncheck[4] and not self.buttoncheck[6] and not self.heavyPressed) or self.heavyBuffer > 0:
                self.heavyPressed = True
                self.heavy()
                
            
            if self.attackBuffer > 0:
                self.attackBuffer -= 1
                
            if self.specialBuffer > 0:
                self.specialBuffer -= 1
                
            if self.jumpBuffer > 0:
                self.jumpBuffer -= 1
                
            if self.heavyBuffer > 0:
                self.heavyBuffer -= 1
            
            if self.start_blocking_now > 0:
                self.start_blocking_now -= 1
                
            if self.hitstunFrames > 0:
                #print("still in hitstun")
                self.hitstunFrames -= 1
                
            if self.backdashTimer > 0:
                self.backdashTimer -= 1
            if self.forwarddashTimer > 0:
                self.forwarddashTimer -= 1

            if self.training_settings[4] != 0 and self.playerNum == 2:
                if (self.isHitstun and self.training_settings[3] == 0) or self.isBlockstun:
                    self.isLeaveBlockstun = True
                elif self.isLeaveBlockstun and self.animListID in ACTIONABLE_LIST :
                    if self.training_settings[4] == 1 and not self.isJump:
                        #print("force jab")
                        self.set_new_anim_by_ID(get_anim_ID("Attack"))
                        self.isLeaveBlockstun = False
                    elif self.training_settings[4] == 2 and not self.isJump:
                        #print("force jab")
                        self.set_new_anim_by_ID(get_anim_ID("AttackLw"))
                        self.isLeaveBlockstun = False
                    elif self.training_settings[4] == 3 and not self.isJump:
                        #print("force jab")
                        self.set_new_anim_by_ID(get_anim_ID("Heavy"))
                        self.isLeaveBlockstun = False
                    elif self.training_settings[4] == 4 and not self.isJump:
                        #print("force jab")
                        self.set_new_anim_by_ID(get_anim_ID("HeavyLw"))
                        self.isLeaveBlockstun = False
                    elif self.training_settings[4] == 5 and not self.isJump:
                        #print("force dp")
                        self.set_new_anim_by_ID(get_anim_ID("SpecialLw"))
                        self.isLeaveBlockstun = False
                    elif self.training_settings[4] == 6 and not self.isJump:
                        #print("force dp")
                        self.set_new_anim_by_ID(get_anim_ID("SpecialN"))
                        self.isLeaveBlockstun = False
                    elif self.training_settings[4] == 7 and not self.isJump:
                        #print("force dp")
                        self.set_new_anim_by_ID(get_anim_ID("SpecialS"))
                        self.isLeaveBlockstun = False
                    elif self.training_settings[4] == 8 and not self.isJump:
                        #print("force backdash")
                        self.set_new_anim_by_ID(get_anim_ID("BackDash"))
                        self.isLeaveBlockstun = False
                        if self.is_left:
                            self.moveXThisFrame = stats.BDASH_SPEED[self.char_id]
                        else:
                            self.moveXThisFrame = -stats.BDASH_SPEED[self.char_id]
            if self.isCpu:
                if self.isBlockstun:
                    self.isLeaveBlockstun = True
                elif self.isLeaveBlockstun and self.animListID in ACTIONABLE_LIST and not self.isJump:
                    rng = random.randint(0, 100)
                    if rng < 35:
                        self.set_new_anim_by_ID(cpu_data.JAB[self.char_id])
                    elif rng < 45:
                        self.set_new_anim_by_ID(cpu_data.DP[self.char_id])
                    elif rng < 55:
                        self.set_new_anim_by_ID(cpu_data.DP2[self.char_id])
                    elif rng < 60:
                        self.set_new_anim_by_ID(cpu_data.GRAB)
                    elif rng < 62:
                        self.set_new_anim_by_ID(get_anim_ID("BackDash"))
                        if self.is_left:
                            self.moveXThisFrame = stats.BDASH_SPEED[self.char_id]
                        else:
                            self.moveXThisFrame = -stats.BDASH_SPEED[self.char_id]
                    
                    self.isLeaveBlockstun = False

            if self.hitstunFrames <= 0:
                self.isHitstun = False
                self.isBlockstun = False
                if self.y < 5:
                    self.y = 0
            

            if not self.isHitstun:
                self.maxHitstun = False

            if not self.buttoncheck[4]:
                self.attackPressed = False

            if not self.buttoncheck[5]:
                self.heavyPressed = False

            if not self.buttoncheck[6]:
                self.specialPressed = False
            
            self.set_pushback()


            if True:#self.moveXThisFrame != 0 or self.moveYThisFrame != 0:
                x = self.x
                y = self.y
                newXVal = x
                newYVal = y
                #print(f"{newXVal}, {newYVal}")

                #Forces players to stay within fighting area
                if abs(x+self.moveXThisFrame) < BOX_SIZE[0]-4:
                    newXVal = x+self.moveXThisFrame
                
                newYVal = y+self.moveYThisFrame

                #Pushbox
                left_pushbox = (char_pos[-(self.playerNum)][0] - PUSHBOXES[0]) - self.x  < 105 and self.is_left == False
                right_pushbox = self.x - (char_pos[-(self.playerNum)][0] + PUSHBOXES[0])  < 105 and self.is_left
                top_pushbox = self.y - (char_pos[-(self.playerNum)][1] + PUSHBOXES[2])  < 90
                bottom_pushbox =  (char_pos[-(self.playerNum)][1] + PUSHBOXES[1]) - self.y  < 105
                #if top_pushbox and bottom_pushbox:
                    #print(f"same height: [{(char_pos[-(self.playerNum)][0] - PUSHBOXES[0]) - self.x}, {self.x - (char_pos[-(self.playerNum)][0] + PUSHBOXES[0])}]")
                    #print(f"X Pos for other one: {char_pos[-(self.playerNum)][0]}")
                if (left_pushbox or right_pushbox) and (top_pushbox and bottom_pushbox) and not self.disableJostle:
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

                if self.x > BOX_SIZE[0]-4:
                    self.x = BOX_SIZE[0]-4
                if self.x < -BOX_SIZE[0] +4:
                    self.x = -BOX_SIZE[0] +4
                if self.y < 0:
                    self.y = 0
                self.turtle.setpos(self.x, self.y)
                self.lastmoveX = newXVal - x
                self.lastmoveY = newYVal - y
                #print(f"{self.lastmoveX}, {self.lastmoveY}")
                self.moveXThisFrame = 0.0
                self.moveYThisFrame = 0.0

            
            #self.update_hit_hurt()

            char_pos[self.playerNum - 1][0] = self.x 
            char_pos[self.playerNum - 1][1] = self.y 
            #print(char_pos)

class battleUI:
    def __init__(self, screen, p1Turtle, p2Turtle, isTraining):
        self.screen = screen
        self.p1 = p1Turtle
        self.p2 = p2Turtle
        self.p1HP = turtle.Turtle()
        self.p2HP = turtle.Turtle()
        self.p1Icon = turtle.Turtle()
        self.p2Icon = turtle.Turtle()
        self.isTraining = isTraining
        self.youWin = turtle.Turtle()
        self.p1HpPos = [-190,150]
        self.p2HpPos = [180,150]
        self.p1Icon.penup()
        self.p2Icon.penup()
        self.p1Icon.hideturtle()
        self.p2Icon.hideturtle()
        self.p1Icon.goto(-370, 185)
        self.p2Icon.goto(360, 185)
        self.p1HP.penup()
        self.p2HP.penup()
        self.youWin.penup()
        screen.tracer(0)
        self.youWin.hideturtle()
        self.p1HP.hideturtle()
        self.p2HP.hideturtle()
        self.p1HP.goto(self.p1HpPos[0], self.p1HpPos[1])
        self.p2HP.goto(self.p2HpPos[0], self.p2HpPos[1])
        self.youWin.goto(0, 0)
        screen.update()
        screen.tracer(10)

        self.hp_bar_length = 300
        self.hp_start_x = 30
        self.hp_start_y = 175
        self.hp_bar_thickness = 2*SCALE
    
    def clear(self): #Clears the screen
        self.p1HP.clear()
        self.p2HP.clear()
        self.youWin.clear()
        self.p1Icon.clear()
        self.p2Icon.clear()

    def update_healthbar(self): #Updates health bar based on their health remaining

        p1_hp_length = (self.p1.hp/stats.HEALTH[self.p1.char_id]) * self.hp_bar_length
        p2_hp_length = (self.p2.hp/stats.HEALTH[self.p2.char_id]) * self.hp_bar_length
        offset = -5
        self.screen.tracer(0)
        self.p1HP.clear()
        self.p1HP.penup()
        self.p1HP.goto(-self.hp_start_x+offset, self.hp_start_y  - self.hp_bar_thickness)
        if self.p1.hp > 0:
            self.p1HP.fillcolor("cyan")
            self.p1HP.begin_fill()
            self.p1HP.goto(-self.hp_start_x +offset, self.hp_start_y + self.hp_bar_thickness)
            self.p1HP.goto(-(self.hp_start_x + p1_hp_length) +offset, self.hp_start_y + self.hp_bar_thickness)
            self.p1HP.goto(-(self.hp_start_x + p1_hp_length) +offset, self.hp_start_y  - self.hp_bar_thickness)
            self.p1HP.goto(-(self.hp_start_x)+offset, self.hp_start_y  - self.hp_bar_thickness)
            self.p1HP.end_fill()
        self.p1HP.goto(-(self.hp_start_x+ (self.hp_bar_length * 0.5))+offset, self.hp_start_y)
        self.p1HP.shape("sprites/hpbar.gif")
        self.p1HP.stamp()

        self.p2HP.clear()
        self.p2HP.penup()
        if self.p2.hp > 0:
            self.p2HP.goto(self.hp_start_x+offset, self.hp_start_y)
            self.p2HP.fillcolor("red")
            self.p2HP.begin_fill()
            self.p2HP.goto(self.hp_start_x+offset, self.hp_start_y + self.hp_bar_thickness)
            self.p2HP.goto((self.hp_start_x + p2_hp_length)+offset, self.hp_start_y + self.hp_bar_thickness)
            self.p2HP.goto((self.hp_start_x + p2_hp_length)+offset, self.hp_start_y  - self.hp_bar_thickness)
            self.p2HP.goto((self.hp_start_x)+offset, self.hp_start_y  - self.hp_bar_thickness)
            self.p2HP.end_fill()
        self.p2HP.goto((self.hp_start_x+ (self.hp_bar_length * 0.5))+offset, self.hp_start_y)
        self.p2HP.shape("sprites/hpbar.gif")
        self.p2HP.stamp()
        
        self.p1Icon.clear()
        self.p2Icon.clear()
        self.p1Icon.shape(f"sprites/F0{self.p1.char_id}_Head.gif")
        if self.p1.alt != 0:
            self.p1Icon.shape(f"sprites{self.p1.alt+1}/F0{self.p1.char_id}_Head.gif")
        else:
            self.p1Icon.shape(f"sprites/F0{self.p1.char_id}_Head.gif")
        self.p1Icon.stamp()
        if self.p2.alt != 0:
            self.p2Icon.shape(f"reverse_sprites{self.p2.alt+1}/F0{self.p2.char_id}_Head.gif")
        else:
            self.p2Icon.shape(f"reverse_sprites/F0{self.p2.char_id}_Head.gif")
        self.p2Icon.stamp()
        self.screen.update()
        self.screen.tracer(10)
    
    def update(self):
        self.update_healthbar()
        if self.p1.hp <= 0 or self.p2.hp <= 0:
            player = 1
            if self.p2.hp > self.p1.hp:
                player = 2
            self.youWin.shape(f"sprites/p{player}_win.gif") #Hooray
            self.youWin.stamp()

chars = []
alternates = []
cpus = False

def rematch(x,y): #Another on click method for turtle screen awesome
    global chars
    global alternates
    if abs(x) > 25:
        return
    if y > 13 and y < 40:
        menu.run(True,chars,alternates,cpus)
    if y > -60 and y < -33:
        menu.run()

def pause_update(pause_turtle, controls, training_settings:list):
    global chars
    shape = pause_turtle.shape()
    up = [controls[0][2], controls[1][2]]
    down = [controls[0][3], controls[1][3]]
    accept = [controls[0][4], controls[1][4]]
    if not training_settings[0]:
        if shape in ["menu/pause_1.gif", "menu/pause_2.gif", "menu/pause_3.gif"]:
            if keyboard.is_pressed(up[0]) or keyboard.is_pressed(up[1]):
                if shape == "menu/pause_2.gif":
                    pause_turtle.shape("menu/pause_1.gif")
                    time.sleep(0.2)
                if shape == "menu/pause_3.gif":
                    pause_turtle.shape("menu/pause_2.gif")
                    time.sleep(0.2)
            if keyboard.is_pressed(down[0]) or keyboard.is_pressed(down[1]):
                if shape == "menu/pause_1.gif":
                    pause_turtle.shape("menu/pause_2.gif")
                    time.sleep(0.2)
                if shape == "menu/pause_2.gif":
                    pause_turtle.shape("menu/pause_3.gif")
                    time.sleep(0.2)
            if keyboard.is_pressed(accept[0]) or keyboard.is_pressed(accept[1]):
                if shape == "menu/pause_1.gif":
                    pause_turtle.shape("menu/movelist.gif")
                if shape == "menu/pause_2.gif":
                    return 2
                if shape == "menu/pause_3.gif":
                    menu.run()
    else:
        if shape in ["menu/training_pause_1.gif", "menu/training_pause_2.gif", "menu/training_pause_3.gif"]:
            if keyboard.is_pressed(up[0]) or keyboard.is_pressed(up[1]):
                if shape == "menu/training_pause_2.gif":
                    pause_turtle.shape("menu/training_pause_1.gif")
                    time.sleep(0.2)
                if shape == "menu/training_pause_3.gif":
                    pause_turtle.shape("menu/training_pause_2.gif")
                    time.sleep(0.2)
            if keyboard.is_pressed(down[0]) or keyboard.is_pressed(down[1]):
                if shape == "menu/training_pause_1.gif":
                    pause_turtle.shape("menu/training_pause_2.gif")
                    time.sleep(0.2)
                if shape == "menu/training_pause_2.gif":
                    pause_turtle.shape("menu/training_pause_3.gif")
                    time.sleep(0.2)
            if keyboard.is_pressed(accept[0]) or keyboard.is_pressed(accept[1]):
                if shape == "menu/training_pause_1.gif":
                    pause_turtle.shape("menu/training_menu.gif")
                    return 1
                if shape == "menu/training_pause_2.gif":
                    return 2
                if shape == "menu/training_pause_3.gif":
                    menu.run()

class setting_icon:
    def __init__(self, pos:int, list_update:list, list_num:int, screen):
        self.pos = pos
        self.turtle = turtle.Turtle()
        self.turtle.penup()
        self.turtle.goto(0, pos)
        self.list_update = list_update
        self.list_num = list_num
        self.turtle.shape(self.list_update[list_num])
        self.screen = screen
    
    def onclick_update(self, x, y):
        self.list_num += 1
        if self.list_num >= len(self.list_update):
            self.list_num = 0
        self.turtle.shape(self.list_update[self.list_num])
        self.screen.update()
        #print("update")

class save_icon:
    def __init__(self, pos:int, turtle_list:list, screen, characters:list):
        self.pos = pos
        self.turtle = turtle.Turtle()
        self.turtle.penup()
        self.turtle.goto(0, pos)
        self.turtle_list = turtle_list
        self.turtle.shape("menu/training_save.gif")
        self.screen = screen
        self.characters = characters
    
    def onclick_update(self, x, y):
        new_training_settings = [True]
        new_training_settings.append(bool(self.turtle_list[0].list_num))
        new_training_settings.append(bool(self.turtle_list[1].list_num))
        new_training_settings.append(int(self.turtle_list[2].list_num))
        new_training_settings.append(int(self.turtle_list[3].list_num))
        #print(new_training_settings)
        run(new_training_settings, self.characters)


def run(training_settings=[False,False,False,0,0], character=[0,0], alts=[0,0], cpu=False):
    global chars
    global alternates
    global cpus
    global is_ditto
    chars = character
    alternates = alts
    cpus = cpu
    controlsList = get_controls_from_txt()
    turtle.TurtleScreen._RUNNING=True
    screen = turtle.Screen()
    screen.setup(SCREEN_WIDTH, SCREEN_HEIGHT)
    screen.title("Shotos")
    screen.bgcolor("white")
    screen.clearscreen()
    #[Is in training mode, Enable hitboxes, Enable Frame by Frame, Blocking Mode, Reversal]
    #screen.delay(17)
    f = open("log.txt","w")
    f.write("")
    f.close()
    load_list = ["sprites", "reverse_sprites"]
    for i in alts:
        if i != 0:
            load_list.append(f"sprites{i+1}")
            load_list.append(f"reverse_sprites{i+1}")
    print(load_list)
    for i in load_list:
        for root, dirs, files in os.walk(i):
                #print(files)
                for filename in files:
                    skip = True
                    for x in character:
                        if f"F0{x}_" in filename:
                            skip = False
                    for x in ["hpbar","win","Head"]:
                        if x in filename:
                            skip = False
                    if skip:
                        continue
                    if filename.endswith(".gif"):
                        #print(filename)
                        #Handles scaling up and stuff
                        larger = PhotoImage(file=f"{i}/{filename}").zoom(SCALE, SCALE)
                        screen.addshape(f"{i}/{filename}", Shape("image", larger))
        for root, dirs, files in os.walk("menu"):
            for filename in files:
                if filename.endswith(".gif"):
                    screen.addshape(f"menu/{filename}")
    
    if character[0] == character[1]:
        is_ditto = True
    else:
        is_ditto = False

    screen.tracer(0)
    if training_settings[1] and training_settings[0]: #Hitbox/hurtbox drawing!
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
    

    #Initialising players
    p1 = player(
        1,
        -150, 0,
        #["a", "d", "w", "s", "f", "g", "h"],
        controlsList[0],
        False,
        training_settings,
        character[0],
        alts[0]
    )
    p2 = player(
        2,
        150, 0,
        #["left", "right", "up", "down", ".", "/", "shift"],
        controlsList[1],
        True,
        training_settings,
        character[1],
        alts[1]
    )
    if cpu:
        p2.isCpu = True

    accessOtherPlayer = [p2, p1]
    p1.update_other_list(accessOtherPlayer)
    p2.update_other_list(accessOtherPlayer)

    youwin = False

    ui = battleUI(screen, p1, p2, training_settings[0])
    
    ground = turtle.Turtle()
    ground.penup()
    ground.pensize(5)
    ground.goto(-1000,-125)
    ground.pendown()
    ground.goto(1000,-125)
    ground.penup()

    if training_settings[2]:
        frame_advance = turtle.Turtle()
        frame_advance.penup()
        frame_advance.goto(0,-150)
        frame_advance.shape("menu/frame_advance.gif")

    pause_ui = turtle.Turtle()
    pause_ui.penup()
    pause_ui.goto(-4,4)
    pause_ui.hideturtle()
    if not training_settings[0]:
        pause_ui.shape("menu/pause_1.gif")
    else:
        pause_ui.shape("menu/training_pause_1.gif")


    ui.update()
    p1.update()
    p2.update()
    p1.update()
    p2.update()
    screen.tracer(10)
    screen.update()
    paused = False
    pause_release = False

    prev_delay = 0.0
    p1HPRestore = 0
    p2HPRestore = 0
    while youwin == False:
            try:
                if prev_delay > FRAME_LENGTH*2:
                    pass
                    #print("Frame Skip! Performance aint looking good")

                start = time.time()
                turn_order = bool(random.getrandbits(1))
                if not paused and (((training_settings[2] and  keyboard.is_pressed("space")) or (not training_settings[2]))):
                    pause_ui.hideturtle()
                    if training_settings[0]:
                        pause_ui.shape("menu/training_pause_1.gif")
                    else:
                        pause_ui.shape("menu/pause_1.gif")
                    if not (keyboard.is_pressed("escape") or keyboard.is_pressed("backspace")):
                        pause_release = True
                    if (keyboard.is_pressed("escape") or keyboard.is_pressed("backspace")) and pause_release:
                        pause_release = False
                        paused = True
                    ui.update()
                    if turn_order:
                        p1.update()
                        p2.update()
                    else:
                        p2.update()
                        p1.update()
                    if training_settings[0] and training_settings[1]:
                        draw_boxes(screen, p1_hurtbox_draw, p1_hurtbox_draw2, p1_hitbox_draw, p2_hurtbox_draw, p2_hurtbox_draw2, p2_hitbox_draw)
                elif paused:
                    pause_ui.showturtle()
                    ui.clear()
                    if training_settings[0] and training_settings[1]:
                        p1_hurtbox_draw.clear()
                        p1_hurtbox_draw2.clear()
                        p1_hitbox_draw.clear()
                        p2_hurtbox_draw.clear()
                        p2_hurtbox_draw2.clear()
                        p2_hitbox_draw.clear()
                    screen.update()
                    if not (keyboard.is_pressed("escape") or keyboard.is_pressed("backspace")):
                        pause_release = True
                    if (keyboard.is_pressed("escape") or keyboard.is_pressed("backspace")) and pause_release:
                        pause_release = False
                        paused = False
                    pause_val = pause_update(pause_ui, controlsList, training_settings)
                    if pause_val == 2:
                        paused = False
                    if pause_val == 1:
                        screen.clearscreen()
                        screen.tracer(0)
                        block = ["menu/block_0.gif", "menu/block_1.gif", "menu/block_2.gif"]
                        hitbox = ["menu/hitbox_false.gif", "menu/hitbox_true.gif"]
                        frame = ["menu/frame_false.gif", "menu/frame_true.gif"]
                        reversal = [
                            "menu/reversal_0.gif", "menu/reversal_1.gif", "menu/reversal_2.gif", "menu/reversal_3.gif", "menu/reversal_4.gif", "menu/reversal_5.gif",
                            "menu/reversal_6.gif", "menu/reversal_7.gif", "menu/reversal_8.gif"
                        ]
                        bg = turtle.Turtle()
                        bg.shape("menu/training_menu.gif")
                        setting_hitbox = setting_icon(90, hitbox, int(training_settings[1]), screen)
                        setting_frame = setting_icon(30, frame, int(training_settings[2]), screen)
                        setting_block = setting_icon(-30, block, int(training_settings[3]), screen)
                        setting_reversal = setting_icon(-90, reversal, int(training_settings[4]), screen)
                        save = save_icon(-150, [setting_hitbox,setting_frame,setting_block,setting_reversal], screen, character)
                        screen.update()
                        screen.tracer(10)
                        setting_hitbox.turtle.onclick(setting_hitbox.onclick_update)
                        setting_frame.turtle.onclick(setting_frame.onclick_update)
                        setting_block.turtle.onclick(setting_block.onclick_update)
                        setting_reversal.turtle.onclick(setting_reversal.onclick_update)
                        save.turtle.onclick(save.onclick_update)
                        screen.mainloop()
                elif training_settings[2] and not keyboard.is_pressed("space"):
                    pause_ui.hideturtle()
                    if training_settings[0]:
                        pause_ui.shape("menu/training_pause_1.gif")
                    else:
                        pause_ui.shape("menu/pause_1.gif")
                    if not (keyboard.is_pressed("escape") or keyboard.is_pressed("backspace")):
                        pause_release = True
                    if (keyboard.is_pressed("escape") or keyboard.is_pressed("backspace")) and pause_release:
                        pause_release = False
                        paused = True
                    ui.update()
                end = time.time()
                new_delay = (end-start)*10**3
                #print(f"Time taken: {new_delay}ms, normalise: {FRAME_LENGTH - (new_delay)}ms")
                if (new_delay/1000) < FRAME_LENGTH/1000:
                    time.sleep(FRAME_LENGTH/1000 - (new_delay/1000))
                prev_delay = new_delay

                p1.hp -= p1.decreaseHp
                p2.hp -= p2.decreaseHp
                if training_settings[0] and (p1.hp < 1 or p1HPRestore >= HP_RESTORE_DURATION):
                    p1.hp = stats.HEALTH[p1.char_id]
                    p1HPRestore = 0
                if training_settings[0] and (p2.hp < 1 or p2HPRestore >= HP_RESTORE_DURATION):
                    p2.hp = stats.HEALTH[p2.char_id]
                    p2HPRestore = 0
                if not(training_settings[2] and not keyboard.is_pressed("space")):
                    if p1.decreaseHp == 0:
                        p1HPRestore += 1
                    else:
                        p1HPRestore = 0
                    if p2.decreaseHp == 0:
                        p2HPRestore += 1
                    else:
                        p2HPRestore = 0
                
                p1.decreaseHp = 0
                p2.decreaseHp = 0
                if p1.hp <= 0 or p2.hp <= 0:
                    youwin = True
            except Exception as exc:
                print(exc)
                sys.exit()

    ui.update()
    screen.update()
    time.sleep(2)
    screen.tracer(0)
    resetti = turtle.Turtle()
    resetti.shape("menu/rematch.gif")
    screen.update()
    screen.onscreenclick(rematch)
    screen.mainloop()     