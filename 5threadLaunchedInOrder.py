import threading
import time
import os


ev=threading.Event()
ev.clear()
evCodeEnd=threading.Event()


def code():
    global sharedVar
    print('code launch')
    evCodeEnd.set()
    
    
def notepad():
    evCodeEnd.wait()
    print('notepad launch')
    ev.set()
    

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