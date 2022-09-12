from netCDF4 import Dataset
from pyresample import kd_tree, geometry
import numpy as np

def readData(f1_,f2_,f3_,n1,n2):
    fh=Dataset(f1_)
    lon=fh["FS/Longitude"][n1:n2,:]
    lat=fh["FS/Latitude"][n1:n2,:]
    icount=0
    for lon1,lat1 in zip(lon[:,24],lat[:,24]):
        if lon1>-110 and lon1<-65 and lat1>30 and lat1<60:
            icount+=1
    zKu=fh["FS/PRE/zFactorMeasured"][n1:n2,:,:,:]
    sfcType=fh["FS/PRE/landSurfaceType"][n1:n2,:]
    pType=fh["FS/CSF/typePrecip"][n1:n2,:]
    pType=(pType/1e7).astype(int)
    fh_cmb=Dataset(f2_)
    qv=fh_cmb["KuKaGMI/vaporDensity"][n1:n2,:,:]
    press=fh_cmb["KuKaGMI/airPressure"][n1:n2,:,:]
    envNodes=fh_cmb["KuKaGMI/envParamNode"][n1:n2,:,:]
    airTemp=fh_cmb["KuKaGMI/airTemperature"][n1:n2,:,:]
    skTemp=fh_cmb["KuKaGMI/skinTemperature"][n1:n2,:]
    binNodes=fh_cmb["KuKaGMI/phaseBinNodes"][n1:n2,:]
    bcf=fh["FS/PRE/binClutterFreeBottom"][n1:n2,:]
    bsf=fh["FS/PRE/binRealSurface"][n1:n2,:,:]
    pwc=fh_cmb["KuKaGMI/precipTotWaterCont"][n1:n2,:,:]
    sfcEmiss=fh_cmb["KuKaGMI/surfEmissivity"][n1:n2,:,:]
    dm=fh_cmb["KuKaGMI/precipTotDm"][n1:n2,:,:]
    cldw=fh_cmb["KuKaGMI/cloudLiqWaterCont"][n1:n2,:,:]
    sfcBin=fh_cmb["KuKaGMI/Input/surfaceRangeBin"][n1:n2,:,:]
    sfcPrecip=fh["FS/SLV/precipRateNearSurface"][n1:n2,:]
    bbPeak=fh["FS/CSF/binBBPeak"][n1:n2,:]
    #print(fh["FS/PRE"])
    #print(fh["FS/VER"])
    h0=fh["FS/VER/heightZeroDeg"][n1:n2,:]
    pRateCMB=fh_cmb["KuKaGMI/precipTotRate"][n1:n2,:,:]
    h0=fh["FS/VER/heightZeroDeg"][n1:n2,:]
    #print(fh_cmb["KuKaGMI"])
    #stop
    fh.close()
    fh_cmb.close()
    a=np.nonzero(pType==1)
    fh_gmi=Dataset(f3_)
    gmi_lon=fh_gmi["S1/Longitude"][:]
    gmi_lat=fh_gmi["S1/Latitude"][:]
    tc=fh_gmi["S1/Tc"][:]
    gmi_lon2=fh_gmi["S2/Longitude"][:]
    gmi_lat2=fh_gmi["S2/Latitude"][:]
    tc2=fh_gmi["S2/Tc"][:]
    sat_lon=fh_gmi['S1/SCstatus/SClongitude'][:]
    dlon=(sat_lon-gmi_lon[:,110]).mean()
    swath_def = geometry.SwathDefinition(lons=gmi_lon, lats=gmi_lat)
    swath_def2 = geometry.SwathDefinition(lons=gmi_lon2, lats=gmi_lat2)
    target_def = geometry.SwathDefinition(lons=lon[:,:], lats=lat[:,:])
    tc_regrid = kd_tree.resample_gauss(swath_def, tc[:,:,:],
                                       target_def, radius_of_influence=25000, \
                                       sigmas=[12500 for k in range(9)])
    tc_regrid2 = kd_tree.resample_gauss(swath_def2, tc2[:,:,:],
                                        target_def, radius_of_influence=25000, \
                                    sigmas=[12500 for k in range(4)])

    umu=np.cos(53/180.0*np.pi)
    bsf1=bsf[:,:,0]
    n1=qv.shape[0]
    #print(envNodes[132,14,:])
    #print(airTemp.shape)
    #print(envNodes[:,:,0].min(),envNodes[:,:,0].max())
    #print(cldw.shape)
    #print(umu)
    #print(skTemp.shape)
    #print(sfcEmiss.shape)
    a=np.nonzero(pType>0)
    print(len(a[0]))
        
    return qv,press,sfcType,pType,airTemp,envNodes,binNodes,\
        bcf,bsf1,pwc,sfcEmiss,dm,skTemp,lon,lat,tc_regrid,tc_regrid2,zKu,cldw,bbPeak,h0,pRateCMB,h0