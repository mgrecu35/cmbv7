import cAlg
ifirst=1
if ifirst==1:
    cAlg.mainfortpy()
    cAlg.initp2()
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
nstda=0.05

sfcSnowRateL=[]
sfcRainRateL=[]
pRate99=np.zeros((88),float)-99
pRateL=[]

#cAlg.init_keras()
cAlg.init_keras2()
#stop
dmL=[]
irainp=0
snowProfL=[]
for f1_,f2_,f3_ in zip(f1[:],f2[:],f3[:]):
    input_=readData(f1_,f2_,f3_,n1,n2)
    qv,press,sfcType,pType,airTemp,envNodes,binNodes,\
        bcf,bsf1,pwc,sfcEmiss,dm,skTemp,lon,lat,tc_regrid,tc_regrid2,zKu,cldw,bbPeak,h0,pRateCMB,h0=input_
    h0=h0.data
    n2=qv.shape[0]
    pRate3D=np.zeros((n2,49,88),float)
    zsfcL=[]
#    from chaseRet import retr
    iwcL=[]
    for i in range(n1,n2):
        a=np.nonzero(pType[i,12:37]>0)
        for j in a[0]:
            z13obs=zKu[i,j,::2,0]
            z35obs=zKu[i,j,::2,1]
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
            
            log10dn=np.zeros((88),float)+0.0
            n1p,n2p=node[0:2]
            n2p+=1
            if n2p>node[4]+1:
                n2p=node[4]+1
            node+=1
            a1=np.nonzero(z13obs[n1p:n2p]>10)
            if n2p>n1p:
                iwc_nn=np.zeros((n2p-n1p),float)
            if len(a1[0])>0:
                temp=z13obs[n1p:n2p][a1].data*0-10
                x_in=np.array([z13obs[n1p:n2p][a1].data,z35obs[n1p:n2p][a1].data,temp]).T
                y_out=cAlg.call_keras2(x_in)
                Nw,IWC,Dm=y_out[:,0],y_out[:,1],y_out[:,2]
                
                Nw2=cAlg.get_nw(z13obs[n1p:n2p][a1].data,z35obs[n1p:n2p][a1].data,1e3*Dm)
                log10dn[n1p:n2p][a1]=Nw2*0.975+0.025*np.log10(Nw/0.08e8)+0.5*np.random.randn()
                #dmL.append([dm_ensf[-1],Dm[-1]])
                iwc_nn[a1]=IWC
                if n2p<node[3] and node[3]<88:
                    #print(n2p,node[2],node[3],node[4])
                    
                    log10dn[n2p:node[3]]=np.interp(np.arange(n2p,node[3]),[n2p,node[3]],\
                        [log10dn[n2p-1],log10dn[node[3]]])
                    #if node[2]<node[4] and n2p<node[2]-1:
                        #stop
                #print(nw_ensf)
            #if hfreez>0 or n2p-n1p<10:
            #    continue
            pia35m,pia13m,z35mod,pwc,salb,kext,asym,\
            rrate,dm,log10dn,z13,z35 = cAlg.fmodel_fortran(z13obs,z35obs,node,isurf,imu,log10dnp,\
            nodep,dr,ic,jc,hh,nmfreq,itype,\
            hfreez,pia13srt,relpia13srt,pia35srt,relpia35srt,imemb,xs,nstda,log10dn)
            pia35m,pia13m,z35mod,pwc,salb,kext,
           
            #print(isurf)
            pRateL.append(rrate)
            pRate3D[i,j+12,:]=rrate
            if(hfreez<=0):
                #print(rrate[node[4]-1],pRateCMB[i,j,node[4]-1])
                
                if rrate[node[4]-1]>0 and len(a1[0])>=0:
                   #print(len(sfcRateL),node)
                   sfcSnowRateL.append([rrate[node[4]-1],pRateCMB[i,j,node[4]-1]])
                   for k in range(n1p,n2p):
                       if z35obs[k]>12 and z13obs[k]>12:
                        zsfcL.append([z35obs[k],z35mod[k]])
                        iwcL.append([iwc_nn[k-n1p],pwc[k]])    
                   #print(nw_ensf,node,n1p,n2p,rrate[node[4]-1])
                   #print(n1p,n2p)
                   #stop
            if(hfreez>0 and node[4]>=node[3]):
                if rrate[node[4]-1]>0:
                    sfcRainRateL.append([rrate[node[4]-1],pRateCMB[i,j,node[4]-1]])
                    snowProfL.append(rrate[node[3]-30:node[3]])
        else:
            pRateL.append(pRate99)
    break

sfcRainRateL=np.array(sfcRainRateL)
sfcSnowRateL=np.array(sfcSnowRateL)
pRateL=np.array(pRateL)
zsfcL=np.array(zsfcL)
dmL=np.array(dmL)
pRatem=np.ma.array(pRate3D[:,24,:],mask=pRate3D[:,24,:]<0)
import matplotlib
plt.pcolormesh(zKu[:,24,::-1,0].T,cmap='jet',vmin=0,vmax=40)
plt.xlim(300,500)
plt.ylim(0,80)
plt.figure()
plt.pcolormesh(pRatem[:,::-1].T,norm=matplotlib.colors.LogNorm(vmin=0.1,vmax=20),cmap='jet')
plt.xlim(300,500)
plt.ylim(0,40)