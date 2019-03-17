import threading
import time
sharedVar=65

sem = threading.Semaphore()

def inc():
    sem.acquire()
    global sharedVar
    reg=sharedVar
    time.sleep(0.2)
    reg+=1
    sharedVar=reg
    sem.release()

def dec():
    sem.acquire()
    global sharedVar
    reg=sharedVar
    time.sleep(0.2)
    reg-=1
    sharedVar=reg
    sem.release()

incThread = threading.Thread(None, inc, None)
decThread = threading.Thread(None, dec, None)

incThread.start()
decThread.start()

incThread.join()
decThread.join()

print(sharedVar)