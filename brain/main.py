import random

def do_sign(sign_name):
    """
    The robot perform the sign (if found) matching the passed string
    """
    print(f"doing sign {sign_name}")

def detect_sign(sign_names, detect_period=5):
    """
    The robot will detect for the signs (if found) matching the passed string for the period of time or forever if None
    returns one of the passed signs if detected, or "null" if nothings found at the end of detect_period
    """

    print(f"doing sign {sign_names}")
    return sign_names[0]


new_signs = []

def idle():
    reset()
    _ = detect_sign(["start"], detect_period=None)
    learn_sign()

def learn_sign():
    sign = new_signs[0]
    do_sign(sign)
    detected_sign = detect_sign([sign, "exit", "repeat"])

    if detected_sign == sign: #if sign done correctly
        learnt_signs.append(new_signs.pop(0))
        if len(new_signs) == 0: #if user has completed all signs
            do_sign("you win")
            idle()
        else: #o/w move onto next sign
            do_sign("correct")
            learn_sign()
    elif detected_sign == "null": #sign done incorrectly
        do_sign("no")
        learn_sign()
    elif detected_sign == "repeat": 
        learn_sign()
    elif detected_sign == "exit":
        idle()

def reset():
    new_signs = random.shuffle(["how_are_you", "robot", "bristol", "teacher", "sign", "software"])


if __name__ == "__main__":
    random.seed()
    idle()
    
