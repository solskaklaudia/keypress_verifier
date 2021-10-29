from pynput.keyboard import Key, Listener
import time

def on_press(key):
    elapsed_time = time.perf_counter()
    print('{0} pressed at {1}'.format(
        key, elapsed_time))

def on_release(key):
    elapsed_time = time.perf_counter()
    print('{0} released at {1}'.format(
        key, elapsed_time))
    if key == Key.esc:
        # Stop listener
        return False

# Collect events until released
with Listener(
        on_press = on_press,
        on_release = on_release) as listener:
    listener.join()