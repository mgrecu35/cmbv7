from multiprocessing import Process
import os
import time
def info(title):
    print(title)
    print('module name:', __name__)
    print('parent process:', os.getppid())
    print('process id:', os.getpid())
    
def f(name):
    #info('function f')
    print('hello', name)
    time.sleep(10)
nL=['bob','bob2','bob3','bob4']
if __name__ == '__main__':
    jobs=[]
    t1=time.time()
    for n in nL:
        p = Process(target=f, args=(n,))
        jobs.append(p)
        p.start()
    for j in jobs:
        j.join()
    print('all done')
    print(time.time()-t1)
