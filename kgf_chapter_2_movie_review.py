# -*- coding: utf-8 -*-
"""KGF_Chapter-2_Movie_Review.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1w42_0wUqSTHerfHOvo2pBhuBqrX3vOdF

#  NLP through K.G.F. Chapter-2 Movie IMDb User Review

In this notebook the User Review of the movie KGF Chapter-2 in the IMDb website is used to train the classification model for classifying whether the review is negative ,neutral or positive.The data that is to be trained undergoes various stages of NLP , removing html from the text , removing punctuation,tokenizing,stemming etc..Here Naive Bayes Classifier ,Decision Tree Classifier and Random Forest Classifier are used for training the model.

I have used Octoparse tool for webscarping the IMDb data.

"""

# Connecting google drive to this notebook
from google.colab import drive
drive.mount('/content/drive')

"""### Loading the dataset and finding some insights from the data."""

# importing libraries
import pandas as pd
import numpy as np
import nltk
from bs4 import BeautifulSoup
import string
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from nltk.stem.porter import PorterStemmer

# importing the dataset 
data = pd.read_csv('/content/drive/MyDrive/KGF2 data.csv')
data.head()

# checking columns of the dataset
data.columns

# checking shape of the dataset
data.shape

# checking missing values of the dataset
data.isnull().sum()

# creating summary of the dataset
data.describe(include='all')

# creating overview of the dataset
data.info()

# evaluating frequency of score
data.Score.value_counts()

# creating a table with columns as Score and grouped by date
pd.crosstab(data['Date'],data['Score'])

# Plotting a graph
import seaborn as sns
import matplotlib.pyplot as plt 

plt.figure(figsize=(18,10))
sns.countplot(x="Date",hue="Score",data=data)

"""### Preparing the dataset for training the various classification model."""

# dropping useless columns from the dataframe 
data_1 = data.drop(['Title','Name','Date','actions'],axis=1)

# dropping rows from the dataframe with null values
data_1 = data_1.dropna(axis=0)

# checking shape of the dataframe
data_1.shape

# looking first 10 rows of the dataframe
data_1.head(10)

"""### Classifying Score into 3 categories negative ,neutral, positive

* 1 to 4   --> 0(**negative**)
* 5 to 7   --> 1(**neutral**)
* 8 to 10  --> 2(**positive**)

"""

# classifying score into 3 categories

x=0
for i in data_1['Score']:
  if i>7:
    i=2
  elif i<8 and i>4:
    i=1
  else:
    i=0
  data_1['Score'][x]=i
  x=x+1

# removing some end rows from the dataframe
data_1=data_1.drop(labels=range(1074,1079),axis=0)

# looking last 10 rows of the dataframe
data_1.tail(10)

# removing html text from the dataframe
def remove_htmltext(text):
  soup = BeautifulSoup(text,'lxml')
  html_free=soup.get_text()
  return html_free

data_1['text']=data_1['text'].apply(lambda x: remove_htmltext(x))

data_1.head()

# removing punctuation from the dataframe
def remove_punctuation(text):
  no_punct = "".join([c for c in text if c not in string.punctuation])
  return no_punct

data_1['text']=data_1['text'].apply(lambda x:remove_punctuation(x))

data_1.head()

# tokenizing the string of words into single word and changing into lower case
tokenizer = RegexpTokenizer(r'\w+')

data_1['text']=data_1['text'].apply(lambda x: tokenizer.tokenize(x.lower()))

data_1.head()

# removing the stopwords from the dataframe
nltk.download('stopwords')
def remove_stopwords(text):
  words = [w for w in text if w not in set(stopwords.words('english'))]
  return words

data_1['text']=data_1['text'].apply(lambda x:remove_stopwords(x))

data_1.head()

# applying stemming to the dataframe
stemmer = PorterStemmer()
def word_stemmer(text):
  stem_text = " ".join([stemmer.stem(i) for i in text])
  return stem_text

data_1['text']=data_1['text'].apply(lambda x:word_stemmer(x))

data_1.head()

# creating the Bag of Words model
corpus = []
corpus = data_1['text']
from sklearn.feature_extraction.text import CountVectorizer
cv = CountVectorizer(max_features = 1500)
X = cv.fit_transform(corpus).toarray()
y = data_1.iloc[:,0].values

# printing the predictor variable
print(X)

# printing the target variable
print(y)

"""### Splitting the dataset into training and test set."""

# splitting the dataset into training set and test set 
from sklearn.model_selection import train_test_split
X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.2,random_state=0)

"""### Training the dataset using classification model and analyzing accuracy of the model."""

# training the Naive Bayes Classification model to the training dataset
from sklearn.naive_bayes import GaussianNB
classifier = GaussianNB()
classifier.fit(X_train,y_train)

# predicting the values classified by the following model
y_pred = classifier.predict(X_test)

# calculating accuracy of the model by accuracy_score
from sklearn.metrics import accuracy_score
acc = accuracy_score(y_test,y_pred)
acc

# calculating accuracy of the model by confusion matrix
from sklearn.metrics import confusion_matrix
cm = confusion_matrix(y_test,y_pred)
print(cm)

# training the Decision tree Classification model
from sklearn.tree import DecisionTreeClassifier
classifier_1 = DecisionTreeClassifier(criterion="entropy",random_state=0)
classifier_1.fit(X_train,y_train)

y_pred_1 = classifier_1.predict(X_test)

acc_1 = accuracy_score(y_test,y_pred_1)
print(acc_1)

cm_1 = confusion_matrix(y_test,y_pred_1)
cm_1

# training the random forest classification model
from sklearn.ensemble import RandomForestClassifier
classifier_2 = RandomForestClassifier(n_estimators=10,criterion="entropy",random_state=0)
classifier_2.fit(X_train,y_train)

y_pred_2 = classifier_2.predict(X_test)

acc_2 = accuracy_score(y_test,y_pred_2)
acc_2

cm_2 = confusion_matrix(y_test,y_pred_2)
cm_2

"""#### <blockquote>Analyzing various classification models through accuracy_score and confusion matrix it is found that Randomforestclassifier model yields high accuracy.</blockquote>"""
