import pickle
import tensorflow as tf
from tensorflow.keras.layers import *
from tensorflow.keras.models import Sequential, Model
from tensorflow.keras.optimizers import Adam, RMSprop
import numpy as np
import combAlg as cmb
from numpy import *
cmb.mainfortpy()
cmb.initp2()

model=tf.keras.models.load_model('model_3layers_03.h5')
#stop
mlSet=pickle.load(open('mlSet_03.plkz','rb'))
xL=[]
yL=[]
nz=15
res=array([0.07591046, 1.07204676, 3.22332151, 3.11376803])
dmL=[]
for rec1 in mlSet[:]:
    zKu,zKa, rrEns,dmOut,attOut,dsrtPIA,nc=rec1
    zKu[zKu<0]=0
    zKu[zKu.mask==True]=0
    zKa[zKa<0]=0
    zKa[zKa.mask==True]=0
    x=[zKu[0:nz]/45,zKa[0:nz]/40]
    logAtt=np.log10(attOut[:nz,:]+1e-9)
    logAtt[logAtt<-4]=-4
    logAtt[:,0]=(4+logAtt[:,0])/3.0
    logAtt[:,1]=(3+logAtt[:,1])/3.0
    x1=[zKu[0:]/45,zKa[0:]/40]
    logAtt1=np.log10(attOut[:,:]+1e-9)
    logAtt1[logAtt1<-4]=-4
    logAtt1[:,0]=(4+logAtt1[:,0])/3.0
    logAtt1[:,1]=(3+logAtt1[:,1])/3.0
    ##yp=model.predict(np.array(x1))
    #yp=model.predict(np.array([np.array(x1).T]))
    #attKu=10**(3*yp[0,:,0]-4)
    #zKu_true=zKu+attKu.cumsum()*2
    #logattKa=3*yp[0,:,1]-3
    #dmRet=np.polyval(res,logattKa-log10(0.125)-0.1*zKu_true)
    #dmL.append([dmOut[-1],dmRet[-1]])
    yL.append(logAtt)
    xL.append(np.array(x).T)

xL=np.array(xL)
yL=np.array(yL)
nt=xL.shape[0]
r=np.random.random(nt)
a=np.nonzero(r<0.5)
b=np.nonzero(r>=0.5)
x_train=xL[a[0],:,:]
y_train=yL[a[0],:,:]
x_val=xL[b[0],:,:]
y_val=yL[b[0],:,:]

yp=model.predict(x_val[0:100000,:,:])
fout=open('mlData.txt','w')

for i in range(100000):
    for j in range(15):
        s='%6.3f %6.3f %6.3f %6.3f %6.3f %6.3f'%(x_val[i,j,0],x_val[i,j,1],\
                                                 y_val[i,j,0],y_val[i,j,1],yp[i,j,0],yp[i,j,1])
        #print(s)
        fout.write(s+'\n')
        

fout.close()
