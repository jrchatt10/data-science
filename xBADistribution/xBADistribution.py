import numpy as np
import random
import matplotlib.pyplot as plt
import pandas as pd
import requests
import io
import datetime
import pybaseball

def get_player_batted_balls(playerFirst, playerLast, dateGT, dateLT):
    
    results = []
    #all batted balls for a single player
    url='https://baseballsavant.mlb.com/statcast_search/csv?all=true&hfPT=&hfAB=single%7Cdouble%7Ctriple%7Chome%5C.%5C.run%7Cfield%5C.%5C.out%7Cdouble%5C.%5C.play%7Cfield%5C.%5C.error%7Cgrounded%5C.%5C.into%5C.%5C.double%5C.%5C.play%7Cfielders%5C.%5C.choice%7Cfielders%5C.%5C.choice%5C.%5C.out%7Cforce%5C.%5C.out%7Csac%5C.%5C.bunt%7Csac%5C.%5C.bunt%5C.%5C.double%5C.%5C.play%7Csac%5C.%5C.fly%7Csac%5C.%5C.fly%5C.%5C.double%5C.%5C.play%7Ctriple%5C.%5C.play%7C&hfBBT=&hfPR=&hfZ=&stadium=&hfBBL=&hfNewZones=&hfGT=R%7C&hfC=&hfSea=&hfSit=&player_type=batter&hfOuts=&opponent=&pitcher_throws=&batter_stands=&hfSA=&game_date_gt={}&game_date_lt={}&hfInfield=&team=&position=&hfOutfield=&hfRO=&home_road=&batters_lookup%5B%5D={}&hfFlag=&hfPull=&metric_1=&hfInn=&min_pitches=0&min_results=0&group_by=name-event&sort_col=pitches&player_event_sort=h_launch_speed&sort_order=desc&min_pas=0&type=details&'
    
    #convert playername into Savant PlayerID for search
    playerIDtable = pybaseball.playerid_lookup(playerLast,playerFirst)
    player = playerIDtable.loc[0].key_mlbam

    #convert year, month, and day into individual integers
    monthGT = int(dateGT[5:7])
    monthLT = int(dateLT[5:7])
    yearGT = int(dateGT[0:4])
    yearLT = int(dateLT[0:4])
    dayGT = int(dateGT[8:10])
    dayLT = int(dateLT[8:10])
    
    #if spanning more than a month get needed days of first month, then months in between, then needed days of last month
    if monthLT > monthGT:
        dateGT = datetime.date(yearGT,monthGT,dayGT)
        dateGT = dateGT.strftime("%Y-%m-%d")
        dateLT = datetime.date(yearGT,monthGT+1,1) - datetime.timedelta(days=1)
        dateLT = dateLT.strftime("%Y-%m-%d")
        data = requests.get(url.format(dateGT, dateLT, player)).content
        df = pd.read_csv(io.StringIO(data.decode('utf-8')))
        results.append(df)
        if ((monthLT - monthGT) > 1):
            for month in range((monthGT+1),monthLT):
                dateGT = datetime.date(yearGT,month,1)
                dateGT = dateGT.strftime("%Y-%m-%d")
                dateLT = datetime.date(yearGT,month+1,1) - datetime.timedelta(days=1)
                dateLT = dateLT.strftime("%Y-%m-%d")
                data = requests.get(url.format(dateGT, dateLT, player)).content
                df = pd.read_csv(io.StringIO(data.decode('utf-8')))
                results.append(df)
        dateGT = datetime.date(yearGT,monthLT,1)
        dateGT = dateGT.strftime("%Y-%m-%d")
        dateLT = datetime.date(yearGT,monthLT,dayLT)
        dateLT = dateLT.strftime("%Y-%m-%d")
        data = requests.get(url.format(dateGT, dateLT, player)).content
        df = pd.read_csv(io.StringIO(data.decode('utf-8')))
        results.append(df)
        
    #if months equal just grab the days needed
    if monthLT == monthGT:
        dateGT = datetime.date(yearGT,monthGT,dayGT)
        dateGT = dateGT.strftime("%Y-%m-%d")
        dateLT = datetime.date(yearGT,monthLT,dayLT)
        dateLT = dateLT.strftime("%Y-%m-%d")
        data = requests.get(url.format(dateGT, dateLT, player)).content
        df = pd.read_csv(io.StringIO(data.decode('utf-8')))
        results.append(df)
    
    return pd.concat(results)

print("Enter player's first name: ")
firstName = input()
print("Enter player's last name: ")
lastName = input()
print("Enter Start Date (YYYY-MM-DD): ")
fromDate = input()
print("Enter End Date (YYYY-MM-DD): ")
toDate = input()
playerBattedBalls = get_player_batted_balls(firstName, lastName, fromDate, toDate)
playerBattedBalls = playerBattedBalls.reset_index(drop=True)
xBA = playerBattedBalls["estimated_ba_using_speedangle"]

playerIDtable = pybaseball.playerid_lookup(lastName,firstName)
player = playerIDtable.loc[0].key_mlbam

playerBattedBallsMore = pybaseball.statcast_batter(fromDate, toDate, player)

BAlist = []
for x in range(100000):
    hit = 0
    for i in range(0, len(xBA)):
        rand = random.uniform(0, 1)
        if rand < xBA[i]:
            hit = hit + 1
    BA = hit/((len(xBA)+len(playerBattedBallsMore.events[playerBattedBallsMore.events == 'strikeout'])))
    BAlist.append(BA)

hits = len(playerBattedBallsMore.events[playerBattedBallsMore.events == 'single']) + len(playerBattedBallsMore.events[playerBattedBallsMore.events == 'double']) + len(playerBattedBallsMore.events[playerBattedBallsMore.events == 'triple']) + len(playerBattedBallsMore.events[playerBattedBallsMore.events == 'home_run'])
avg = hits/(len(playerBattedBallsMore.events[playerBattedBallsMore.events.notnull()]) - (len(playerBattedBallsMore.events[playerBattedBallsMore.events == 'walk']) + len(playerBattedBallsMore.events[playerBattedBallsMore.events == 'sac_bunt']) + len(playerBattedBallsMore.events[playerBattedBallsMore.events == 'sac_bunt_double_play'])+len(playerBattedBallsMore.events[playerBattedBallsMore.events == 'sac_fly']) + len(playerBattedBallsMore.events[playerBattedBallsMore.events == 'sac_bunt_double_play']) + len(playerBattedBallsMore.events[playerBattedBallsMore.events == 'hit_by_pitch']) + len(playerBattedBallsMore.events[playerBattedBallsMore.events == 'intentional_walk'])))

figure = plt.figure(figsize=(20, 6))

axes = figure.add_subplot(1, 1, 1)
axes.hist(BAlist, color="DimGray", bins=20, weights=(np.ones(len(BAlist)) / len(BAlist)))
axes.set_xlabel("BAlist")
axes.set_ylabel("Percentage")
axes.set_title("Histogram of BA based on xBA")
plt.axvline(sum(BAlist)/len(BAlist), color='k', linestyle='dashed', linewidth=4)
plt.axvline(avg, color='red', linestyle='dashed', linewidth=4)
plt.text(.1, .95, 'Actual BA: {:.3f}'.format(avg), ha='center', va='center', fontsize = 15, color='red', transform=axes.transAxes)
plt.text(.1, .88, 'xBA: {:.3f}'.format(sum(BAlist)/len(BAlist)), ha='center', va='center', fontsize = 15, transform=axes.transAxes)

plt.show()
plt.close()

