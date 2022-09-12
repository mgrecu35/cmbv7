import cAlg
ifirst=1
if ifirst==1:
    cAlg.mainfortpy()
    ifirst=0
import matplotlib.pyplot as plt

from readData import readData
import glob
f3=sorted(glob.glob("Data/1C*"))
f1=sorted(glob.glob("Data/2A*"))
f2=sorted(glob.glob("Data/2B*"))
n1,n2=0,800
import numpy as np
xs=np.random.randn(50)
nstda=0.1

sfcRateL=[]
pRate99=np.zeros((88),float)-99
pRateL=[]


for f1_,f2_,f3_ in zip(f1,f2,f3):
    input_=readData(f1_,f2_,f3_,n1,n2)
    qv,press,sfcType,pType,airTemp,envNodes,binNodes,\
        bcf,bsf1,pwc,sfcEmiss,dm,skTemp,lon,lat,tc_regrid,tc_regrid2,zKu,cldw,bbPeak,h0,pRateCMB,h0=input_
    h0=h0.data
    n2=qv.shape[0]
    for i in range(n1,n2):
        a=np.nonzero(pType[i,12:37]>0)
        for j in a[0]:
            z13obs=zKu[i,j,::2,0]
            z35obs=zKu[i,j,::2,0]
            node=binNodes[i,j,:]
            isurf=int(bsf1[i,j]/2)
            nodep=node
            log10dnp=np.zeros((5),float)
            ic,jc=1,1
            dr=0.25
            hh=(np.arange(88)*0.25)[::-1]
            itype=pType[i,j]
            hfreez=h0[i,j]/1000.
            pia13srt=-99.9
            relpia13srt=-1
            pia35srt=-99.9
            relpia35srt=-1
            imemb=1
            nmfreq=8
            imu=np.zeros((88),int)+3
            ##node[4]=int(bcf[i,j]/2)
            node+=1
            log10dn=np.zeros((88),float)+0.5
            pia35m,pia13m,z35mod,pwc,salb,kext,asym,\
            rrate,dm,log10dn,z13,z35 = cAlg.fmodel_fortran(z13obs,z35obs,node,isurf,imu,log10dnp,\
            nodep,dr,ic,jc,hh,nmfreq,itype,\
            hfreez,pia13srt,relpia13srt,pia35srt,relpia35srt,imemb,xs,nstda,log10dn)
            #print(isurf)
            pRateL.append(rrate)
            if(hfreez<=0):
                #print(rrate[node[4]-1],pRateCMB[i,j,node[4]-1])
                if rrate[node[4]-1]>=0:
                   #print(len(sfcRateL),node)
                   sfcRateL.append([rrate[node[4]-1],pRateCMB[i,j,node[4]-1]])
        else:
            pRateL.append(pRate99)


sfcRateL=np.array(sfcRateL)
#pRateL=np.array(pRateL)
#pRatem=np.ma.array(pRateL,mask=pRateL<0)
import matplotlib
#plt.pcolormesh(zKu[:,24,::-1,0].T,cmap='jet',vmin=0,vmax=40)
#plt.xlim(350,600)
#plt.ylim(0,80)
#plt.figure()
#plt.pcolormesh(pRatem[:,::-1].T,norm=matplotlib.colors.LogNorm(vmin=0.1,vmax=20),cmap='jet')
#plt.ylim(0,40)