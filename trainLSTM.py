import pickle
import tensorflow as tf
from tensorflow.keras.layers import *
from tensorflow.keras.models import Sequential, Model
from tensorflow.keras.optimizers import Adam, RMSprop
import numpy as np


mlSet=pickle.load(open('mlSet_03.plkz','rb'))
xL=[]
yL=[]
for rec1 in mlSet:
    zKu,zKa, rrEns,dmOut,attOut,dsrtPIA,nc=rec1
    zKu[zKu<0]=0
    zKu[zKu.mask==True]=0
    zKa[zKa<0]=0
    zKa[zKa.mask==True]=0
    x=[zKu[0:5]/45,zKa[0:5]/40]
    logAtt=np.log10(attOut[:5,:]+1e-9)
    logAtt[logAtt<-4]=-4
    logAtt[:,0]=(4+logAtt[:,0])/3.0
    logAtt[:,1]=(3+logAtt[:,1])/3.0
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

def lstm_model(ndims=2):
    ntimes=None
    inp = tf.keras.layers.Input(shape=(ntimes,ndims,))
    out1 = tf.keras.layers.LSTM(4, return_sequences=True)(inp)
    out = tf.keras.layers.LSTM(2, return_sequences=True)(out1)
    model = tf.keras.Model(inputs=inp, outputs=out)
    return model

model=lstm_model()

model.compile(
    optimizer=tf.keras.optimizers.Adam(),  \
    loss='mse',\
    metrics=[tf.keras.metrics.MeanSquaredError()])

history = model.fit(x_train, y_train, batch_size=128,epochs=25,\
                    validation_data=(x_val, y_val))


model.save('model_05.h5')
