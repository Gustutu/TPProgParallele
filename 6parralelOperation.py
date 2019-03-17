import threading
import time
import os



results=[]
sem = threading.Semaphore(4)
cv= threading.Condition()
ev=threading.Event()
evT4=threading.Event()


def ab():
   
    global results
    if(len(results))==2:
        evT4.wait()
    
    sem.acquire()
    results.append(3+4)
    print("T1 done")
    sem.release()
    ev.set()
  
    
def cd():
    
    global results
    if(len(results))==2:
        evT4.wait()
    
    sem.acquire()
    results.append(6-3)
    print("T2 done")
    sem.release()
    ev.set()
    
    
def ef():
    global results
    if(len(results))==2:
        evT4.wait()
    
    sem.acquire()
    results.append(1+1)
    print("T3 done")
    sem.release()
    ev.set()
    
def T4():
    ev.wait()
    ev.clear()
    global results
    sem.acquire()
    r=results[0]*results[1]
    print("intermediate result"+str(r))
    evT4.set()
    sem.release()
    ev.wait()
    sem.acquire()
    r=r*results[2]
    sem.release()
    print(r)

abThread = threading.Thread(None, ab, None)
cdThread = threading.Thread(None, cd, None)
efThread=threading.Thread(None, ef, None)
T4Thread=threading.Thread(None, T4, None)

cdThread.start()
efThread.start()
abThread.start()


T4Thread.start()


abThread.join()
cdThread.join()
efThread.join()
T4Thread.join()

print("end")