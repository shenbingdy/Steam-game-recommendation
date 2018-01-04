import pandas as pd
import numpy as np 
import json
from sqlalchemy import*


# # Recommendation by ALS

# load the appid id and data
appid_use_list_path='C:/Users/shenbingdy/Desktop/datalab/game/my git/data/appid_use_list.txt'
user_inventory_adress='C:/Users/shenbingdy/Desktop/datalab/game/my git/data/steam_user_id_summary.txt'
with open (appid_use_list_path, 'r') as f:
    appid_use_list_temp=f.readlines()
    appid_use_list=[]
    for i in range(len(appid_use_list_temp)):
        appid_use_list+=[appid_use_list_temp[i].strip()] 


from pyspark.mllib.recommendation import ALS
from pyspark import SparkContext
sc=SparkContext.getOrCreate()

# set the fuction for data transfering
def load_string(string):
    S=json.loads(string)
    return list(S.items())[0]
inventory_rdd=sc.textFile(user_inventory_adress).map(load_string).zipWithIndex()
print(inventory_rdd.take(1))

def user_list(x):
    ((user_id,inventory),index)=x
    return (index,user_id)

user_id_full_list=inventory_rdd.map(user_list).collectAsMap()#collectAsMap() change it to dict
user_id_full_list[5]

def F_Tuple (x):
    ((user_id,inventory),index)=x
    if inventory!=None:
        temp=[]
        for i in inventory:
            #if str(i.get('appid')) in appid_use_list:
            temp+=[(i.get('appid'),1)]
        return (index, temp)
    else:
        return (index,[])
   
# change the data to rdd 
train_rdd_temp=inventory_rdd.map(F_Tuple).flatMapValues(lambda x:x)
print(train_rdd_temp.take(10))

def F_Flat (x):
    (index,(appid, ValuE))=x
    return (index,appid, ValuE)

train_rdd=train_rdd_temp.map(F_Flat)
print(train_rdd.take(10))


# Build a ALS model and train the data
model=ALS.train(train_rdd,5)
recom_dict={}
for index in list(user_id_full_list.keys()):
    try:
        recom_list=[i.product for i in model.recommendProducts(index,10)] 
        user_id=user_id_full_list.get(index)
        recom_dict.update({user_id:recom_list})
    except:
           pass   


# change it to a sql table
df_recom=pd.DataFrame.from_dict(recom_dict,'index')
df_recom.index.name='stem_user_id'
df_recom.reset_index(inplace=True)
engine=create_engine('mysql+pymysql://root:innovation@127.0.0.1/game_re?charset=utf8mb4')
ALS_recom=df_recom.to_sql('ALS_reco',engine,if_exists='replace',index=False)

