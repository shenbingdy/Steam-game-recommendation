
import requests,sys,time
import pandas as pd
import numpy as np 
import json
import nltk
from nltk.corpus import stopwords


# show work_status function
def F_work(step,current,total):
    current+=step
    Per=int(current/total*100)
    status='>'*Per+' '*(100-Per)
    if Per<=100:
        sys.stdout.write('\r[{0}] {1:.2f}%'.format(status,Per))
        #sys.stdout.write('\r[{0}] {1:.2f}% '.format(status, percentage))
        sys.stdout.flush()
    else:
        print('\n')
		
  
# Get the most popular games for new user
#   import the appid 
appid_detail_txt_url='C:/Users/shenbingdy/Desktop/datalab/game/my git/data/appid_dict.txt'
with open (appid_detail_txt_url,'r') as f:
     appid_detail=f.read()
appid_dict=json.loads(appid_detail)
appid_list=list(appid_dict.keys())


# get all the game app
dict_popular={}
for appid in appid_list:
    dict_p={}
    if appid_dict.get(appid).get('owners'):
        dict_p.update({'owners':appid_dict.get(appid).get('owners')})
    else:
        dict_p.update({'owners':None})
    if appid_dict.get(appid).get('players_2weeks'):
        dict_p.update({'players_2weeks':appid_dict.get(appid).get('players_2weeks')})
    else:
        dict_p.update({'players_2weeks':None})
    if appid_dict.get(appid).get('tags'):
        dict_p.update({'tags':appid_dict.get(appid).get('tags').keys()})
    else:
        dict_p.update({'tags':None})   
    dict_popular.update({appid:dict_p})


df_popular=pd.DataFrame.from_dict(dict_popular,'index')
df_popular['appid']=df_popular.index


# get the most popular game app
df_Top10_appid=df_popular.sort_values('owners',ascending=False)[:10][['appid','owners']]
# get the most popular game app in recent 2 weeks
df_Top10_appid_2weeks=df_popular.sort_values('players_2weeks',ascending=False)[:10][['appid','owners']]
#mergee the results 
df_top_10=df_Top10_appid_2weeks[:5]
i=0
j=0
while i<5:
    if df_Top10_appid['appid'][j] in df_top_10['appid'][:]: 
        j+=1
    else:          
        df_top_10=df_top_10.append(df_Top10_appid[j:j+1])
        j+=1
        i+=1
		
# change to sql table
from sqlalchemy import *
engine = create_engine('mysql+pymysql://root:innovation@127.0.0.1/game_re?charset=utf8mb4') #how to buil
#game_re need to be build in my sql software
df_top_10.to_sql('top_10_popular',engine,if_exists='replace',index=False)


# # recommendations by game content 
# get the game content
#   get the game information
appid_detail_txt_url='C:/Users/shenbingdy/Desktop/datalab/game/my git/data/appid_detail.txt'
with open (appid_detail_txt_url,'r') as f:
     appid_detail=f.readlines()

appid_detail_dict={}
for i in range(len(appid_detail)):
    appid_detail_dict.update(json.loads(appid_detail[i]))
appid_list=list(appid_detail_dict.keys())

#   save game information into a dataFrame
appid_list=list(appid_detail_dict.keys())
detail_appid_dict={}
for appid in appid_list:
    detail_dict={}
    if appid_detail_dict.get(appid).get('success'):
        detail_dict.update({'type':appid_detail_dict.get(appid).get('data').get('type')})
        detail_dict.update({'name':appid_detail_dict.get(appid).get('data').get('name')})
        detail_dict.update({'required_age':appid_detail_dict.get(appid).get('data').get('required_age')})
        detail_dict.update({'is_free':appid_detail_dict.get(appid).get('data').get('is_free')})
        detail_dict.update({'detailed_description':appid_detail_dict.get(appid).get('data').get('detailed_description')})
        detail_dict.update({'about_the_game':appid_detail_dict.get(appid).get('data').get('about_the_game')})
        detail_dict.update({'short_description':appid_detail_dict.get(appid).get('data').get('short_description')})
        detail_dict.update({'supported_languages':appid_detail_dict.get(appid).get('data').get('supported_languages')})
        detail_dict.update({'reviews':appid_detail_dict.get(appid).get('data').get('reviews')})
        detail_dict.update({'developers':appid_detail_dict.get(appid).get('data').get('developers')})
        detail_dict.update({'linux':appid_detail_dict.get(appid).get('data').get('platforms').get('linux')})
        detail_dict.update({'mac':appid_detail_dict.get(appid).get('data').get('platforms').get('mac')})
        detail_dict.update({'windows':appid_detail_dict.get(appid).get('data').get('platforms').get('windows')})
        
        if appid_detail_dict.get(appid).get('data').get('metacritic'):
            detail_dict.update({'score':appid_detail_dict.get(appid).get('data').get('metacritic').get('score')})
        else:
            detail_dict.update({'score':None})
        if appid_detail_dict.get(appid).get('data').get('controller_support'):
            detail_dict.update({'controller_support':appid_detail_dict.get(appid).get('data').get('controller_support')})
        else:
            detail_dict.update({'controller_support':None})  
            
        if appid_detail_dict.get(appid).get('data').get('price_overview'):
            detail_dict.update({'currency':appid_detail_dict.get(appid).get('data').get('price_overview').get('currency')})
            detail_dict.update({'intial_price':appid_detail_dict.get(appid).get('data').get('price_overview').get('initial')/100})
            detail_dict.update({'final_price':appid_detail_dict.get(appid).get('data').get('price_overview').get('final')/100})
            detail_dict.update({'discount_percent':appid_detail_dict.get(appid).get('data').get('price_overview').get('discount_percent')})
        else:
            detail_dict.update({'currency':None})
            detail_dict.update({'intial_price':None})
            detail_dict.update({'final_price':None})
            detail_dict.update({'discount_percent':None})
            
        if appid_detail_dict.get(appid).get('data').get('recommendations'):
            detail_dict.update({'recommendations_total':appid_detail_dict.get(appid).get('data').get('recommendations').get('total')})
        else:
            detail_dict.update({'recommendations_total':None})
        if appid_detail_dict.get(appid).get('data').get('pc_requirements'):
            detail_dict.update({'PC_minimum':appid_detail_dict.get(appid).get('data').get('pc_requirements').get('minimum')})  
            detail_dict.update({'PC_recommended':appid_detail_dict.get(appid).get('data').get('pc_requirements').get('recommended')})  
        else:  
            detail_dict.update({'PC_minimum':None})
            detail_dict.update({'PC_recommended':None})
            
        if appid_detail_dict.get(appid).get('data').get('mac_requirements'):
            detail_dict.update({'mac_minimum':appid_detail_dict.get(appid).get('data').get('mac_requirements').get('minimum')})  
            detail_dict.update({'mac_recommended':appid_detail_dict.get(appid).get('data').get('mac_requirements').get('recommended')})  
        else:  
            detail_dict.update({'mac_minimum':None})
            detail_dict.update({'mac_recommended':None})
            
        if appid_detail_dict.get(appid).get('data').get('linux_requirements'):
            detail_dict.update({'linux_minimum':appid_detail_dict.get(appid).get('data').get('linux_requirements').get('minimum')})  
            detail_dict.update({'linux_recommended':appid_detail_dict.get(appid).get('data').get('linux_requirements').get('recommended')})  
        else:  
            detail_dict.update({'linux_minimum':None})
            detail_dict.update({'linux_recommended':None})
                                                    
        detail_dict.update({'date':appid_detail_dict.get(appid).get('data').get('release_date').get('date')})
        detail_appid_dict.update({appid:detail_dict})


df_detail_appid=pd.DataFrame.from_dict(detail_appid_dict,'index')
df_detail_appid.drop(df_detail_appid[df_detail_appid['is_free']].index, inplace=True)
appid_use_list=df_detail_appid.index


# save the appid_use_list
appid_use_list_path='C:/Users/shenbingdy/Desktop/datalab/game/my git/data/appid_use_list.txt'
with open (appid_use_list_path, 'w') as f:
     f.writelines(['%s\n' %i for i in appid_use_list])



#analyze the game contect
from nltk.tokenize import word_tokenize
from nltk.tokenize import WordPunctTokenizer
from nltk.stem.snowball import GermanStemmer
from bs4 import BeautifulSoup


#preparing the data for nltk analysis
def pre_process_cn(inputs, low_freq_filter):  
    # get rid of the thml tag
    soup = BeautifulSoup(inputs,'lxml')
    text=soup.get_text()
    # seperate words
    from nltk.tokenize import WordPunctTokenizer
    text_words = WordPunctTokenizer().tokenize(text)
    #get rid of stopwords
    english_stopwords = stopwords.words('english')
    texts_filtered_stopwords = [word for word in text_words if not word in english_stopwords] 
    #get rid of punctuations
    english_punctuations =  [',','-','"','.', '/',':', ';', '?', '(', ')', '[', ']', "'",'&', '!', '*', '@', '#', '$', '%','\x97']
    texts_filtered = [word for word in texts_filtered_stopwords if not word in english_punctuations]
    #stem
    from nltk.stem.lancaster import LancasterStemmer
    st = LancasterStemmer()
    texts_stemmed = [st.stem(word) for word in texts_filtered] 
     
    #get rid of low frenquency words
    if low_freq_filter:
        stems_once = set(stem for stem in set(texts_stemmed) if texts_stemmed.count(stem) == 1)
        texts = [stem for stem in texts_stemmed if stem not in stems_once] 
    else:
        texts = texts_stemmed
    return texts
texts_all=[pre_process_cn(i, low_freq_filter=True) for i in df_detail_appid['about_the_game']]


# analyze the content and similarities of the games 
from gensim import corpora, models, similarities


# built the model to analyze the content
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
dictionary = corpora.Dictionary(texts_all)
corpus = [dictionary.doc2bow(text) for text in texts_all]
tfidf = models.TfidfModel(corpus)
corpus_tfidf = tfidf[corpus]
lsi = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=10)
index = similarities.MatrixSimilarity(lsi[corpus])


# analyze the similarities of the games
F_work(0,0,len(appid_use_list))
current=0
total=len(appid_use_list)
tfidf_about_the_game_dict={}
for i in range(total):
    tfidf_game=[]
    ml_game = texts_all[i]
    ml_bow = dictionary.doc2bow(ml_game)
    ml_tfidf = tfidf[ml_bow]
    ml_lsi = lsi[ml_tfidf]
    sims = index[ml_lsi]
    sort_sims = sorted(enumerate(sims), key=lambda item: -item[1])[1:100]
    for (j,k) in sort_sims:# j is the index of appid
        tfidf_game+=[appid_use_list[j]] #
    tfidf_about_the_game_dict.update({appid_use_list[i]:tfidf_game})
    F_work(1,current,total)  
    current+=1


# transfer it to sql table
df_tfidf_about_the_game=pd.DataFrame.from_dict(tfidf_about_the_game_dict,'index')
df_tfidf_about_the_game.index.name='appid'
df_tfidf_about_the_game.reset_index(inplace=True)
df_tfidf_about_the_game.to_sql('content_recom', engine, if_exists='replace')


# # # # recommendations by user 

#import user's data
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn import metrics
user_inventory_adress='C:/Users/shenbingdy/Desktop/datalab/game/my git/data/steam_user_id_summary.txt'
user_inventory_dict={}
with open (user_inventory_adress,'r') as f:
     user_inventory_str=f.readlines()                         
for i in range(len(user_inventory_str)):
    user_id,user_inventory=list(json.loads(user_inventory_str[i]).items())[0]
    
    if user_inventory!=None:
        user_inventory_dict[user_id]={} #  
        for playtime_dict in user_inventory:
            user_appid=str(playtime_dict.get('appid'))
            user_play=playtime_dict.get('playtime_forever')
            if (user_appid in appid_use_list) and (user_play>0):
                user_inventory_dict[user_id].update({user_appid:1})  
df_user_appid=pd.DataFrame.from_dict(user_inventory_dict,'index').fillna(0)





#analyze the similarities of the user
current=0
total=df_user_appid.shape[0]
F_work(0,0,total)
dict_recom={}
for i in range(total):
    realtion=np.argsort(-metrics.pairwise.cosine_similarity(df_user_appid[i:i+1],df_user_appid).flatten())[1:101]
    Rec_id=[]
    for j in realtion:
        Rec_id+=[df_user_appid.index[j]]
    dict_recom.update({str(df_user_appid.index[i]):Rec_id})
    F_work(1,current,total)
    current+=1
# transfer it to sql table
df_user_recom=pd.DataFrame.from_dict(dict_recom,'index')
df_user_recom.index.name='user_id'
df_user_recom.reset_index(inplace=True)
df_user_recom.to_sql('user_recom_userbased',engine, if_exists='replace')

# the item based 
df_appid_user=pd.DataFrame.from_dict(user_inventory_dict,'columns').fillna(0)
current=0
total=df_appid_user.shape[0]
F_work(0,0,total)
dict_app_recom={}
for i in range(total):
    realtion=np.argsort(-metrics.pairwise.cosine_similarity(df_appid_user[i:i+1],df_appid_user).flatten())[1:101]
    item_recom=[]
    for j in realtion:
        item_recom+=[str(df_appid_user.index[j])]
    dict_app_recom.update({str(df_appid_user.index[i]):item_recom})
    F_work(1,current,total)
    current+=1
df_app_recom=pd.DataFrame.from_dict(dict_app_recom,'index')
df_app_recom.columns=['g'+str(x)for x in df_app_recom.columns]
df_app_recom.index.name='steam_id'
df_app_recom.reset_index(inplace=True)
df_app_recom.to_sql('items_recom_itemsbased',engine, if_exists='replace')
