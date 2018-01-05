
import requests,sys,time
import pandas as pd
import numpy as np 
import json

## show work status fuction 

def F_status (step, total, current=0):
    current+=step
    Percentage= int((current/total)*100)
    status='>'*Percentage+' '*(100-Percentage)
    if Percentage < 100:
        sys.stdout.write('\rStatus: [{0}] {1:.2f}% '.format(status, Percentage))
        sys.stdout.flush()
    else:
        print ('\n')


# We have the 5000 user_id and plan to get user_id inofrmation and game information 
#    get user_inventoty from steampy power
#    get api information https://developer.valvesoftware.com/wiki/Steam_Web_API#GetGlobalAchievementPercentagesForApp_.28v0001.29
#    IsPlayingSharedGame (v0001)
#    IsPlayingSharedGame returns the original owner's SteamID if a borrowing account is currently playing this game. If the game is not borrowed or the borrower currently doesn't play this game, the result is always 0.
#    Example URL: http://api.steampowered.com/IPlayerService/IsPlayingSharedGame/v0001/?key=XXXXXXXXXXXXXXXXX&steamid=76561197960434622&appid_playing=240&format=json

#load the 5000 user_id
user_id_path= 'C:/Users/shenbingdy/Desktop/datalab/game/my git/data/steam_user_id.txt'
with open (user_id_path, 'r') as f:
     steam_user_id_lst=f.readlines()[::2]###
len(steam_user_id_lst)


#get user_inventoty from steam by api
current=0
total=len( steam_user_id_lst)
F_status(0,total,current)
initial_time=time.time()
user_inventory={}
for steam_user_id in steam_user_id_lst:
    steam_user_id_url='http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/'
    param={'key':'4850408CACE43F02FCFB811A67B4DAAF',
              'steamid':steam_user_id.strip(),
              'format':'json'}
    for i in range(3):
            try:
                r=requests.get(steam_user_id_url, param)
                break
            except:
                    time.sleep(.5)
                    pass
    steam_user_game=r.json().get('response').get('games')
    user_inventory.update({steam_user_id.strip():steam_user_game})
    F_status(1,total,current)
    current+=1
    if current%200==0:
        time.sleep(300)
final_time=time.time()
print('The total second is :',-initial_time+final_time)       
# Save the data in to a txt file:
user_inventory_adress='C:/Users/shenbingdy/Desktop/datalab/game/my git/data/steam_user_id_summary.txt'
with open (user_inventory_adress, 'w') as f:
     for steam_user_id,steam_user_game in user_inventory.items():
            f.write(json.dumps({steam_user_id:steam_user_game})) 
            f.write('\n')


			
##get user_inventoty from steam by api recent 2 weeks
current=0
total=len( steam_user_id_lst)
F_status(0,total,current)
initial_time=time.time()
user_inventory_recent={}
for steam_user_id in steam_user_id_lst:
    steam_user_id_url='http://api.steampowered.com/IPlayerService/GetRecentlyPlayedGames/v0001/'
    param={'key':'4850408CACE43F02FCFB811A67B4DAAF',
              'steamid':steam_user_id.strip(),
              'format':'json'}
    for i in range(3):
            try:
                r=requests.get(steam_user_id_url, param)
                break
            except:
                    time.sleep(.5)
                    pass
    steam_user_game=r.json().get('response').get('games')
    user_inventory_recent.update({steam_user_id.strip():steam_user_game})
    F_status(1,total,current)
    current+=1
    if current%200==0:
        time.sleep(280)
final_time=time.time()
print('The total second is :',-initial_time+final_time)
# Save the data in to a txt file:
user_inventory_recent_adress='C:/Users/shenbingdy/Desktop/datalab/game/my git/data/steam_user_id_recent_summary.txt'
with open (user_inventory_recent_adress, 'w') as f:
     for steam_user_id,steam_user_game in user_inventory.items():
            f.write(json.dumps({steam_user_id:steam_user_game})) 
            f.write('\n')





#By using the third part software get the ranking of game 

#get all the game app_id and save to a file
appid_url='http://steamspy.com/api.php?request=all'
appid_dict=requests.get(appid_url).json()
appid_list=list(appid_dict.keys())
appid_list_url='C:/Users/shenbingdy/Desktop/datalab/game/my git/data/appid_list.txt'
appid_dict_url='C:/Users/shenbingdy/Desktop/datalab/game/my git/data/appid_dict.txt'
with open (appid_list_url, 'w') as f:
    for i in range(len(appid_list)):
        f.write(appid_list[i])
        f.write('\n')
with open (appid_dict_url, 'w') as f:
    f.write(json.dumps(appid_dict))


#get all the game information and save them to a file
appid_url='http://steamspy.com/api.php?request=all'
appid_dict=requests.get(appid_url).json()

appid_detail_dict={}
appid_detail_txt_url='C:/Users/shenbingdy/Desktop/datalab/game/my git/data/appid_detail1.txt'
current=0
total=len(appid_list)
F_status(0,total,current)
initial_time=time.time()
with open (appid_detail_txt_url,'w') as f:
    for appid in appid_list:
        appid_detial_url=('http://store.steampowered.com/api/appdetails?appids=%s')%(appid)
        for i in range(3):
            try:
                r=requests.get(appid_detial_url).json()
                break
            except:
                    time.sleep(0.5)
                    pass
        appid_detail_dict.update(r)
        f.write(json.dumps(r))
        f.write('\n')
        F_status(1,total,current)
        current+=1
        if current%200==0:
            time.sleep(300)
print('The total second is ', (time.time()-initial_time))

