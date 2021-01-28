fnameDPR='../DPRData/Atlantic/2A.GPM.DPR.V8-20180723.20180830-S183511-E200744.025593.V06A.HDF5'
fnameDPR='../monthly/SEAsia/2A.GPM.DPR.V8-20180723.20180602-S021248-E034522.024198.V06A.HDF5'
from netCDF4 import Dataset
import numpy as np
import pickle
labelst=pickle.load(open('labels_SO.pklz','rb'))

import glob
fs=glob.glob("out/dpr.15_45*HDF5")
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
indx=range(327)
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
    bcf_ms=fh['MS/PRE/binClutterFreeBottom'][:,:]
    btop=fh['NS/PRE/binStormTop'][:,:]
    pType=(fh['NS/CSF/typePrecip'][:,:]/1e7).astype(int)
    binBB=fh['NS/CSF/binBBPeak'][:,:]
    binBBTop=fh['NS/CSF/binBBTop'][:,:]
    bsfc=fh['NS/PRE/binRealSurface'][:,:]
    pathAtten=fh['NS/SRT/pathAtten'][:,:]
    rFlag=fh['NS/SRT/reliabFlag'][:,:]
    piaHyb=fh['NS/SRT/PIAhybrid'][:,:]
    #print(fh['NS/SRT/'])
    #stop
    print(lat.mean(),lat.min(),lat.max())
    return lat,lon,sfcRain,zm,zmka,fh,dayOfMonth,hh,sfcType,h0,bz,\
        bcf,btop,pType,binBB,binBBTop,bsfc,pathAtten,rFlag,bcf_ms,piaHyb
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
def st_BB(pL,binBB,binBBTop,bcf,bsfc,btop,sfcType,pathAtten,relFlag,zm,zmka,f):
    for j in range(49):
        a=np.nonzero(binBB[:,j]>0)
        b=np.nonzero(sfcType[:,j][a]!=0)
        for i in a[0][b]:
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
            dnst=-0.1
            dnp=np.zeros((176),float)
            btop_=btop[i,j]
            bcf_=bcf[i,j]
            dn1d,dm1d,rrate1d,zkuc,zkasim,epst,piaku,piaka,\
                dzdn,dpiadn,piakus,piakas = cmb.iter_profst(btop_,bzd_,bb,bbt,bbb,bcf_,bsfc_,zkul,zkal,\
                                                            dr,eps,imu,dnst,dnCoeff,dnp)

            #dn1d,dm1d,rrate1d,zkuc,zkasim,epst,piaku,piaka,dzdn,\
            #    rrate1d_sub,dn_sub,dm_sub,zkuc_sub,piahb_sub,\
            #    piaka_sub,zetas = cmb.iter_profcv2(btop_,bzd_,bcf_,bsfc,zkul,zkal,dr,eps,\
            #                                       imu,itype,dncv,dnp,piasrtku,relpiasrtku)
	    
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
                #print(rrate1d[bcf_],rrate_out[-1])
                rrateOld=rrate1d[bcf_]
                rrate1d[bcf_]=rrate_out[-1]
                #print(piakus,piakas,rrate1d[bbb],rrate1d[bbt])
                if rrate1d[bcf_]<300:
                    pL[j].append([rrate1d[bbb],rrate1d[bbt],rrate1d[bcf_],rrateOld,sfcRain[i,j]])
                else:
                    print(f,i,j)

def st_noBB(pL,pType,binBB,binBBTop,bcf,bsfc,btop,bzd,sfcType,pathAtten,relFlag,zm,zmka,f):
    for j in range(49):
        a=np.nonzero(binBB[:,j]<=0)
        b=np.nonzero(pType[:,j][a]==1)
        c=np.nonzero(sfcType[:,j][a][b]!=0)
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
            dncv=-0.1
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
                rrateOld=rrate1d[bcf_]
                rrate1d[bcf_]=rrate_out[-1]
                #print(piakus,piakas,rrate1d[bbb],rrate1d[bbt])
                bbt=bzd_-2
                #print(bzd_)
                if rrate1d[bcf_]<300:
                    pL[j].append([rrate1d[bbb],rrate1d[bbt],rrate1d[bcf_],rrateOld,sfcRain[i,j]])
                else:
                    print(f,i,j)
                              
ic=0
pathAttenR=np.zeros((49),float)
piaHybR=np.zeros((49),float)
zsfc=np.zeros((49),float)
zsfcKa=np.zeros((49),float)
countR=np.zeros((49),float)
for i in np.array(indx[:]):#ind2[-20:])[[2,11,12,15,16,18]]:
    ic+=1
    f=fs[i]
    #if not (('25384' in f) or ('25371' in f) or ('25380' in f)):
    #    continue
    #if not ( ('25302' in f) ):
    #    continue
    lat,lon,sfcRain,zm,zmka,fh,dayOfMonth,hh,\
        sfcType,h0,bzd,bcf,btop,pType,binBB,\
        binBBTop,bsfc,pathAtten,relFlag,bcf_ms,piaHyb=readSfcRain(f)

    for j in range(49):
        a=np.nonzero(pType[:,j]==1)
        b=np.nonzero(sfcType[:,j][a]!=0)
      
        for k in (a[0][b]):
            if (relFlag[k,j]==1 or relFlag[k,j]==2) and piaHyb.mask[k,j]==False:
                pathAttenR[j]+=pathAtten[k,j]
                piaHybR[j]+=piaHyb[k,j]
                zsfc[j]+=10**(0.1*zm[k,j,bcf[k,j]-1])
                #print(piaHyb[k,j],pathAtten[k,j])
                if abs(j-24)<13:
                    zsfcKa[j]+=10**(0.1*zmka[k,j-12,bcf_ms[k,j-12]])
                countR[j]+=1
        c=np.nonzero(piaHybR!=piaHybR)
        if len(c[0])>0:
            stop
            
plt.figure(figsize=(6,8))
plt.subplot(311)
plt.plot((piaHybR/countR))
plt.plot((pathAttenR/countR))
plt.ylabel('PIA(Ku)(dB)')
plt.legend(['DSRT','Hybrid'])
plt.subplot(312)
plt.plot(np.log10(zsfc/countR)*10)
plt.ylabel('Z_sfc(Ku)(dBZ)')
plt.subplot(313)
plt.plot(countR)
plt.ylabel('Counts')
plt.xlabel('Ray')
plt.tight_layout()
plt.savefig('threeHumps.png')

stop
plt.figure(figsize=(6,8))
plt.suptitle('Mid-latitude Stratiform Precipitation Land')
plt.subplot(311)
plt.plot(np.array(pLnoBB_s)[:,-1]+np.array(pL_s)[:,-1])
plt.plot(np.array(pLnoBB_s)[:,-3]+np.array(pL_s)[:,-3])
plt.ylabel('Precipitation Volume (mm/h*Counts)')
plt.legend(['DPR','Combined'])
plt.subplot(312)
plt.plot((np.array(pLnoBB_s)[:,-1]+np.array(pL_s)[:,-1])/(np.array(countBB)+np.array(countnoBB)))
plt.plot((np.array(pLnoBB_s)[:,-3]+np.array(pL_s)[:,-3])/(np.array(countBB)+np.array(countnoBB)))
plt.plot((np.array(pLnoBB_s)[:,-2]+np.array(pL_s)[:,-2])/(np.array(countBB)+np.array(countnoBB)))
plt.plot((np.array(pL_s)[:,-3])/(np.array(countBB)))
plt.plot((np.array(pLnoBB_s)[:,-3])/(np.array(countnoBB)))
plt.ylabel('Precipitation rate (mm/h)')
plt.ylim(0,3.5)
plt.legend(['DPR','CMB_DF','CMB_SF','CMB_DF_BB','CMB_DF_noBB'],ncol=3,loc=8)
plt.subplot(313)
plt.plot(np.array(countBB))
plt.plot(np.array(countnoBB))
plt.plot(0.5*(np.array(countBB)+np.array(countnoBB)))
plt.xlabel('Ray')
plt.ylabel('Counts')
plt.legend(['BB','noBB','Average'])
plt.tight_layout()
plt.savefig('crossTrackStats_MidLandSt.png')
pickle.dump([pL,pLnoBB],open('dataTropicsMidLE.pklz','wb'))
r2=(np.array(pLnoBB_s)[:,-2]+np.array(pL_s)[:,-2])/(np.array(countBB)+np.array(countnoBB))
r3=(np.array(pLnoBB_s)[:,-3]+np.array(pL_s)[:,-3])/(np.array(countBB)+np.array(countnoBB))
r1=(np.array(pLnoBB_s)[:,-1]+np.array(pL_s)[:,-1])/(np.array(countBB)+np.array(countnoBB))

