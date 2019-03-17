import threading
import time
sharedVar=65

def inc():
    global sharedVar
    reg=sharedVar
    time.sleep(0.2)
    reg+=1
    sharedVar=reg



def dec():
    global sharedVar
    reg=sharedVar
    time.sleep(0.2)
    reg-=1
    sharedVar=reg

incThread = threading.Thread(None, inc, None)
decThread = threading.Thread(None, dec, None)

incThread.start()
decThread.start()

incThread.join()
decThread.join()

print(sharedVar)