from multiprocessing import Process
import os
import time
# git remote set-url origin https://mgrecu35@github.com/mgrecu35/cmbv7.git

def info(title):
    print(title)
    print('module name:', __name__)
    print('parent process:', os.getppid())
    print('process id:', os.getpid())
    
def fsh(fname):
    cmb1=fname.split('.')[-4:]
    cmb1out="out/cmb."+cmb1[0]+"."+cmb1[1]+"."+cmb1[3]
    cmd='bpsh 245 ./combAlg.exe %s %s>&out/out.%s'%(fname,cmb1out,cmb1[1])
    print(cmd)
    os.system(cmd)
    time.sleep(1)
import glob

if __name__ == '__main__':
    #
    for iday in range(1,2):
        iday=1
        fs=glob.glob("/gpmdata/2018/08/%2.2i/radar/2A.GPM.DPR.V8*"%iday)
        fs=sorted(fs)
        jobs=[]
        t1=time.time()
        if iday==1:
            t11=t1
        for f in fs:
            p = Process(target=fsh, args=(f,))
            jobs.append(p)
            p.start()
        for j in jobs:
            j.join()
        print('all done')
        print(time.time()-t1)
    print(time.time()-t11)
