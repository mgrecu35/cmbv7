from netCDF4 import Dataset
from numpy import *
import numpy as np

def readRet(f1,f2):
    fh1=Dataset(f1)
    fh2=Dataset(f2)
    r1=fh1['NS/surfPrecipTotRate'][:,:]
    r2=fh2['NS/surfPrecipTotRate'][:-1,:]
    pType=(fh2['NS/Input/precipitationType'][:-1,:]/1e7).astype(int)
    a=nonzero(pType==1)
    x=fh1['NS/Longitude'][:,:]
    y=fh1['NS/Latitude'][:,:]
    return r1,r2,pType,x,y

def cmpRet(f1,f2):
    fh1=Dataset(f1)
    fh2=Dataset(f2)
    r1=fh1['NS/surfPrecipTotRate'][:,:]
    r2=fh2['NS/surfPrecipTotRate'][:-1,:]
    pType=(fh2['NS/Input/precipitationType'][:-1,:]/1e7).astype(int)
    a=nonzero(pType==1)
    print(r1.shape,r2.shape,pType.shape)
    rst=[r1[a].sum(),r2[a].sum()]
    c1=corrcoef(r1[a],r2[a])[0,1]
    a=nonzero(pType==2)
    b=nonzero(r2[a]==r2[a])
    rcv=[r1[a][b].sum(),r2[a][b].sum()]
    c2=corrcoef(r1[a],r2[a])[0,1]
    print('st=',c1,'cv=',c2)
    if len(a[0])!=len(b[0]):
        print(f1,f2)
        print(len(a[0]),len(b[0]))
        c=nonzero(r2[a]!=r2[a])
        print(a[0][c])
        stop
    return np.array(rst),np.array(rcv)



import matplotlib.pyplot as plt


import pickle
rstrat,rconv,counts=pickle.load(open('aug2018.pklz','rb'))
