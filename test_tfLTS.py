import tensorflow as tf

ndims=2
npia=2
ntimes=None
inp = tf.keras.layers.Input(shape=(ntimes,ndims,))
inp2 = tf.keras.layers.Input(shape=(npia,))
out1 = tf.keras.layers.LSTM(4, return_sequences=True)(inp)
out = tf.keras.layers.LSTM(4, return_sequences=True)(out1)
att=tf.keras.backend.sum(tf.math.exp(out),axis=-1)
attKa=tf.math.exp(out[:,:,0])
attKu=tf.math.exp(out[:,:,1])
piaKa=tf.keras.backend.sum(attKa,axis=-1)
piaKu=tf.keras.backend.sum(attKu,axis=-1)
dpia=tf.keras.layers.Subtract()([piaKa,piaKu])
model = tf.keras.Model(inputs=inp, outputs=[out,dpia])
inp=tf.Variable([[[1.0,2.0],[2.0,3.0]],[[2.0,2.0],[2.0,3.0]]])
