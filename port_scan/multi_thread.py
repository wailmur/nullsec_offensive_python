import threading
import time

def delayed_message():
    print("Hello, wait 5 seconds (in the background).")
    time.sleep(5.1)
    print("Thanks for waiting!")

thread = threading.Thread(target=delayed_message) # create a thread
thread.start() # start thread
# this part still runs despite waiting
for i in range(1, 6):
    time.sleep(1)
    print(f"Second(s): {i}")