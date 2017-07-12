
# coding: utf-8

# In[105]:

import findspark
findspark.init()
from pyspark import SparkContext
from pyspark import SparkConf


# In[91]:


import pandas as pd
import numpy as np
from sklearn import grid_search, datasets
from spark_sklearn import GridSearchCV
from sklearn import ensemble
from pyspark.sql import SparkSession
from spark_sklearn.util import createLocalSparkSession
from patsy import dmatrices
from sklearn import metrics
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn import svm
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB


# In[92]:




# In[93]:

df = pd.read_csv("../data/matcheswithfeatures.csv", index_col = 0)
df.tail()


# In[94]:

spark = createLocalSparkSession()


# In[95]:

y, X = dmatrices('team1Winning ~ 0 + Avg_SR_Difference + Avg_WPR_Difference + Total_MVP_Difference + Prev_Enc_Team1_WinPerc +                   Total_RF_Difference', df, return_type="dataframe")
y_arr = np.ravel(y)


# In[96]:

X.tail()


# In[97]:

X_timetrain = X.loc[X.index < 398]
Y_timetrain = y.loc[y.index < 398]
Y_timetrain_arr = np.ravel(Y_timetrain)
X_timetest = X.loc[X.index >= 398]
Y_timetest = y.loc[y.index >= 398]
Y_timetest_arr = np.ravel(Y_timetest)
X_timetest


# In[99]:

tuned_parameters = {
    "n_estimators": [ 100 ],
    "max_depth" : [ 3 ],
    "learning_rate": [ 0.1 ],
}
gbc = ensemble.GradientBoostingClassifier()
clf = GridSearchCV(spark.sparkContext, gbc, tuned_parameters)
clf


# In[100]:

clf.fit(X_timetrain, Y_timetrain_arr)
clftest_pred = clf.predict(X_timetest)
print "Accuracy is ", metrics.accuracy_score(Y_timetest_arr, clftest_pred) *100, "%"


# In[101]:

knn1 = KNeighborsClassifier()
knn_params = {
    "n_neighbors": [31]
}
clf2 = GridSearchCV(spark.sparkContext, knn1, knn_params, n_jobs = 2)
clf2


# In[102]:

clf2.fit(X_timetrain, Y_timetrain_arr)
clf2test_pred = clf2.predict(X_timetest)
print "Accuracy is ", metrics.accuracy_score(Y_timetest_arr, clf2test_pred) *100, "%"


# In[ ]:



