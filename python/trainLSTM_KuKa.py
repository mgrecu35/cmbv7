import pickle
import tensorflow as tf
from tensorflow.keras.layers import *
from tensorflow.keras.models import Sequential, Model
from tensorflow.keras.optimizers import Adam, RMSprop
import numpy as np

print('reading training data!')
print('still reading...')
mlSet=pickle.load(open('mlSetCv_05.plkz','rb'))
print('reading done')
xL=[]
yL=[]
nz=25

for rec1 in mlSet:
    zKu,zKa,rrateOut,dmOut,dsrtPIA,nc=rec1
    zKu[zKu<0]=0
    zKu[zKu.mask==True]=0
    zKa[zKa<0]=0
    zKa[zKa.mask==True]=0
    x=[zKu[0:nz]/45,zKa[0:nz]/40.]
    logAtt=np.sqrt(rrateOut[:nz]+1e-9)
    y1=np.zeros((nz,2),float)
    y1[:,0]=dmOut[0:nz]/3.0
    y1[:,1]=(logAtt)/11.0
    if logAtt.max()==logAtt.max():
        yL.append(y1.copy())
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

def lstm_model(ndims=2):
    ntimes=None
    inp = tf.keras.layers.Input(shape=(ntimes,ndims,))
    out1 = tf.keras.layers.LSTM(4, return_sequences=True)(inp)
    out1 = tf.keras.layers.LSTM(4, return_sequences=True)(out1)
    out = tf.keras.layers.LSTM(2, return_sequences=True)(out1)
    model = tf.keras.Model(inputs=inp, outputs=out)
    return model

model=lstm_model(2)

model.compile(
    optimizer=tf.keras.optimizers.Adam(),  \
    loss='mse',\
    metrics=[tf.keras.metrics.MeanSquaredError()])

history = model.fit(x_train, y_train, batch_size=128,epochs=100,\
                    validation_data=(x_val, y_val))


model.save('modeldm_3layers_04_Cv_KuKa.h5')

import matplotlib
import matplotlib.pyplot as plt

yp=model.predict(x_val)
a1=np.nonzero(y_val[:,:,0]>0)
fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_aspect('equal')
plt.hist2d(3*y_val[:,:,0][a1],3*yp[:,:,0][a1],bins=0.3+np.arange(36)*0.075,norm=matplotlib.colors.LogNorm(),cmap='jet')
plt.xlabel("True Dm (mm)")
plt.ylabel("Predicted Dm (mm)")
plt.title("Dual Frequency Dm Retrievals")
c=plt.colorbar()
c.ax.set_title("Counts")
plt.savefig("DF_CV_Dm.png")

yp=model.predict(x_val)
fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_aspect('equal')
a1=np.nonzero(y_val[:,:,1]>0)
plt.hist2d(y_val[:,:,1][a1],yp[:,:,1][a1],bins=np.arange(25)*0.04,norm=matplotlib.colors.LogNorm(),cmap='jet')
