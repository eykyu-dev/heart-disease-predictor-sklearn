# -*- coding: utf-8 -*-
"""preprocessed.cleveland.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1rE2GqvvyjLwEAkSUpo8y-zETGLmtJeLa

## Data import
"""

import pandas as pd
import numpy as np
from google.colab import files
import io
uploaded = files.upload()

# can try processed.cleveland.data, processed.hungarian.data, processed.switzerland.data or processed.va.data
df = pd.read_csv(io.BytesIO(uploaded['processed.cleveland.data']), names=['age','sex','cp','trestbps','chol','fbs','restecg','thalach','exang','oldpeak','slope','ca','thal','target'])
df.head()

"""## Data cleaning"""

for cat in ['age','sex','cp','trestbps','chol','fbs','restecg','thalach','exang','oldpeak','slope','ca','thal','target']:
    if df[df[cat]== '?'].empty == False:
        print(df[df[cat]== '?'])

df.shape

# Remove columns with missing data
for cat in df:
    if df[df[cat] == '?'].empty == True: # if there is no missing value in a single category, then pass
        pass
    else:
        df.drop(df[df[cat] == '?'].index, inplace=True) # drop the row with missing data
df['ca'] = df['ca'].astype('float64')
df['thal'] = df['thal'].astype('float64')
df.shape

# lists of categorical attributes and numerical attributes
cat_att = ['age', 'sex','cp', 'fbs', 'restecg', 'exang', 'slope', 'thal']
num_att = ['trestbps','chol','thalach','oldpeak','ca']

"""## Visualizing data"""

# Reveal attribute correlation
import seaborn as sns
import matplotlib.pyplot as plt
plt.figure(figsize=(15, 12))
sns.heatmap(df.corr(),annot=True, vmin=-1, vmax=1, center= 0)
plt.title('original correlation matrix')

"""Target attribute<br>
num: Experiments with the Cleveland database have concentrated on simply attempting to distinguish presence (values 1,2,3,4) from absence (value 0)<br>
1. demographics<br>
age: age in years<br>
sex: sex (1 = male; 0 = female)<br>
2. current medical condition<br>
cp: chest pain type (Value 1: typical angina; Value 2: atypical angina; Value 3: non-anginal pain; Value 4: asymptomatic)<br>
trestbps: resting blood pressure (in mm Hg on admission to the hospital)<br>
chol: serum cholestoral in mg/dl<br>
fbs: (fasting blood sugar > 120 mg/dl) (1 = true; 0 = false)<br>
restecg: resting electrocardiographic results<br>
thalach: maximum heart rate achieved<br>
exang: exercise induced angina (1 = yes; 0 = no)<br>
oldpeak = ST depression induced by exercise relative to rest<br>
slope: the slope of the peak exercise ST segment<br>
ca: number of major vessels (0-3) colored by flourosopy<br>
thal: 3 = normal; 6 = fixed defect; 7 = reversable defect<br>
"""

# function that returns target label
def idd(val):
    if val == 0:
        return 'absence'
    else:
        return 'presence'

df_vis = df.copy()
df_vis['age']=df_vis['age'].astype('int64')
df_vis['target']=df_vis['target'].apply(idd) # generate target label
plt.figure(figsize=(7,5))
sns.countplot(data = df_vis, x = 'sex', hue='target') # plot occurence of heart disease in either gender
plt.title('Occurence of heart disease in different genders')

plt.figure(figsize=(10,4))
sns.countplot(data = df_vis, x = 'age', hue='target')  # plot occurence of heart disease in diff age groups
plt.title('Occurence of heart disease in different age groups')

sns.pairplot(df_vis,hue='target')

sns.pairplot(df_vis.drop(columns=['fbs','chol','restecg','trestbps','oldpeak','slope','ca']),hue='target')

"""## Transformation

## log transformation
"""

df_log = df.copy()
df_log['trestbps']=np.log(df_log['trestbps'])
df_log['chol']=np.log(df_log['chol'])
df_log['thalach']=np.log(df_log['thalach'])
plt.figure(figsize=(15, 12))
sns.heatmap(df_log.corr(),annot=True, vmin=-1, vmax=1, center= 0)
plt.title('correlation matrix after log transformation')

"""## Normalize data"""

from sklearn.preprocessing import MinMaxScaler
df_norm = df.copy()
scaler = MinMaxScaler()
for cat in df_norm.columns:
    if df_norm[cat].dtype == 'int64' or df_norm[cat].dtype == 'float64':
        df_norm[cat]= scaler.fit_transform(df_norm[cat].values.reshape(-1,1))
df_norm.head()

"""## Split dataset"""

# Split into training and testing sets
from sklearn.model_selection import train_test_split

X = df[['age','sex','cp','trestbps','chol','fbs','restecg','thalach','exang','oldpeak','slope','ca','thal']]
y = df['target']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30, random_state=42)
X_train.head()

y_train