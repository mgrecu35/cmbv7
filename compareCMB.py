f1='/gpmdata/2018/08/01/radar/2A.GPM.DPR.V8-20180723.20180801-S105937-E123210.025137.V06A.HDF5'
f2='out/test.h5'
f1='/gpmdata/2018/08/01/radar/2B.GPM.DPRGMI.CORRA2018.20180801-S105937-E123210.025137.V06A.HDF5'
from netCDF4 import Dataset
from numpy import *

def cmpRet(f1,f2):
    fh1=Dataset(f1)
    fh2=Dataset(f2)
    r1=fh1['NS/surfPrecipTotRate'][:,:]
    r2=fh2['NS/surfPrecipTotRate'][:,:]
    pType=(fh2['NS/Input/precipitationType'][:,:]/1e7).astype(int)
    a=nonzero(pType==1)
    rst=[r1[a].sum(),r2[a].sum()]
    a=nonzero(pType==2)
    rcv=[r1[a].sum(),r2[a].sum()]
    return rst,rcv

rst,rcv=cmpRet(f1,f2)
print(rst)
print(rcv)
