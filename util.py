

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
