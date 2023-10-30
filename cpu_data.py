
from util import get_anim_ID
import random
#Ranges for CPU to be wary of
JAB_RANGE = 25

POKE_RANGE = 35

THEIR_POKE_RANGE = [26,28,40]

PROJECTILE_RANGE = 93

THEIR_PROJECTILE_RANGE = [92,53,130]

#Moves types
JAB = [get_anim_ID("Attack"),get_anim_ID("AttackLw"),get_anim_ID("Attack")]
POKE = [get_anim_ID("AttackLw"),get_anim_ID("Attack"),get_anim_ID("AttackLw")]
POKE2 = [get_anim_ID("AttackLw"),get_anim_ID("Heavy"),get_anim_ID("AttackLw")]
ANTIAIR = [get_anim_ID("HeavyLw"),get_anim_ID("HeavyLw"),get_anim_ID("HeavyLw")]
BIG = [get_anim_ID("Heavy"),get_anim_ID("SpecialN"),get_anim_ID("Heavy")]
DP = [get_anim_ID("SpecialLw"),get_anim_ID("SpecialLw"),get_anim_ID("SpecialLw")]
DP2 = [get_anim_ID("SpecialLw"),get_anim_ID("SpecialS"),get_anim_ID("SpecialLw")]
TATSU = [get_anim_ID("SpecialS"),get_anim_ID("SpecialS"),get_anim_ID("SpecialS")]
PROJECTILE = [get_anim_ID("SpecialN"),get_anim_ID("SpecialN"),get_anim_ID("SpecialN")]

SPECIAL_CANCEL = [get_anim_ID("SpecialS"), get_anim_ID("SpecialN"), get_anim_ID("SpecialS")]
SPECIAL_CANCEL_SAFE = [get_anim_ID("None"), get_anim_ID("SpecialS"), get_anim_ID("SpecialS")]

WALK_F = get_anim_ID("WalkF")
WALK_B = get_anim_ID("WalkB")
DASH_F = get_anim_ID("ForwardDash")
WAIT = get_anim_ID("Idle")
DASH_B = get_anim_ID("BackDash")
JUMP = get_anim_ID("JumpSquat")
GRAB = get_anim_ID("ThrowWhiff")

#Move Categories
GROUND_MOVE = [get_anim_ID("Attack"), get_anim_ID("AttackLw"), get_anim_ID("Heavy"), get_anim_ID("HeavyLw"), 
               get_anim_ID("SpecialN"), get_anim_ID("SpecialLw"), get_anim_ID("SpecialS"), get_anim_ID("ThrowWhiff"), 
               get_anim_ID("WalkF"), get_anim_ID("WalkB"), get_anim_ID("ForwardDash"), get_anim_ID("BackDash"), get_anim_ID("JumpSquat"), get_anim_ID("Idle")
            ]
AIR_MOVE = [get_anim_ID("AttackAir"), get_anim_ID("HeavyAir"), get_anim_ID("SpecialS")]

#Parameters
BLOCK_CHANCE = 65

def add_to_queue(object, anim): #Adds an action to the queue
    object.cpuQueue.append(anim)

def rng_queue(object, choices): #Adds a random action to the queue based on a list of choices
    object.cpuQueue.append(random.choice(choices))

def check_movement(object,yourX,theirX, yourY, theirY):
    if object.isJump:
        add_to_queue(object, WAIT)
        return
    distance = int(abs(yourX-theirX)/10) + 10
    distanceY = int(abs(yourY-theirY)/10)
    if distance < JAB_RANGE: #Up Close
        if random.randint(0, 100) < 80:
            if distanceY < 3: #If theyre on the same level or ever so slightly above
                rng_queue(object, [DASH_B, JAB[object.char_id], JAB[object.char_id], GRAB])
            elif distanceY < 25: #If theyre above but not too high to antiair
                rng_queue(object, [DASH_B, ANTIAIR[object.char_id], ANTIAIR[object.char_id], DP[object.char_id]])
            else:
                add_to_queue(object, WAIT)
        else:
            if random.randint(0, 100) < 80:
                for _ in range(0,random.randint(1, 10)):
                    add_to_queue(object, WALK_B)
            else:
                for _ in range(0,random.randint(1, 10)):
                    add_to_queue(object, WALK_F)
    elif distance < POKE_RANGE: #Midrange spacing, prime footsies area
        if random.randint(0, 100) < 68:
            if distance > THEIR_POKE_RANGE[object.char_id]:
                rng_queue(object, [DASH_B,DASH_B, DASH_F, POKE[object.char_id],DASH_B,DASH_B, DASH_F, POKE2[object.char_id],DASH_B,DASH_B, DASH_F, POKE[object.char_id],BIG[object.char_id]])
            else:
                rng_queue(object, [DASH_B,DASH_B, DASH_F, POKE[object.char_id], POKE2[object.char_id], POKE[object.char_id],DASH_B,DASH_B, DASH_F, POKE[object.char_id], POKE2[object.char_id], 
                                   POKE[object.char_id], DASH_B,DASH_B, DASH_F, POKE[object.char_id], POKE2[object.char_id], POKE[object.char_id], BIG[object.char_id]])
        else:
            if random.randint(0, 100) < 65:
                for _ in range(0,random.randint(1, 15)):
                    add_to_queue(object, WALK_B)
            else:
                for _ in range(0,random.randint(1, 15)):
                    add_to_queue(object, WALK_F)
    elif distance < PROJECTILE_RANGE: #Within projectile spacing, far range
        if random.randint(0, 100) < 68:
            rng_queue(object, [DASH_F, DASH_F,DASH_F, DASH_F, POKE[object.char_id], POKE2[object.char_id], PROJECTILE[object.char_id], PROJECTILE[object.char_id], TATSU[object.char_id], BIG[object.char_id]])
        else:
            if random.randint(0, 100) < 50:
                for _ in range(0,random.randint(1, 15)):
                    add_to_queue(object, WALK_B)
            else:
                for _ in range(0,random.randint(1, 15)):
                    add_to_queue(object, WALK_F)
    elif distance >= PROJECTILE_RANGE: #Very far range, no normals are really hitting over here
        if random.randint(0, 100) < 68:
            if distance > THEIR_PROJECTILE_RANGE[object.char_id]:
                rng_queue(object, [DASH_F, DASH_F,DASH_F, DASH_F, DASH_F, DASH_F,DASH_F, DASH_F, DASH_F,DASH_F, DASH_F,
                            PROJECTILE[object.char_id], TATSU[object.char_id], TATSU[object.char_id]
                ])
            else:
                rng_queue(object, [DASH_F, DASH_F,DASH_F, DASH_F, DASH_F, DASH_F,DASH_F, DASH_F, DASH_F,DASH_F, DASH_F,
                            PROJECTILE[object.char_id], PROJECTILE[object.char_id], PROJECTILE[object.char_id], TATSU[object.char_id]
                ])
        else:
            if random.randint(0, 100) < 50:
                for _ in range(0,random.randint(1, 15)):
                    add_to_queue(object, WALK_B)
            else:
                for _ in range(0,random.randint(1, 15)):
                    add_to_queue(object, WALK_F)


