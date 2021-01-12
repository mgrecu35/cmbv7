import tensorflow as tf
from tensorflow.keras.layers import *
from tensorflow.keras.models import Sequential, Model
from tensorflow.keras.optimizers import Adam, RMSprop
import numpy as np

def modTest():
    input1 = Input(shape=(1,))
    input2 = Input(shape=(1,))
    input = Concatenate()([input1, input2])
    x = Dense(2)(input)
    x = Dense(2)(x)
    x1 = tf.keras.backend.sum(x,axis=1)
    x2=Multiply()([x1,input1])[:,0]
    modTest = Model(inputs=[input1, input2], outputs=[x,x1,x2])
    return modTest

mod=modTest()
inp3=tf.Variable(np.array([[3.0],[4.0],[5]],np.float32))
inp4=tf.Variable(np.array([[2.0],[2.0],[3]],np.float32))
