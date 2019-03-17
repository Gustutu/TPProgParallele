# Distributed Programming TP 1

## Concurrent Access To Shared Memory : Race Problems

### Question 1

```python
import threading
import time

# initialize our shared variable with a value
sharedVar = 65

# increment thread function
def inc():
    global sharedVar
    reg = sharedVar
    reg += 1
    sharedVar = reg

# decrement thread function
def dec():
    global sharedVar
    reg = sharedVar
    reg -= 1
    sharedVar = reg

incThread = threading.Thread(None, inc, None)
decThread = threading.Thread(None, dec, None)

# start both threads
incThread.start()
decThread.start()

# wait for both threads to finish
incThread.join()
decThread.join()

# output the result of the shared variable
print(sharedVar)
```

### Question 2

```python
import threading
import time

# initialize our shared variable with a value
sharedVar = 65

# increment thread function
def inc():
    global sharedVar
    reg = sharedVar
    time.sleep(0.2)
    reg += 1
    sharedVar = reg

# decrement thread function
def dec():
    global sharedVar
    reg = sharedVar
    time.sleep(0.2)
    reg -= 1
    sharedVar = reg

incThread = threading.Thread(None, inc, None)
decThread = threading.Thread(None, dec, None)

# start both threads
incThread.start()
decThread.start()

# wait for both threads to finish
incThread.join()
decThread.join()

# output the result of the shared variable
print(sharedVar)
```

In this snippet, we are using the sleep function.  
When a thread is taking a long time (like in this example with the sleep function), the OS process scheduler switches to another process.  
The issue is that if we switch to another process (thread in this case), the last thread to finish will override the previous value of `sharedVar` because we are not updating its value after the sleep function has finished.  
We are modifying a local `reg` variable that corresponds to the initial value of `sharedVar`, that will always have the value 65.  
Thus, the last thread to finish will update the global variable `sharedVar` with either 66 or 64.

## Solving the Problem : Synchronizing access using semaphores

### Question 1

```python
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
    reg -= 1
    sharedVar=reg
    sem.release()

incThread = threading.Thread(None, inc, None)
decThread = threading.Thread(None, dec, None)
dec2Thread = threading.Thread(None, dec, None)

incThread.start()
decThread.start()
dec2Thread.start()

incThread.join()
decThread.join()

print(sharedVar)

```

### Question 2
```python
import threading
import time
import os



sharedVar=65
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

explorerThread.start()
notepadThread.start()
codeThread.start()

codeThread.join()
notepadThread.join()
explorerThread.join()

print("end")

```



### Question 3

```py
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
    #if the result array size is equal 2 the wait for T4 to end
    if(len(results))==2:
        evT4.wait()
    
    sem.acquire()
    results.append(3+4)
    print("T1 done")
    sem.release()
    #if the lenght of result array is superior or equal to 2 then wake up T4 thread
    if(len(results)>=2):
        print()
        ev.set()
  
    
def cd():
    
    global results
    if(len(results))==2:
        evT4.wait()
    
    sem.acquire()
    results.append(6-3)
    print("T2 done")
    sem.release()
    if(len(results)>=2):
       ev.set()
    
    
def ef():
    global results
    if(len(results))==2:
        evT4.wait()
    
    sem.acquire()
    results.append(1+1)
    print("T3 done")
    sem.release()
    if(len(results)>=2):
       ev.set()
    
def T4():
    #wait for event from thread to continue:
    ev.wait()
    ev.clear()
    global results
    sem.acquire()
    r=results[0]*results[1]
    print("intermediate result"+str(r))
    #unlock last thread:
    evT4.set()
    sem.release()

    #wait for last thread
    ev.wait()
    sem.acquire()
    r=r*results[2]
    sem.release()
    print(r)

abThread = threading.Thread(None, ab, None)
T4Thread=threading.Thread(None, T4, None)
cdThread = threading.Thread(None, cd, None)
efThread=threading.Thread(None, ef, None)

cdThread.start()
efThread.start()
T4Thread.start()
abThread.start()

abThread.join()
cdThread.join()
efThread.join()
T4Thread.join()

print("end")

```