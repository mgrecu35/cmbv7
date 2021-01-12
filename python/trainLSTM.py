import pickle
import tensorflow as tf
from tensorflow.keras.layers import *
from tensorflow.keras.models import Sequential, Model
from tensorflow.keras.optimizers import Adam, RMSprop
import numpy as np

print('reading training data!')
print('still reading...')
mlSet=pickle.load(open('mlSet_04.plkz','rb'))
print('reading done')
xL=[]
yL=[]
nz=20

for rec1 in mlSet:
    zKu,zKa, rrEns,dmOut,attOut,dsrtPIA,nc=rec1
    zKu[zKu<0]=0
    zKu[zKu.mask==True]=0
    zKa[zKa<0]=0
    zKa[zKa.mask==True]=0
    x=[zKu[0:nz]/45]
    logAtt=np.log10(attOut[:nz,:]+1e-9)
    logAtt[logAtt<-4]=-4
    logAtt[:,0]=(4+logAtt[:,0])/3.0
    logAtt[:,1]=(3+logAtt[:,1])/3.0
    y1=dmOut[0:nz]/3.0
    yL.append(y1[:,np.newaxis])
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
    out = tf.keras.layers.LSTM(1, return_sequences=True)(out1)
    model = tf.keras.Model(inputs=inp, outputs=out)
    return model

model=lstm_model()

model.compile(
    optimizer=tf.keras.optimizers.Adam(),  \
    loss='mse',\
    metrics=[tf.keras.metrics.MeanSquaredError()])

history = model.fit(x_train, y_train, batch_size=128,epochs=150,\
                    validation_data=(x_val, y_val))


model.save('modeldm_3layers_04.h5')

import matplotlib
import matplotlib.pyplot as plt

yp=model.predict(x_val)
plt.hist2d(yp.flatten(),y_val.flatten(),bins=np.arange(41)*0.025,norm=matplotlib.colors.LogNorm(),cmap='jet')
