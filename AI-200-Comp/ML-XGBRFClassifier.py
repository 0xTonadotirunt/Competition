feature_cols = ["auction","device","country","log_bid_id","log_auction","log_device","log_time","log_country","log_ip","log_url","log_average_time","log_average_ip","log_average_url","average_time","num_bid_eq_time","bid_id_med", "auction_med", "time_med", "country_med", "ip_med","auc_med_train","time_med_train","country_med_train","ip_med_train"]

X = train_set[feature_cols]
y = train_set["outcome"]

X_kaggle = test_set[feature_cols]
X_kaggle

from sklearn.ensemble import RandomForestClassifier
import xgboost as xgb
from xgboost import XGBRFClassifier
from sklearn.model_selection import StratifiedKFold, KFold
from sklearn.metrics import accuracy_score, roc_auc_score 
import statistics

# DECISION_TREE_WEIGHT = 0.7 
model = XGBRFClassifier(n_estimators=300,learning_rate = 0.1, subsample=0.9, colsample_bynode=0.2,verbosity=0,)

skf = StratifiedKFold(n_splits=18)

sk_fold_auc = [] 

for train_index, test_index in skf.split(X,y):
    X_train, X_test = X.iloc[train_index], X.iloc[test_index]
    y_train, y_test = y.iloc[train_index], y.iloc[test_index] 
    
    new_model = model.fit(X_train,y_train)
    y_pred = model.predict(X_test)
    
    auc = roc_auc_score(y_test,y_pred)
    sk_fold_auc.append(auc)

sk_fold_mean_auc = statistics.mean(sk_fold_auc)

print('Average AUC:', round(sk_fold_mean_auc, 4)) 


#GENERATE AND EXPORT PREDICTIONS
final_model = model.fit(X, y)
probabilities = final_model.predict_proba(X_kaggle)
kaggle_preds = probabilities[:,1]  # Extract values from the rightmost column

output_dataframe = pd.DataFrame({
    'bidder_id': test_set['bidder_id'],
    'prediction': kaggle_preds
})
output_dataframe.to_csv('my_predictions.csv', index=False)  
