# -*- coding: utf-8 -*-
"""
Created on Wed Nov  7 13:26:08 2018

@author: A-Bibeka
"""
%reset -f

import os
import pandas as pd
import numpy as np
from datetime import datetime
from datetime import date, timedelta # to get 1st Sunday of an year
import matplotlib.pyplot as plt # this is used for the plot the graph 
from sklearn.preprocessing import StandardScaler # for normalization
from sklearn.preprocessing import MinMaxScaler

## for Deep-learing:
import keras
from keras.layers import Dense
from keras.models import Sequential
from keras.utils import to_categorical
from keras.optimizers import SGD 
from keras.callbacks import EarlyStopping
from keras.utils import np_utils
import itertools
from keras.layers import LSTM
from keras.layers import Dropout

print('Current working directory ',os.getcwd())
#os.chdir("C:\\Users\\a-bibeka\\Documents\\GitHub\\RNN_TaxiDemand")"
os.chdir("/Users/Apoorb/Documents/GitHub/RNN_TaxiDemand")
print('Current working directory ',os.getcwd())

# load data
df = pd.read_csv('RNN_data.csv',index_col=0,parse_dates=True)
#df=df.drop(columns="NumTrip_0")
# split into train and test sets
values = df.values

#Check if the data is correct
Check_df=pd.DataFrame({"Y":df.Y,"Y-t":df.iloc[:,1:].sum(axis=1)})

n_train_time = int(np.floor(0.8*df.shape[0]))
train = values[:n_train_time, :]
test = values[n_train_time:, :]
##test = values[n_train_time:n_test_time, :]
# split into input and outputs
train_X, train_y = train[:, 1:], train[:, 0]
test_X, test_y = test[:, 1:], test[:, 0]
# reshape input to be 3D [samples, timesteps, features]
train_X = train_X.reshape((train_X.shape[0], train_X.shape[1],1))
test_X = test_X.reshape((test_X.shape[0], test_X.shape[1],1))
print(train_X.shape, train_y.shape, test_X.shape, test_y.shape) 
# We reshaped the input into the 3D format as expected by LSTMs, namely [samples, timesteps, features].



# design network
model = Sequential()
model.add(LSTM(50, input_shape=(train_X.shape[1], train_X.shape[2])))
model.add(LSTM(250))
model.add(Dense(1))
model.compile(loss='mae', optimizer='adam')
# fit network
history = model.fit(train_X, train_y, epochs=200, batch_size=72, validation_data=(test_X, test_y), verbose=2, shuffle=False)

# summarize history for loss
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper right')
plt.show()


# make a prediction
yhat = model.predict(test_X)
test_X = test_X.reshape((test_X.shape[0], 168))
# invert scaling for forecast
inv_yhat = np.concatenate((yhat, test_X[:, -167:]), axis=1)
inv_yhat = scaler.inverse_transform(inv_yhat)
inv_yhat = inv_yhat[:,0]
# invert scaling for actual
test_y = test_y.reshape((len(test_y), 1))
inv_y = np.concatenate((test_y, test_X[:, -6:]), axis=1)
inv_y = scaler.inverse_transform(inv_y)
inv_y = inv_y[:,0]
# calculate RMSE
rmse = np.sqrt(mean_squared_error(inv_y, inv_yhat))
print('Test RMSE: %.3f' % rmse)

