#DATA PREPARATION
import pandas as pd 

bids_df = pd.read_csv("data2/bids.csv")
train_df = pd.read_csv("data2/train.csv")
test_df = pd.read_csv("data2/test.csv")

import warnings 

warnings.filterwarnings("ignore")

bids_bidder_ids = list(bids_df.bidder_id.unique())
train_bidder_ids = list(train_df.bidder_id)
test_bidder_ids = list(test_df.bidder_id)

train_not_found = []
test_not_found = [] 

for trainbidderid in train_bidder_ids:
    if trainbidderid not in bids_bidder_ids:
        train_not_found.append(trainbidderid)

for testbidderid in test_bidder_ids:
    if testbidderid not in bids_bidder_ids:
        test_not_found.append(testbidderid)


print(f"{len(train_not_found)} bidders from train.csv are not found in bids.csv.")
print(f"{len(test_not_found)} bidders from test.csv are not found in bids.csv.")

#FEATURE ENGINEERING
##Find number of bids for each bidder_id
bidder_counts = bids_df.groupby("bidder_id")['auction'].count().reset_index()
bidder_counts = bidder_counts.rename(columns={"auction":"num_bids"})

##Convert number of bids > log(number of bids)
import numpy as np
bidder_counts['log+1'] = (bidder_counts['num_bids']+1).transform(np.log)

##merge bidder_counts df with train df
feature_set = train_df.merge(bidder_counts,on="bidder_id",how="left")
feature_set["num_bids"] = feature_set["num_bids"].fillna(0)
feature_set["log+1"] = feature_set["log+1"].fillna(0)

bidder_unique = bids_df.groupby("bidder_id").nunique().reset_index()
bidder_unique['log_bid_id'] = (bidder_unique['bid_id']+1).transform(np.log)

bidder_unique["average_ip"]  = (bidder_unique["ip"] / bidder_unique["auction"])
bidder_unique["average_device"] = bidder_unique["device"] / bidder_unique["auction"]
bidder_unique["average_time"] = bidder_unique["time"] / bidder_unique["auction"]
bidder_unique["average_country"] = bidder_unique["country"] / bidder_unique["auction"]
bidder_unique["average_url"] = bidder_unique["url"] / bidder_unique["auction"]

#Add in new features 
##if data > feature_median (of bidder_unique ) : 0
##if data < feature_median (of bidder_unique ) : 1
## Medians of each features
bid_id_median = bidder_unique["bid_id"].median()
auction_median = bidder_unique["auction"].median()
device_median = bidder_unique["device"].median()
time_median = bidder_unique["time"].median()
country_median = bidder_unique["country"].median()
ip_median = bidder_unique["ip"].median()
url_median = bidder_unique["url"].median()

##function used
def more_than_med(input_num, median):
    if input_num > median:
        return 1
    return 0

##new columns using .apply()
bidder_unique["bid_id_med"] = bidder_unique.apply(lambda x: more_than_med(x["bid_id"],bid_id_median),axis=1)
bidder_unique["auction_med"] = bidder_unique.apply(lambda x: more_than_med(x["auction"],auction_median),axis=1)
bidder_unique["device_med"] = bidder_unique.apply(lambda x: more_than_med(x["device"],device_median),axis=1)
bidder_unique["time_med"] = bidder_unique.apply(lambda x: more_than_med(x["time"],time_median),axis=1)
bidder_unique["country_med"] = bidder_unique.apply(lambda x: more_than_med(x["country"],country_median),axis=1)
bidder_unique["ip_med"] = bidder_unique.apply(lambda x: more_than_med(x["ip"],ip_median),axis=1)
bidder_unique["url_med"] = bidder_unique.apply(lambda x: more_than_med(x["url"],url_median),axis=1)
bidder_unique

##merge bidder_unique with train_set and test_set
train_set = train_df.merge(bidder_unique,on="bidder_id",how="left")
test_set = test_df.merge(bidder_unique,on="bidder_id",how="left")

train_set[["log_bid_id","merchandise"]] = train_set[["log_bid_id","merchandise"]].fillna(0)
train_set[["auction","device","time","country","ip","url"]] = train_set[["auction","device","time","country","ip","url"]].fillna(train_set[["auction","device","time","country","ip","url"]].median())
train_set[["average_device","average_time","average_country","average_ip","average_url"]] = train_set[["average_device","average_time","average_country","average_ip","average_url"]].fillna(train_set[["average_device","average_time","average_country","average_ip","average_url"]].median())
test_set[["log_bid_id","merchandise"]] = test_set[["log_bid_id","merchandise"]].fillna(0)
test_set[["auction","device","time","country","ip","url"]] = test_set[["auction","device","time","country","ip","url"]].fillna(test_set[["auction","device","time","country","ip","url"]].median())
test_set[["average_device","average_time","average_country","average_ip","average_url","average_country"]] = test_set[["average_device","average_time","average_country","average_ip","average_url","average_country"]].fillna(test_set[["average_device","average_time","average_country"]].median())

##new features for train_set and test_set 
###log_(feature)
train_set['log_auction'] = (train_set['auction']+1).transform(np.log)
train_set['log_device'] = (train_set['device']+1).transform(np.log)
train_set['log_time'] = (train_set['time']+1).transform(np.log)
train_set['log_country'] = (train_set['country']+1).transform(np.log)
train_set['log_ip'] = (train_set['ip']+1).transform(np.log)
train_set['log_url'] = (train_set['url']+1).transform(np.log)

test_set['log_auction'] = (test_set['auction']+1).transform(np.log)
test_set['log_url'] = (test_set['url']+1).transform(np.log)
test_set['log_device'] = (test_set['device']+1).transform(np.log)
test_set['log_time'] = (test_set['time']+1).transform(np.log)
test_set['log_country'] = (test_set['country']+1).transform(np.log)
test_set['log_ip'] = (test_set['ip']+1).transform(np.log)

###log_average_(feature)
train_set['log_average_device'] = (train_set['average_device']+1).transform(np.log)
train_set['log_average_time'] = (train_set['average_time']+1).transform(np.log)
train_set['log_average_country'] = (train_set['average_country']+1).transform(np.log)
train_set['log_average_ip'] = (train_set['average_ip']+1).transform(np.log)
train_set['log_average_url'] = (train_set['average_url']+1).transform(np.log)

test_set['log_average_url'] = (test_set['average_url']+1).transform(np.log)
test_set['log_average_device'] = (test_set['average_device']+1).transform(np.log)
test_set['log_average_time'] = (test_set['average_time']+1).transform(np.log)
test_set['log_average_country'] = (test_set['average_country']+1).transform(np.log)
test_set['log_average_ip'] = (test_set['average_ip']+1).transform(np.log)

### check if bid_id == time. theoretically, a human will not be able to bid multiple times per second
#Function used
def check_num_bid_eq_time(bid_id, time):
    
    if bid_id == time:
        return 1
    else:
        return 0 
    
#Create new columns
train_set["num_bid_eq_time"] = train_set.apply(lambda x: check_num_bid_eq_time(x["bid_id"],x["time"]),axis=1)
test_set["num_bid_eq_time"] = test_set.apply(lambda x: check_num_bid_eq_time(x["bid_id"],x["time"]),axis=1)

# Adding special func features to train_set # 
### if the auction 
def outcome_to_binary(param_median,train_median):
    if param_median > train_median:
        return 1 
    return 0
    
#Median for each of the features
auc_train_median = train_set["auction"].median()
dev_train_median = train_set["device"].median()
time_train_median = train_set["time"].median()
country_train_median = train_set["country"].median()
ip_train_median = train_set["ip"].median()
url_train_median = train_set["url"].median()
    
#New columns
train_set["auc_med_train"] = train_set.apply(lambda x: outcome_to_binary(x["auction"],auc_train_median), axis=1)
train_set["dev_med_train"] = train_set.apply(lambda x: outcome_to_binary(x["device"], dev_train_median), axis=1)
train_set["time_med_train"] = train_set.apply(lambda x: outcome_to_binary(x["time"], time_train_median), axis=1)
train_set["country_med_train"] = train_set.apply(lambda x: outcome_to_binary(x["country"], country_train_median), axis=1)
train_set["ip_med_train"] = train_set.apply(lambda x: outcome_to_binary(x["ip"], ip_train_median), axis=1)
train_set["url_med_train"] = train_set.apply(lambda x: outcome_to_binary(x["url"], url_train_median), axis=1)

test_set["auc_med_train"] = test_set.apply(lambda x: outcome_to_binary(x["auction"],auc_train_median), axis=1)
test_set["dev_med_train"] = test_set.apply(lambda x: outcome_to_binary(x["device"], dev_train_median), axis=1)
test_set["time_med_train"] = test_set.apply(lambda x: outcome_to_binary(x["time"], time_train_median), axis=1)
test_set["country_med_train"] = test_set.apply(lambda x: outcome_to_binary(x["country"], country_train_median), axis=1)
test_set["ip_med_train"] = test_set.apply(lambda x: outcome_to_binary(x["ip"], ip_train_median), axis=1)
test_set["url_med_train"] = test_set.apply(lambda x: outcome_to_binary(x["url"], url_train_median), axis=1)

###Useful : corr() to select features
import plotly.express as px
corr = train_set.corr()
fig = px.imshow(corr)
fig.show()
