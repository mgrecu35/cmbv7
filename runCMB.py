import os,glob

fs=glob.glob("../SO/DPR/dpr.SO*")
fs=sorted(fs)
os.environ["DYLD_LIBRARY_PATH"]="/Users/mgrecu/miniconda3/lib"
#print os.getenv("DYLD_LIBRARY_PATH")
foutF=open("runCMB.sh","w")
for f in fs:
    fout=f.replace("dpr","cmb")
    cmd='./combAlg.exe %s %s \n'%(f,fout)
    print(cmd)
    #os.system(cmd)
    foutF.write(cmd)
foutF.close()
