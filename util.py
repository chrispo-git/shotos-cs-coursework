#Contains constants and functioned used between many py files
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
    "Heavy",
    "HeavyLw",
    "HeavyAir",
    "Hitstun",
    "Guard",
    "CrouchGuard",
    "GuardAir",
    "SpecialLw",
    "SpecialN",
    "SpecialNEmpty",
    "SpecialS",
    "ThrowWhiff",
    "ThrowF"
]


def get_anim_ID(name: str) -> int:
        global ANIMATION_LIST_LABEL
        try:
            value = ANIMATION_LIST_LABEL.index(name)
            return value
        except ValueError:
            return -1

def get_controls_from_txt() -> list:
    f = open("controls.txt")
    controls = f.readlines()
    for x in range(0, len(controls)):
        i = controls[x]
        i = i.replace("\n", "")
        i = i.split(" ")
        while len(i) < 7:
            i.append("_")
        controls[x] = i
    
    return controls