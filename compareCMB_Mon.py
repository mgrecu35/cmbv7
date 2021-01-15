f1='/gpmdata/2018/08/01/radar/2A.GPM.DPR.V8-20180723.20180801-S105937-E123210.025137.V06A.HDF5'
f2='out/test.h5'
f1='/gpmdata/2018/08/01/radar/2B.GPM.DPRGMI.CORRA2018.20180801-S105937-E123210.025137.V06A.HDF5'
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

import glob

rst_t=np.zeros((2,),float)
rcv_t=np.zeros((2,),float)

dx=2.5
ny=int(120/2.5)
nx=int(360/2.5)
from numba import jit
counts=np.zeros((nx,ny,3),float)
rconv=np.zeros((nx,ny,2),float)
rstrat=np.zeros((nx,ny,2),float)
@jit(nopython=True)
def grid(rcounts,rconv,rstrat,r1,r2,pType,x,y,dx,nx,ny):
    nscan,nr=r1.shape
    for i in range(nscan):
        for j in range(nr):
            i0=int((x[i,j]+180)/dx)
            j0=int((y[i,j]+65)/dx)
            if i0>=0 and i0<nx and j0>=0 and j0<ny:
                if pType[i,j]==1:
                    rcounts[i0,j0,0]+=1
                    rstrat[i0,j0,0]+=r1[i,j]
                    rstrat[i0,j0,1]+=r2[i,j]
                if pType[i,j]==2:
                    rcounts[i0,j0,1]+=1
                    rconv[i0,j0,0]+=r1[i,j]
                    rconv[i0,j0,1]+=r2[i,j]
                if pType[i,j]<1 or pType[i,j]>2:
                    rcounts[i0,j0,2]+=1
    return rcounts,rconv,rstrat

for iday in range(1,27):
    fs=glob.glob("/gpmdata/2018/08/%2.2i/radar/2B.GPM.DPRGMI.C*"%iday)
    fs=sorted(fs)
    for fname in fs:
        cmb1=fname.split('.')[-4:]
        cmb1out="out/cmb."+cmb1[0]+"."+cmb1[1]+"."+cmb1[3]
        rst,rcv=cmpRet(fname,cmb1out)
        r1,r2,pType,x,y=readRet(fname,cmb1out)
        rst_t+=rst
        rcv_t+=rcv
        counts,rconv,rstrat=grid(counts,rconv,rstrat,r1,r2,pType,x,y,dx,nx,ny)
    print(rst_t/rst_t.mean())
    print(rcv_t/rcv_t.mean())


import matplotlib.pyplot as plt
a=nonzero(counts[:,:,0]>0)
rstrat[:,:,0][a]=rstrat[:,:,0][a]/counts[:,:,0][a]
a=nonzero(counts[:,:,0]>0)
rstrat[:,:,1][a]=rstrat[:,:,1][a]/counts[:,:,0][a]
plt.figure()
plt.subplot(211)
rstrat=ma.array(rstrat,mask=rstrat<=0)
plt.pcolormesh(rstrat[:,:,0].T,cmap='jet',vmax=10)
plt.subplot(212)
plt.pcolormesh(rstrat[:,:,1].T,cmap='jet',vmax=10)

a=nonzero(counts[:,:,1]>0)
rconv[:,:,0][a]=rconv[:,:,0][a]/counts[:,:,1][a]
a=nonzero(counts[:,:,1]>0)
rconv[:,:,1][a]=rconv[:,:,1][a]/counts[:,:,1][a]
rconv=ma.array(rconv,mask=rstrat<=0)
plt.figure()
plt.subplot(211)
plt.pcolormesh(rconv[:,:,0].T,cmap='jet',vmax=20)
plt.subplot(212)
plt.pcolormesh(rconv[:,:,1].T,cmap='jet',vmax=20)

import pickle
pickle.dump([rstrat,rconv,counts],open('aug2018.pklz','wb'))
