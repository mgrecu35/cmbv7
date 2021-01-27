fnameDPR='../DPRData/Atlantic/2A.GPM.DPR.V8-20180723.20180830-S183511-E200744.025593.V06A.HDF5'
fnameDPR='../monthly/SEAsia/2A.GPM.DPR.V8-20180723.20180602-S021248-E034522.024198.V06A.HDF5'
from netCDF4 import Dataset
import numpy as np
import pickle
labelst=pickle.load(open('labels_SO.pklz','rb'))

import glob
fs=glob.glob("DPR/dpr*HDF5")
fs=sorted(fs)
bzL=[[]for i in range(5)]
ind=[35,65,266,378,405,420,435]
ind2=[384, 134, 293, 303, 170,  72, 346, 322, 123, 341, 335, 397, 119,
      369, 186, 193, 191, 174, 110,  89, 393, 211, 374, 140, 196, 257,
      239,  95,  19, 175, 279,  65, 230, 396, 461, 180, 226, 237, 232,
      420,  17, 411, 435, 390, 104, 378,  35,  63, 266, 405]
def readSfcRainS(fname):
    fh=Dataset(fname,'r')
    sfcRain=fh['NS/SLV/precipRateNearSurface'][:,:]
    return sfcRain
#rainL=[]
#for f in fs:
#    rain=readSfcRainS(f)
#    rainL.append(rain.sum())
#rainL=np.array(rainL)
#inds=np.argsort(rainL)
import pickle
#pickle.dump(inds,open('sortedInd.pklz','wb'))
indx=pickle.load(open('sortedInd.pklz','rb'))
#stop
def readSfcRainCmb(fname):
    fh=Dataset(fname,'r')
    sfcRain=fh['NS/surfPrecipTotRate'][:,:]
    pRate=fh['NS/precipTotRate'][:,:,:]
    binNodes=fh['NS/phaseBinNodes'][:,:]
    fh.close()
    return sfcRain,pRate,binNodes

def readSfcRain(fname):
    fh=Dataset(fname,'r')
    sfcRain=fh['NS/SLV/precipRateNearSurface'][:,:]
    lat=fh['NS/Latitude'][:,:]
    lon=fh['NS/Longitude'][:,:]
    #print(fh['NS/PRE'])
    zm=fh['NS/PRE/zFactorMeasured'][:,:,:]
    zmka=fh['MS/PRE/zFactorMeasured'][:,:,:]
    #print(sfcRain)
    dayOfMonth=fh['NS/ScanTime/DayOfMonth'][:]
    hh=fh['NS/ScanTime/Hour'][:]
    sfcType=fh['NS/PRE/landSurfaceType'][:,:]
    h0=fh['NS/VER/heightZeroDeg'][:,:]
    bz=fh['NS/VER/binZeroDeg'][:,:]
    bcf=fh['NS/PRE/binClutterFreeBottom'][:,:]
    btop=fh['NS/PRE/binStormTop'][:,:]
    pType=(fh['NS/CSF/typePrecip'][:,:]/1e7).astype(int)
    binBB=fh['NS/CSF/binBBPeak'][:,:]
    binBBTop=fh['NS/CSF/binBBTop'][:,:]
    bsfc=fh['NS/PRE/binRealSurface'][:,:]
    pathAtten=fh['NS/SRT/pathAtten'][:,:]
    rFlag=fh['NS/SRT/reliabFlag'][:,:]
    return lat,lon,sfcRain,zm,zmka,fh,dayOfMonth,hh,sfcType,h0,bz,\
        bcf,btop,pType,binBB,binBBTop,bsfc,pathAtten,rFlag
countsT=[0,0,0,0,0]
countsR=[0,0,0,0,0]
sumR=[0,0,0,0,0]
ifs=0
orbCL=[]
rainL=[]

import matplotlib.pyplot as plt
import matplotlib
import libComp as cmb
cmb.mainfortpy()
cmb.initp2()

#for i in np.array(ind2[-20:])[[2,11,12,15,16,18]]:
pL=[[] for i in range(49)]
pLnoBB=[[] for j in range(49)]
def st_BB(pL,binBB,binBBTop,bcf,bsfc,btop,sfcType,pathAtten,relFlag,zm,zmka):
    for j in range(49):
        a=np.nonzero(binBB[:,j]>0)
        b=np.nonzero(sfcType[:,j]>0)
        for i in a[0]:
            bzd_=bzd[i,j]
            bbt=binBBTop[i,j]
            bb=binBB[i,j]
            bbb=bb+2
            bcf_=bcf[i,j]
            bsfc_=bsfc[i,j]
            zkul=zm[i,j,:]
            if abs(j-12)<13:
                zkal=zmka[i,j-12,:]
            else:
                zkal=zm[i,j,:]*0.-99
            dr=0.125
            eps=1.0
            imu=3
            dnCoeff=[-0.01257341, -0.00933038]
            dnst=-0.2
            dnp=np.zeros((176),float)
            btop_=btop[i,j]
            bcf_=bcf[i,j]
            dn1d,dm1d,rrate1d,zkuc,zkasim,epst,piaku,piaka,\
                dzdn,dpiadn,piakus,piakas = cmb.iter_profst(btop_,bzd_,bb,bbt,bbb,bcf_,bsfc_,zkul,zkal,\
                                                            dr,eps,imu,dnst,dnCoeff,dnp)
            if bcf_>bbb+1:
                nc=bsfc_-bcf_
                wzku=0.2
                wzka=0.1
                wpia=1
                nens=60
                dsrtPIA=pathAtten[i,j]*5
                reliabFlag=relFlag[i,j]
                rrate_out,dn_out,zkusimE,zkasimE,\
                    zku_out,zka_out,rrEns,yEns,xEns,dy,pia_out,\
                    dmOut= \
                        cmb.rainprofstg(zkul[bbb:bcf_+1],zkal[bbb:bcf_+1],\
                                        dsrtPIA,piakus,piakas,\
                                        reliabFlag,nc,dr,wzku,wzka,wpia,\
                                        rrate1d[bbb:bcf_+1],dn1d[bbb:bcf_+1],nens)
                rrate1d[bcf_]=rrate_out[-1]
                #print(piakus,piakas,rrate1d[bbb],rrate1d[bbt])
                pL[j].append([rrate1d[bbb],rrate1d[bbt],rrate1d[bcf_],sfcRain[i,j]])


def st_noBB(pL,pType,binBB,binBBTop,bcf,bsfc,btop,bzd,sfcType,pathAtten,relFlag,zm,zmka):
    for j in range(49):
        a=np.nonzero(binBB[:,j]<=0)
        b=np.nonzero(pType[:,j][a]==1)
        c=np.nonzero(sfcType[:,j][a][b]==0)
        d=np.nonzero(bzd[:,j][a][b][c]>0)
        for i in a[0][b][c][d]:
            bzd_=bzd[i,j]
            bbt=binBBTop[i,j]
            bbb=bzd_+2
            bcf_=bcf[i,j]
            bsfc_=bsfc[i,j]
            zkul=zm[i,j,:]
            if abs(j-12)<13:
                zkal=zmka[i,j-12,:]
            else:
                zkal=zm[i,j,:]*0.-99
            dr=0.125
            eps=1.0
            imu=3
            dnCoeff=[-0.01257341, -0.00933038]
            dncv=-0.2
            dnp=np.zeros((176),float)
            btop_=btop[i,j]
            bcf_=bcf[i,j]
            itype=1
            dn1d,dm1d,rrate1d,zkuc,zkasim,epst,\
                piaku,piaka,dzdn,dt1,dt2,dpiadn,\
                piakus,piakas = cmb.iter_profst_nobb(btop_,bzd_,bcf_,bsfc_,zkul,zkal,\
                                                     dr,eps,imu,itype,dnCoeff,dncv,dnp)
            bbb=bzd_+2
            if bcf_>bbb+1:
                nc=bsfc_-bcf_
                wzku=0.2
                wzka=0.1
                wpia=1
                nens=60
                dsrtPIA=pathAtten[i,j]*5
                reliabFlag=relFlag[i,j]
                rrate_out,dn_out,zkusimE,zkasimE,\
                    zku_out,zka_out,rrEns,yEns,xEns,dy,pia_out,\
                    dmOut= \
                        cmb.rainprofstg(zkul[bbb:bcf_+1],zkal[bbb:bcf_+1],\
                                        dsrtPIA,piakus,piakas,\
                                        reliabFlag,nc,dr,wzku,wzka,wpia,\
                                        rrate1d[bbb:bcf_+1],dn1d[bbb:bcf_+1],nens)
                rrate1d[bcf_]=rrate_out[-1]
                #print(piakus,piakas,rrate1d[bbb],rrate1d[bbt])
                bbt=bzd_-2
                #print(bzd_)
                pL[j].append([rrate1d[bbb],rrate1d[bbt],rrate1d[bcf_],sfcRain[i,j]])
                              
ic=0
for i in np.array(indx[:]):#ind2[-20:])[[2,11,12,15,16,18]]:
    ic+=1
    f=fs[i]
    #if not (('25384' in f) or ('25371' in f) or ('25380' in f)):
    #    continue
    #if not ( ('25302' in f) ):
    #    continue
    lat,lon,sfcRain,zm,zmka,fh,dayOfMonth,hh,\
        sfcType,h0,bzd,bcf,btop,pType,binBB,\
        binBBTop,bsfc,pathAtten,relFlag=readSfcRain(f)
    fh.close()
    fcmb=f.replace("dpr","cmb")
    #lon[lon<0]+=360
    sfcRainCMB,pRate,binNodes=readSfcRainCmb(fcmb)
   
    if 1==1:
        st_BB(pL,binBB,binBBTop,bcf,bsfc,btop,sfcType,pathAtten,relFlag,zm,zmka)
        st_noBB(pLnoBB,pType,binBB,binBBTop,bcf,bsfc,btop,bzd,sfcType,pathAtten,relFlag,zm,zmka)
        #stop
        ##
       
        
    continue
    plt.figure(figsize=(12,8))
    plt.suptitle(f)
    plt.subplot(411)
    plt.pcolormesh(sfcRainCMB.T,norm=matplotlib.colors.LogNorm(),cmap='jet',vmin=0.1,vmax=50)
    plt.colorbar()
    plt.subplot(412)
    plt.pcolormesh(sfcRain.T,norm=matplotlib.colors.LogNorm(),cmap='jet',vmin=0.1,vmax=50)
    plt.colorbar()
    plt.subplot(413)
    plt.pcolormesh(zm[:,24,].T,cmap='jet',vmin=0.1,vmax=45)
    plt.plot(bzd[:,24])
    plt.ylim(176,140)
    plt.colorbar()
    plt.subplot(414)
    plt.pcolormesh(zmka[:,12,].T,cmap='jet',vmin=0.1,vmax=40)
    plt.plot(bzd[:,24])
    plt.ylim(176,140)
    plt.colorbar()
    plt.figure()
    #if ('25371' in f):
    #    isc=24
    #if ('25380' in f):
    #    isc=152
    #isc=40
    #plt.subplot(211)
    #plt.pcolormesh(pRate[isc,:,::-1].T,norm=matplotlib.colors.LogNorm(),cmap='jet',vmin=0.1,vmax=50)
    #plt.ylim(0,50)
    #plt.subplot(212)
    #plt.plot(sfcRainCMB[isc,:])
    #plt.xlim(0,50)
    #plt.figure()
    #plt.pcolormesh(pType.T)
    #plt.colorbar()
    #stop


pL_s=[np.array(pL[i]).sum(axis=0) for i in range(49)]
pL_m=[np.array(pL[i]).mean(axis=0) for i in range(49)]
pLnoBB_s=[np.array(pLnoBB[i]).sum(axis=0) for i in range(49)]
pLnoBB_m=[np.array(pLnoBB[i]).mean(axis=0) for i in range(49)]
countnoBB=[len(pLnoBB[i]) for i in range(49)]
countBB=[len(pL[i]) for i in range(49)]
         
plt.figure(figsize=(6,8))
plt.suptitle('Southern Oceans')
plt.subplot(311)
plt.plot(np.array(pLnoBB_s)[:,-1]+np.array(pL_s)[:,-1])
plt.plot(np.array(pLnoBB_s)[:,-2]+np.array(pL_s)[:,-2])
plt.ylabel('Precipitation Volume (mm/h*Counts)')
plt.legend(['DPR','Combined'])
plt.subplot(312)
plt.plot((np.array(pLnoBB_s)[:,-1]+np.array(pL_s)[:,-1])/(np.array(countBB)+np.array(countnoBB)))
plt.plot((np.array(pLnoBB_s)[:,-2]+np.array(pL_s)[:,-2])/(np.array(countBB)+np.array(countnoBB)))
plt.ylabel('Precipitation rate (mm/h)')
plt.ylim(0,3)
plt.legend(['DPR','Combined'])
plt.subplot(313)
plt.plot(np.array(countBB))
plt.plot(np.array(countnoBB))
plt.xlabel('Ray')
plt.ylabel('Counts')
plt.legend(['BB','noBB'])
plt.tight_layout()
plt.savefig('crossTrackStats_SO_Ocean.png')

pickle.dump([pL,pLnoBB],open('dataSO.pklz','wb'))
