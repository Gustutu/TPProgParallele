import threading
import time
sharedVar=65

def inc():
    global sharedVar
    reg=sharedVar
    reg+=1
    sharedVar=reg



def dec():
    global sharedVar
    reg=sharedVar
    reg-=1
    sharedVar=reg

incThread = threading.Thread(None, inc, None)
decThread = threading.Thread(None, dec, None)

incThread.start()
decThread.start()

incThread.join()
decThread.join()

print(sharedVar)