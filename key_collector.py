from pynput.keyboard import Key, Listener
import time
import statistics as st

def calcParameters(keys):
    
    print(keys)
    hold_time = calcAvgHoldTime(keys)
    press_time = calcTimeBetwenKeyPress(keys)
    combinations_time = calcTimeBetweenCombinations(keys)
    print("average key hold time: " + str(hold_time[0]) + " +/- " + str(hold_time[1]) + " ms")
    print("average time between key presses: " + str(press_time[0]) + " +/- " + str(press_time[1]) + " ms")
    print("average time between key combinations: " + str(combinations_time[0]) + " +/- " + str(combinations_time[1]) + " ms")
    print("average typing speed: " + str(calcTypingSpeed(keys)) + " keys/min")
    print("average number of errors: " + str(countErrors(keys)) + " keys/min")


""" Sorting """

# sorting by key first (letter size invariant) and time second
def sortFunc1(e):
    key = str(e["key"]).lower()
    return key, e["time"]

# sorting by time
def sortFunc2(e):
    return e["time"]


""" Calculate typing parameters """

def calcAvgHoldTime(keys):
    """ Calculates average time of holding a key (difference between press and release of a key) """

    keys.sort(key=sortFunc1)

    samples = []

    avg_hold_time = 0
    temp = 0

    for k in range(len(keys)):
        if k%2 == 0:
            temp = keys[k]["time"]
        else: 
            sample = keys[k]["time"] - temp
            samples.append(sample)
            avg_hold_time += sample

    if(len(keys) > 0):
        avg_hold_time = avg_hold_time / (len(keys)/2)

    # standard deviation
    stdev = st.stdev(samples)

    return (avg_hold_time * 1000, stdev * 1000)


def calcTimeBetwenKeyPress(keys):
    """ Calculates average time between key presses """

    keys.sort(key=sortFunc2)

    samples = []

    avg_time_between_key_press = 0
    temp = 0
    key_counter = 0

    for k in range(len(keys)):
        if (keys[k]["status"] == "pressed"):
            
            if(k > 0):
                time = keys[k]["time"] - temp

                # save only times less than 3 seconds
                # to avoid counting pauses in typing
                if(time < 3.0):
                    avg_time_between_key_press += time
                    key_counter += 1
                    samples.append(time)

            temp = keys[k]["time"]

    if(key_counter > 0):
        avg_time_between_key_press = avg_time_between_key_press / key_counter

    # standard deviation
    stdev = st.stdev(samples)

    return (avg_time_between_key_press * 1000, stdev * 1000)


def calcTimeBetweenCombinations(keys):
    """ Calculates average time between pressing another key in key combination 
    eg. between pressing `Ctrl` and `C` """

    keys.sort(key=sortFunc2)

    samples = []

    counter = 0
    avg_time = 0

    for k in range(len(keys)):

        if(k < len(keys) - 1):
            if(keys[k]["status"] == "pressed" and keys[k+1]["status"] == "pressed"):
                sample = keys[k+1]["time"] - keys[k]["time"]
                samples.append(sample)
                avg_time += sample
                counter += 1
        
    if(counter > 0):
        avg_time = avg_time / counter

    # standard deviation
    stdev = st.stdev(samples)

    return (avg_time * 1000, stdev * 1000)


def calcTypingSpeed(keys):
    """ Calculates average numbers of keys pressed per minute
    excluding pauses longer than 3 seconds"""

    keys.sort(key=sortFunc2)

    avg_typing_speed = 0
    time_sum = 0
    temp = 0
    key_counter = 0

    for k in range(len(keys)):
            
        if(keys[k]["status"] == "pressed"):
            if(k > 0):
                time = keys[k]["time"] - temp

                # save only times less than 3 seconds
                # to avoid counting pauses in typing
                if(time < 3.0):
                    time_sum += time      

            temp = keys[k]["time"]
            key_counter += 1

    if(time_sum > 0):
        avg_typing_speed = key_counter / time_sum * 60

    return avg_typing_speed


def countErrors(keys):
    """ Counts errors (number of `backspace` or `delete` keys pressed) per minute """

    keys.sort(key=sortFunc2)

    time_sum = 0
    temp = 0
    errors = 0

    for k in range(len(keys)):
            
        if(k > 0):
            time = keys[k]["time"] - temp

            # save only times less than 3 seconds
            # to avoid counting pauses in typing
            if(time < 3.0):
                time_sum += time

        temp = keys[k]["time"]

        if(keys[k]["status"] == "pressed" and (keys[k]["key"] == Key.backspace or keys[k]["key"] == Key.delete)):
            errors += 1

    if(time_sum > 0):
        avg_errors = errors / time_sum * 60

    return avg_errors


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