
import tensorflow as tf
from tensorflow import keras
from keras.layers import Dense,BatchNormalization
model = keras.models.Sequential()
model.add(Dense(8,input_shape=(3,),activation="relu"))
model.add(BatchNormalization())
model.add(Dense(8,activation="relu"))
model.add(BatchNormalization())
model.add(Dense(8,activation="relu"))
model.add(BatchNormalization())
model.add(Dense(8,activation="relu"))
model.add(BatchNormalization())
model.add(Dense(2,activation="linear"))


model.compile(loss='mse', optimizer='adam', metrics=['accuracy'])


import pickle

d=pickle.load(open("Chase_et_al_2021_NN-master/scalerXy.pklz","rb"))

xm=d["scaler_X_mean_scale"][0]
xs=d["scaler_X_mean_scale"][1]
ym=d["scaler_y_mean_scale"][0]
ys=d["scaler_y_mean_scale"][1]

from netCDF4 import Dataset
import numpy as np

def read_train():
    fname='Chase_et_al_2021_NN-master/Unrimed_simulation_wholespecturm_train_V2.nc'
    fh=Dataset(fname)
    nt=fh["Z"].shape[0]
    zKu_train=fh["Z"][:]+np.random.randn(nt)*0.1
    zKa_train=fh["Z2"][:]+np.random.randn(nt)*0.5
    iwc_train=fh["IWC"][:]
    temp_train=fh["T_env"][:]
    Nw_train=fh["Nw"][:]
    Dm_train=fh["Dm"][:]
    return zKu_train,zKa_train,temp_train, Nw_train,Dm_train

def read_test():
    fname='Chase_et_al_2021_NN-master/Unrimed_simulation_wholespecturm_test_V2.nc'
    fh=Dataset(fname)
    nt=fh["Z"].shape[0]
    zKu_train=fh["Z"][:]+np.random.randn(nt)*0.1
    zKa_train=fh["Z2"][:]+np.random.randn(nt)*0.5
    iwc_train=fh["IWC"][:]
    temp_train=fh["T_env"][:]
    Nw_train=fh["Nw"][:]
    Dm_train=fh["Dm"][:]
    return zKu_train,zKa_train,temp_train, Nw_train,Dm_train


zKu_train,zKa_train,temp_train, Nw_train,Dm_train=read_train()
zKu_test,zKa_test,temp_test, Nw_test,Dm_test=read_test()

X=np.array([zKu_train,zKu_train-zKa_train,temp_train]).T
for k in range(3):
    X[:,k]=(X[:,k]-xm[k])/xs[k]

y=np.array([np.log10(Nw_train),np.log10(Dm_train*1e3)]).T

for k in range(2):
    y[:,k]=(y[:,k]-ym[k])/ys[k]

X_t=np.array([zKu_test,zKu_test-zKa_test,temp_test]).T
for k in range(3):
    X_t[:,k]=(X_t[:,k]-xm[k])/xs[k]

y_t=np.array([np.log10(Nw_test),np.log10(Dm_test*1e3)]).T

for k in range(2):
    y_t[:,k]=(y_t[:,k]-ym[k])/ys[k]
    
model.fit(X, y, epochs=50, batch_size=64)
model.save('nw_dm_nn.h5')
#model = tf.keras.models.load_model('Chase_et_al_2021_NN-master/' + 'NN_6by8.h5',compile=True)
y_=model.predict(X_t)

print(np.corrcoef(y_[:,0],y_t[:,0])[0,1],np.corrcoef(y_[:,1],y_t[:,1])[0,1])
