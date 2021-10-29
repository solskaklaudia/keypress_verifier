from pynput.keyboard import Key, Listener
import time

def calcParameters(keys):
    
    print(keys)
    print("average key hold time: " + str(calcAvgHoldTime(keys)) + " s")
    print("average time between key presses: " + str(calcTimeBetwenKeyPress(keys)) + " s")
    print("average typing speed: " + str(calcTypingSpeed(keys)) + " 1/min")
    print("average number of errors: " + str(countErrors(keys)) + " 1/min")
    print("average time between key combinations: " + str(calcTimeBetweenCombinations(keys)) + " s")


""" Sorting """

def sortFunc1(e):
    key = str(e["key"]).lower()
    return key, e["time"]


def sortFunc2(e):
    return e["time"]


""" Calculate typing parameters """

def calcAvgHoldTime(keys):

    keys.sort(key=sortFunc1)

    avg_hold_time = 0   # in seconds
    temp = 0

    for k in range(len(keys)):
        if k%2 == 0:
            temp = keys[k]["time"]
        else: 
            avg_hold_time += keys[k]["time"] - temp

    if(len(keys) > 0):
        avg_hold_time = avg_hold_time / len(keys) / 2

    return avg_hold_time


def calcTimeBetwenKeyPress(keys):

    keys.sort(key=sortFunc2)

    avg_time_between_key_press = 0 # in seconds
    temp = 0
    key_counter = 0

    for k in range(len(keys)):
        if (keys[k]["status"] == "pressed"):
            
            if(k > 0):
                time = keys[k]["time"] - temp

                # save only times less than 1 seconds
                # to avoid counting pauses in typing
                if(time < 1.0):
                    avg_time_between_key_press += time
                    key_counter += 1

            temp = keys[k]["time"]

    if(key_counter > 0):
        avg_time_between_key_press = avg_time_between_key_press / key_counter

    return avg_time_between_key_press
        

def calcTypingSpeed(keys):

    keys.sort(key=sortFunc2)

    avg_typing_speed = 0    # number of keys per minute
    time_sum = 0            # in seconds
    temp = 0

    for k in range(len(keys)):
            
        if(k > 0):
            time = keys[k]["time"] - temp

            # save only times less than 1 seconds
            # to avoid counting pauses in typing
            if(time < 1.0):
                time_sum += time

        temp = keys[k]["time"]

    if(time_sum > 0):
        avg_typing_speed = len(keys) / time_sum * 60

    return avg_typing_speed


def countErrors(keys):

    keys.sort(key=sortFunc2)

    time_sum = 0 # in seconds
    temp = 0
    errors = 0

    for k in range(len(keys)):
            
        if(k > 0):
            time = keys[k]["time"] - temp

            # save only times less than 1 seconds
            # to avoid counting pauses in typing
            if(time < 1.0):
                time_sum += time

        temp = keys[k]["time"]

        if(keys[k]["status"] == "pressed" and (keys[k]["key"] == Key.backspace or keys[k]["key"] == Key.delete)):
            errors += 1

    if(time_sum > 0):
        avg_errors = errors / time_sum * 60

    return avg_errors


def calcTimeBetweenCombinations(keys):

    counter = 0
    avg_time = 0

    for k in range(len(keys)):

        if(k < len(keys) - 1):
            if(keys[k]["status"] == "pressed" and keys[k+1]["status"] == "pressed"):
                avg_time += keys[k+1]["time"] - keys[k]["time"]
                counter += 1
        
    if(counter > 0):
        avg_time = avg_time / counter

    return counter


""" Detecting keys """

keys = []

def on_press(key):
    elapsed_time = time.perf_counter()
    print('{0} pressed at {1}'.format(key, elapsed_time))

    key = {
            "key": key,
            "status": "pressed",
            "time": elapsed_time
        }

    if(len(keys) > 0):
        # Add key press entry to list if it's not already added,
        # prevents adding multiple entries of the same key when holding
        if(not(keys[-1]["key"] == key["key"] and keys[-1]["status"] == "pressed")):
            keys.append(key)

    else:
        keys.append(key)


def on_release(key):
    elapsed_time = time.perf_counter()
    print('{0} released at {1}'.format(key, elapsed_time))

    key = {
        "key": key,
        "status": "released",
        "time": elapsed_time
    }

    keys.append(key)

    if key["key"] == Key.esc:

        calcParameters(keys)

        # Stop listener
        return False


# Collect events until released
with Listener(
        on_press = on_press,
        on_release = on_release) as listener:
    listener.join()