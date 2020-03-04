#!/usr/bin/env python
# coding: utf-8

# In[32]:


import pandas as pd
import numpy as np
import os
from keras.models import load_model
from keras.preprocessing.text import Tokenizer


# In[33]:


df = pd.read_csv('./dataset/lcquad2/lcquad2.csv').iloc[:, 0:11] 
df.head()


# In[34]:


df['question'].isnull().sum()


# In[35]:


df.dropna(subset=['question'],inplace=True)


# In[36]:


X_predict = df.question


# In[ ]:


df2 = pd.read_csv('./dataset/PosNeg.csv')
title = df2.Question


# In[37]:


# take tokens and build word-in dictionary
tokenizer = Tokenizer(filters='!"#$%&()*+,-./:;<=>?@[\\]^_`{|}~\t\n',lower=True,split=" ")
tokenizer.fit_on_texts(title)


# In[50]:


# X_predict = ["who was the american general in the pacific during world war ii","where do guyanese people live","what is magic johnsons dads name"]
model = load_model('./model/DenseModel.h5')
x_predict_word_ids = tokenizer.texts_to_sequences(X_predict)
x_predict = tokenizer.sequences_to_matrix(x_predict_word_ids, mode='binary')
predict_test = model.predict(x_predict)
predict_result = np.argmax(predict_test,axis=1)                           # 1 temporal   0 no-temporal
print(predict_result)
print(len(predict_result))


# In[51]:


f0 = open("./dataset/lcquad2/output/no-temporal.txt", "w")
f1 = open("./dataset/lcquad2/output/temporal.txt", "w")
for i in range(0, len(X_predict)):
    if predict_result[i] == 0:
        f0.write(X_predict.iloc[i] + "\n")
    elif predict_result[i] == 1:
        f1.write(X_predict.iloc[i] + "\n")
f0.close()
f1.close()


# In[ ]:




