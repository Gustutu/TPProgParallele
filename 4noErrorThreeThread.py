import threading
import time
import os


sharedVar=65
#notepad
#explorer
#code (vscode)
sem = threading.Semaphore(3)
cv= threading.Condition()

def code():
    sem.acquire()
    global sharedVar
    os.system('code')
    sem.release()

def notepad():
    cv.wait()
    global sharedVar
    os.system('notepad')
    sem.release()


def explorer():
    cv.wait
    sem.acquire()
    os.system('explorer')
    sem.release()

codeThread = threading.Thread(None, code, None)
notepadThread = threading.Thread(None, notepad, None)
explorerThread=threading.Thread(None, explorer, None)
#setTo2Thread=threading.Thread(None,setTo2,None)



#setTo2Thread.start()
codeThread.start()
notepadThread.start()
explorerThread.start()


codeThread.join()
notepadThread.join()
explorerThread.join()

print("end")