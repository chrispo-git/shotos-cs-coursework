import turtle
import os

#CONSTANTS
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 450


ANIMATION_LIST = [
    
    [ #Idle
        ["sprites/Idle_0.gif", [18,41,0,36], None]
    ]
]

#Format for Frames= ["sprites/frame.gif", [hurtbox x1, hurtbox x2, hurtbox y1, hurtbox y2], [hitbox x1, hitbox x2, hitbox y1, hitbox y2]]

ANIMATION_LIST_LABEL = [
    "Idle"
]
screen = turtle.Screen()
screen.setup(SCREEN_WIDTH, SCREEN_HEIGHT)
screen.bgcolor("white")
for root, dirs, files in os.walk("sprites"):
    print(files)
    for filename in files:
        if filename.endswith(".gif"):
            print(filename)
            screen.addshape(f"sprites/{filename}")


class player:
    def __init__(self, 
        playerNum: int,
        x: int, y: int,
        #sprite, frame, animList,
        controls: list #Controls expressed as [left, right, up, down, attack, special]
    ):
        self.playerNum = playerNum
        self.x = x
        self.y = y
        self.isJump = False
        self.isFaceRight = False

        #Sprite Init
        self.frame = 0
        self.animListID = 0
        self.sprite = ANIMATION_LIST[self.animListID][self.frame][0]

        #Turtle Setup
        
        self.turtle = turtle.Turtle()
        self.turtle.speed(0)
        self.turtle.penup()
        self.turtle.goto(x, y)
        self.turtle.shape(self.sprite)

p1 = player(
    1,
    0, 0,
    ["a", "d", "w", "s", "f", "g"]
)
screen.listen()
screen.mainloop()