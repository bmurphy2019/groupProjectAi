# -*- coding: utf-8 -*-
"""heartDiseaseAi.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1H6VP92GbQO7HoZTV3YnGn6HVQJTuW8CA
"""

# Brian Murphy R00189335
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation
from keras.callbacks import ModelCheckpoint

# import the csv
df = pd.read_csv('/content/cleveland.csv', header = None)

df.columns = ['age', 'sex', 'cp', 'trestbps', 'chol',
              'fbs', 'restecg', 'thalach', 'exang', 
              'oldpeak', 'slope', 'ca', 'thal', 'target']

# data cleaning
df.isnull().sum()

df['target'] = df.target.map({0: 0, 1: 1, 2: 1, 3: 1, 4: 1})
df['thal'] = df.thal.fillna(df.thal.mean())
df['ca'] = df.ca.fillna(df.ca.mean())


# assign target to Y everything else to X
X = df.iloc[:, :-1].values
y = df.iloc[:, -1].values

# 80-20 train test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=0)

# create the model
model = Sequential()
model.add(Dense(30, input_dim=13, activation='tanh'))
model.add(Dense(20, activation='tanh'))
model.add(Dense(1, activation='sigmoid'))

model.compile(optimizer='adam',loss='binary_crossentropy',metrics=['acc'])

# train and checkpoint
checkpointer = ModelCheckpoint('heartDisease.h5', monitor='val_acc', mode='max', verbose=2, save_best_only=True)
history=model.fit(X_train, y_train, batch_size=32, epochs=350, validation_data=(X_test, y_test), callbacks=[checkpointer])

present_model = keras.models.load_model('heartDisease.h5')
print("Accuracy of our model on test data : " , present_model.evaluate(X_test,y_test)[1]*100 , "%")

import tensorflow as tf

# Convert the model.
converter = tf.lite.TFLiteConverter.from_keras_model(keras.models.load_model('heartDisease.h5'))
tflite_model = converter.convert()

# Save the model.
with open('heartDisease.tflite', 'wb') as f:
  f.write(tflite_model)