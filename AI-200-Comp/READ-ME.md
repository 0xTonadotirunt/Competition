**Project Description:**

In this competition, you'll be chasing down robots for an online auction site. Human bidders on
the site are increasingly frustrated with their inability to win auctions vs. their softwarecontrolled counterparts. As a result, usage from the site's core customer base is plummeting.
To rebuild customer happiness, the site owners need to eliminate computer generated bidding
from their auctions. Their attempt at building a model to identify these bids using behavioral
data, including bid frequency over short periods of time, has proven insufficient.

The goal of this competition is to identify online auction bids that are placed by "robots", helping
the site owners easily flag these users for removal from their site to prevent unfair auction
activity.

**Features :** 

train.csv
-----------------------------------------
bidder_id - unique identifier of a bidder
payment_account - payment account associated with bidder ( obfuscated )
address - mailing address ( obfuscated )
outcome - label whether it is a bot, 1 - bot, 0 - human

bids.csv
-----------------------------------------
bid_id - unique id for this bid
bidder_id - unique identifier of a bidder ( same as bidder_id in train.csv and test.csv ) 
auction - unique identifier of auction
merchandise - category of the auction site , could be a search term, or online advert
device - phone model of visitor
time - time that bid is made ( transformed )
country - the country that the ip belongs to
ip - IP address of bidder ( obfuscated )
url - url where the bidder was referred from ( obfuscated ).


**Kaggle competition link**: 
https://www.kaggle.com/c/ai200-dec-2021-human-or-bot/leaderboard

Teamname : JJZR
-----------------
AUC score
Public : 0.89533
Private : 0.88597

Original Kaggle Competition
-----------------------------
Facebook Recruitment IV: Human or Robot?
https://www.kaggle.com/c/facebook-recruiting-iv-human-or-bot
AUC score
Public : 0.89402
Private : 0.91125
