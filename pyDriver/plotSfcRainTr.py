fnameDPR='../DPRData/Atlantic/2A.GPM.DPR.V8-20180723.20180830-S183511-E200744.025593.V06A.HDF5'
fnameDPR='../monthly/SEAsia/2A.GPM.DPR.V8-20180723.20180602-S021248-E034522.024198.V06A.HDF5'
from netCDF4 import Dataset
import numpy as np
import pickle
labelst=pickle.load(open('labels_SO.pklz','rb'))

import glob
fs=glob.glob("out/dpr*HDF5")
fs=sorted(fs)
bzL=[[]for i in range(5)]
ind=[35,65,266,378,405,420,435]
ind2=[384, 134, 293, 303, 170,  72, 346, 322, 123, 341, 335, 397, 119,
      369, 186, 193, 191, 174, 110,  89, 393, 211, 374, 140, 196, 257,
      239,  95,  19, 175, 279,  65, 230, 396, 461, 180, 226, 237, 232,
      420,  17, 411, 435, 390, 104, 378,  35,  63, 266, 405]
ind2=[170,  78, 147,  58, 249, 284, 119, 117, 132, 247,  10,  26, 215,
      201, 261, 293, 248, 253,  34, 186, 272,  32, 107, 280, 224, 193,
      118,  57,  82,  39, 285, 255, 326, 304,  47,  71,  63, 140, 231,
      319, 262]
def readSfcRainS(fname):
    fh=Dataset(fname,'r')
    sfcRain=fh['NS/SLV/precipRateNearSurface'][:,:]
    return sfcRain
rainL=[]
#for f in fs:
#    rain=readSfcRainS(f)
#    rainL.append(rain.sum())
#stop
def readSfcRainCmb(fname):
    fh=Dataset(fname,'r')
    sfcRain=fh['NS/surfPrecipTotRate'][:,:]
    pRate=fh['NS/precipTotRate'][:,:,:]
    binNodes=fh['NS/phaseBinNodes'][:,:]
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
    return lat,lon,sfcRain,zm,zmka,fh,dayOfMonth,hh,sfcType,h0,bz,\
        bcf,btop,pType
countsT=[0,0,0,0,0]
countsR=[0,0,0,0,0]
sumR=[0,0,0,0,0]
ifs=0
orbCL=[]
rainL=[]

import matplotlib.pyplot as plt
import matplotlib

for i in ind2[-20:]:
    f=fs[i]
    lat,lon,sfcRain,zm,zmka,fh,dayOfMonth,hh,\
        sfcType,h0,bzd,bcf,btop,pType=readSfcRain(f)
    #fcmb=f.replace("dpr","cmb")
    #lon[lon<0]+=360
    #sfcRainCMB,pRate,binNodes=readSfcRainCmb(fcmb)
    plt.figure()
    plt.subplot(311)
    plt.pcolormesh(sfcRain.T,norm=matplotlib.colors.LogNorm(),cmap='jet',vmin=0.1,vmax=50)
    plt.colorbar()
    plt.subplot(312)
    plt.pcolormesh(zm[:,24,].T,cmap='jet',vmin=0.1,vmax=45)
    plt.plot(bzd[:,24])
    plt.ylim(176,100)
    plt.colorbar()
    plt.subplot(313)
    plt.pcolormesh(zmka[:,12,].T,cmap='jet',vmin=0.1,vmax=40)
    plt.plot(bzd[:,24])
    plt.ylim(176,100)
    plt.colorbar()
    #stop
