
# coding: utf-8

# # Predicting the Outcome of Cricket Matches

# In[1]:

import numpy as np # imports a fast numerical programming library
import pandas as pd #lets us handle data as dataframes
#sets up pandas table display
pd.set_option('display.width', 500)
pd.set_option('display.max_columns', 100)
pd.set_option('display.notebook_repr_html', True)
from sklearn.neighbors import KNeighborsClassifier
from sklearn import metrics
from patsy import dmatrices


# In[2]:

matches = pd.read_csv("../data/matcheswithfeatures.csv", index_col = 0)


# In[3]:

y, X = dmatrices('team1Winning ~ 0 + Avg_SR_Difference + Avg_WPR_Difference + Total_MVP_Difference + Prev_Enc_Team1_WinPerc +                   Total_RF_Difference', matches, return_type="dataframe")
y_arr = np.ravel(y)


# ### Splitting Training Set (2008-2013) and Test Set (2013-2015) based on Seasons

# In[4]:

X_timetrain = X.loc[X.index < 398]
Y_timetrain = y.loc[y.index < 398]
Y_timetrain_arr = np.ravel(Y_timetrain)
X_timetest = X.loc[X.index >= 398]
Y_timetest = y.loc[y.index >= 398]
Y_timetest_arr = np.ravel(Y_timetest)


# In[5]:

# Best values of k in time-based split data
knn1 = KNeighborsClassifier(n_neighbors = 31)
knn1.fit(X_timetrain, Y_timetrain_arr)



# In[6]:

def getPrediction(match_id):
    '''Returns the prediction for the given match
    
    Args: match_id (int): Match ID for the required game
    
    Returns: String: Predicted winner of the game and probability of victory 
    '''
    try:
        assert (399 <= match_id <= 517)
        results = {}
        match_row = matches.loc[matches['id'] == match_id]
        team1name = match_row.team1.unique()[0]
        team2name = match_row.team2.unique()[0]
        toPredict = X_timetest.loc[X_timetest.index == match_id-1].values
        prediction_prob = knn1.predict_proba(toPredict)
        prediction = knn1.predict(toPredict)
        if prediction[0] > 0:
            results['name'] = str(team1name)
            results['prob'] = float(prediction_prob[0][1])*100
        else:
            results['name'] = str(team2name)
            results['prob'] = float(prediction_prob[0][0])*100
        return results
    except:
        return None


