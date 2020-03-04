#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import os
from keras.models import load_model
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences


# In[2]:


df = pd.read_csv('./dataset/lcquad2/LcQuadV2_question_with_id.csv')
df.head()


# In[3]:


df['question'].isnull().sum()


# In[4]:


df.dropna(subset=['question'],inplace=True)


# In[5]:


X_predict = df.question


# In[6]:


df2 = pd.read_csv('./dataset/PosNeg.csv')
title = df2.Question


# In[7]:


# take tokens and build word-in dictionary
tokenizer = Tokenizer(filters='!"#$%&()*+,-./:;<=>?@[\\]^_`{|}~\t\n',lower=True,split=" ")
tokenizer.fit_on_texts(title)


# In[8]:


#Predict DenseModel
# X_predict = ["who was the american general in the pacific during world war ii","where do guyanese people live","what is magic johnsons dads name"]
# model = load_model('./model/DenseModel.h5')
# x_predict_word_ids = tokenizer.texts_to_sequences(X_predict)
# x_predict = tokenizer.sequences_to_matrix(x_predict_word_ids, mode='binary')
# predict_test = model.predict(x_predict)
# predict_result = np.argmax(predict_test,axis=1)                           # 1 temporal   0 no-temporal
# print(predict_result)
# print(len(predict_result))


# In[9]:


#Predict CNN
# X_predict = ["Where was Grace Hopper educated at in 1930?", "when did lorin Maazel receive a grammy award?"]
model = load_model('./model/CNNModel2.0.h5')
x_predict_word_ids = tokenizer.texts_to_sequences(X_predict)
x_predict = pad_sequences(x_predict_word_ids, maxlen=20)
predict_test = model.predict(x_predict)
predict_result = np.argmax(predict_test,axis=1)                           # 1 temporal   0 no-temporal
print(predict_result)
print(len(predict_result))


# In[10]:


#Get the id of the question
def checkId(predict):
    for i in range(0, len(df['question'])):
        if predict == df['question'][i]:
            return df['id'][i]


# In[11]:


f0 = open("./dataset/lcquad2/output/id-no-temporal.txt", "w")
f1 = open("./dataset/lcquad2/output/id-temporal.txt", "w")
for i in range(0, len(X_predict)):
    id = str(checkId(X_predict.iloc[i]))
    if predict_result[i] == 0:
        f0.write(id + "|||" + X_predict.iloc[i] + "\n")
        f0.write(X_predict.iloc[i] + "\n")
    elif predict_result[i] == 1:
        f1.write(id + "|||" + X_predict.iloc[i] + "\n")
        f1.write(X_predict.iloc[i] + "\n")
f0.close()
f1.close()


# In[ ]:




