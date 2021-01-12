import tensorflow as tf

ndims=2
npia=2
ntimes=None
inp = tf.keras.layers.Input(shape=(ntimes,ndims,))
inp2 = tf.keras.layers.Input(shape=(2,))
out1 = tf.keras.layers.LSTM(4, return_sequences=True)(inp)
out = tf.keras.layers.LSTM(2, return_sequences=True)(out1)
att=tf.keras.backend.sum(tf.math.exp(out),axis=0)
#attKa=tf.math.exp(out[:,:,0])
#attKu=tf.math.exp(out[:,:,1])


#piaKa=tf.keras.backend.sum(attKa,axis=-1)
#dpiaKa=tf.keras.layers.Add()([inp2[:,-1],attKa[:,-1]])
#piaKa=tf.keras.layers.Add()([piaKa,dpiaKa])
#piaKu=tf.keras.backend.sum(attKu,axis=-1)
#dpia=tf.keras.layers.Subtract()([piaKa,piaKu])
model = tf.keras.Model(inputs=inp, outputs=[out])
inp_t=tf.Variable([[[1.0,2.0],[2.0,3.0],[2.0,4.0]],[[2.0,2.0],[2.0,3.0],[2.0,5.0]]])
inp2_t=tf.Variable([[1.0,2.0],[2.0,3.0]])
inp3=tf.Variable([[2.0],[2.0]])
inp4=tf.Variable([[2.0],[2.0]])

inpo1=tf.keras.layers.Input(shape=(1,))
inpo2=tf.keras.layers.Input(shape=(1,))
dpia1=inpo1*inpo2
model_2=tf.keras.Model(inputs=[inpo1,inpo2], outputs=dpia1)
o1=model_2(inp3,inp4)
