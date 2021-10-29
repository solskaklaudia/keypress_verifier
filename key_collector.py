from pynput.keyboard import Key, Listener
import time

keys = []

def on_press(key):
    elapsed_time = time.perf_counter()
    print('{0} pressed at {1}'.format(
        key, elapsed_time))

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
    print('{0} released at {1}'.format(
        key, elapsed_time))

    key = {
        "key": key,
        "status": "released",
        "time": elapsed_time
    }

    keys.append(key)

    if key["key"] == Key.esc:
        # Stop listener
        return False


# Collect events until released
with Listener(
        on_press = on_press,
        on_release = on_release) as listener:
    listener.join()