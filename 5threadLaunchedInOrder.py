import threading
import time
import os



sharedVar=65
#notepad
#explorer
#code (vscode)
sem = threading.Semaphore(3)
cv= threading.Condition()
ev=threading.Event()
ev.clear()

def code():
   
    cv.acquire()
    global sharedVar
    print('code launch')
    cv.notify_all()
    cv.release()
    
    
def notepad():
    cv.acquire()
    cv.wait()
    cv.acquire()
    ev.set()
    print('notepad launch')
    cv.release()

def explorer():
    ev.wait()
    print('explorer launch')
    

codeThread = threading.Thread(None, code, None)
notepadThread = threading.Thread(None, notepad, None)
explorerThread=threading.Thread(None, explorer, None)
#setTo2Thread=threading.Thread(None,setTo2,None)



#setTo2Thread.start()
explorerThread.start()
notepadThread.start()
codeThread.start()



codeThread.join()
notepadThread.join()
explorerThread.join()

print("end")