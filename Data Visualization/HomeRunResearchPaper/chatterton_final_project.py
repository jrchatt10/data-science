import time
import matplotlib.pyplot as plt
import pandas as pd
import requests
import io
import datetime
import re
import plotly.express as px
import plotly.graph_objects as go

#This is a function to pull down the data sets from Baseball Savant
def get_batted_ball_data(year):
    
    results = []
    #the search is just for line drive and fly ball batted balls - doesn't include grounders or pop ups
    #BBT=fly%5C.%5C.ball%7Cline%5C.%5C.drive
    url='https://baseballsavant.mlb.com/statcast_search/csv?all=true&hfPT=&hfAB=single%7Cdouble%7Ctriple%7Chome%5C.%5C.run%7Cfield%5C.%5C.out%7Cdouble%5C.%5C.play%7Cfield%5C.%5C.error%7Cgrounded%5C.%5C.into%5C.%5C.double%5C.%5C.play%7Cfielders%5C.%5C.choice%7Cfielders%5C.%5C.choice%5C.%5C.out%7Ctriple%5C.%5C.play%7C&hfBBT=fly%5C.%5C.ball%7Cline%5C.%5C.drive%7C&hfPR=&hfZ=&stadium=&hfBBL=&hfNewZones=&hfGT=R%7C&hfC=&hfSea={}%7C&hfSit=&player_type=batter&hfOuts=&opponent=&pitcher_throws=&batter_stands=&hfSA=&game_date_gt={}&game_date_lt={}&hfInfield=&team=&position=&hfOutfield=&hfRO=&home_road=&hfFlag=&hfPull=&metric_1=&hfInn=&min_pitches=0&min_results=0&group_by=name-event&sort_col=pitches&player_event_sort=h_launch_speed&sort_order=desc&min_pas=0&type=details&'
    
    for month in range(3,11):
        dateGT = datetime.date(year,month,1)
        dateGT = dateGT.strftime("%Y-%m-%d")
        dateLT = datetime.date(year,month+1,1) - datetime.timedelta(days=1)
        dateLT = dateLT.strftime("%Y-%m-%d")
        data = requests.get(url.format(year, dateGT, dateLT)).content
        df = pd.read_csv(io.StringIO(data.decode('utf-8')))
        results.append(df)
    
    return pd.concat(results)

#Run the function above for each of the five available seasons
BattedBall2019 = get_batted_ball_data(2019)
BattedBall2018 = get_batted_ball_data(2018)
BattedBall2017 = get_batted_ball_data(2017)
BattedBall2016 = get_batted_ball_data(2016)
BattedBall2015 = get_batted_ball_data(2015)

#Trim the data to just include home run events
homers2019 = BattedBall2019.loc[BattedBall2019['events'] == 'home_run']
homers2018 = BattedBall2018.loc[BattedBall2018['events'] == 'home_run']
homers2017 = BattedBall2017.loc[BattedBall2017['events'] == 'home_run']
homers2016 = BattedBall2016.loc[BattedBall2016['events'] == 'home_run']
homers2015 = BattedBall2015.loc[BattedBall2015['events'] == 'home_run']

#Trim the data further to not include null data for hit distance and any home runs less than 300 feet
homers2015 = homers2015.loc[homers2015['hit_distance_sc'].notnull()]
homers2015 = homers2015.loc[homers2015['hit_distance_sc'] >= 300]
homers2016 = homers2016.loc[homers2016['hit_distance_sc'].notnull()]
homers2016 = homers2016.loc[homers2016['hit_distance_sc'] >= 300]
homers2017 = homers2017.loc[homers2017['hit_distance_sc'].notnull()]
homers2017 = homers2017.loc[homers2017['hit_distance_sc'] >= 300]
homers2018 = homers2018.loc[homers2018['hit_distance_sc'].notnull()]
homers2018 = homers2018.loc[homers2018['hit_distance_sc'] >= 300]
homers2019 = homers2019.loc[homers2019['hit_distance_sc'].notnull()]
homers2019 = homers2019.loc[homers2019['hit_distance_sc'] >= 300]

#Add a column for season for each dataset
homers2019['Season'] = '2019'
homers2018['Season'] = '2018'
homers2017['Season'] = '2017'
homers2016['Season'] = '2016'
homers2015['Season'] = '2015'

#Create a dataset with all seasons concatenated together
seasons = [homers2019, homers2018, homers2017, homers2016, homers2015]
homers = pd.concat(seasons)

#Create the histogram for home run distances
fig = go.Figure()
fig.add_trace(go.Histogram(x=homers2019['hit_distance_sc'], name='2019'))
fig.add_trace(go.Histogram(x=homers2018['hit_distance_sc'], name='2018'))
fig.add_trace(go.Histogram(x=homers2017['hit_distance_sc'], name='2017'))
fig.add_trace(go.Histogram(x=homers2016['hit_distance_sc'], name='2016'))
fig.add_trace(go.Histogram(x=homers2015['hit_distance_sc'], name='2015'))

# Overlay both histograms
fig.update_layout(barmode='overlay', title_text='Count of Home Run Distances per Season',
    xaxis_title_text='Estimated Distance',
    yaxis_title_text='Home Run Count')
# Reduce opacity to see both histograms
fig.update_traces(opacity=0.4)
fig.show()

#Create the scatterplot
fig = px.scatter(homers, x="launch_speed", y="launch_angle", color="Season", 
                 title='Exit Velocity and Launch Angle for every Home Run by Season',
                 labels={"launch_angle": "Launch Angle", "launch_speed": "Exit Velocity"}
                )
fig.update_traces(marker=dict(size=7,
                              opacity=.5),
                  selector=dict(mode='markers'))
fig.show()

#Create the datasets for each bucket of launch speeds and exit velocities
homersBucket1 = homers.loc[(homers['launch_speed'] >= 95) & (homers['launch_speed'] < 100) & (homers['launch_angle'] >= 20) & (homers['launch_angle'] < 25)]
homersBucket2 = homers.loc[(homers['launch_speed'] >= 100) & (homers['launch_speed'] < 105) & (homers['launch_angle'] >= 20) & (homers['launch_angle'] < 25)]
homersBucket3 = homers.loc[(homers['launch_speed'] >= 105) & (homers['launch_speed'] < 110) & (homers['launch_angle'] >= 20) & (homers['launch_angle'] < 25)]
homersBucket4 = homers.loc[(homers['launch_speed'] >= 110) & (homers['launch_speed'] < 115) & (homers['launch_angle'] >= 20) & (homers['launch_angle'] < 25)]
homersBucket5 = homers.loc[(homers['launch_speed'] >= 95) & (homers['launch_speed'] < 100) & (homers['launch_angle'] >= 25) & (homers['launch_angle'] < 30)]
homersBucket6 = homers.loc[(homers['launch_speed'] >= 100) & (homers['launch_speed'] < 105) & (homers['launch_angle'] >= 25) & (homers['launch_angle'] < 30)]
homersBucket7 = homers.loc[(homers['launch_speed'] >= 105) & (homers['launch_speed'] < 110) & (homers['launch_angle'] >= 25) & (homers['launch_angle'] < 30)]
homersBucket8 = homers.loc[(homers['launch_speed'] >= 110) & (homers['launch_speed'] < 115) & (homers['launch_angle'] >= 25) & (homers['launch_angle'] < 30)]
homersBucket9 = homers.loc[(homers['launch_speed'] >= 95) & (homers['launch_speed'] < 100) & (homers['launch_angle'] >= 30) & (homers['launch_angle'] < 35)]
homersBucket10 = homers.loc[(homers['launch_speed'] >= 100) & (homers['launch_speed'] < 105) & (homers['launch_angle'] >= 30) & (homers['launch_angle'] < 35)]
homersBucket11 = homers.loc[(homers['launch_speed'] >= 105) & (homers['launch_speed'] < 110) & (homers['launch_angle'] >= 30) & (homers['launch_angle'] < 35)]
homersBucket12 = homers.loc[(homers['launch_speed'] >= 95) & (homers['launch_speed'] < 100) & (homers['launch_angle'] >= 35) & (homers['launch_angle'] < 40)]
homersBucket13 = homers.loc[(homers['launch_speed'] >= 100) & (homers['launch_speed'] < 105) & (homers['launch_angle'] >= 35) & (homers['launch_angle'] < 40)]
homersBucket14 = homers.loc[(homers['launch_speed'] >= 105) & (homers['launch_speed'] < 110) & (homers['launch_angle'] >= 35) & (homers['launch_angle'] < 40)]

#Create the violin and box plots for the above datasets
fig = px.violin(homersBucket1, x="Season", y="hit_distance_sc", box=True,
                 title='Distance for Home Runs with 95-100 MPH Exit Velocity and 20-25 Degree Launch Angle',
                labels={"hit_distance_sc": "Estimated Home Run Distance"}
                )

fig.show()

fig = px.violin(homersBucket2, x="Season", y="hit_distance_sc", box=True,
                 title='Distance for Home Runs with 100-105 MPH Exit Velocity and 20-25 Degree Launch Angle',
                labels={"hit_distance_sc": "Estimated Home Run Distance"}
                )

fig.show()

fig = px.violin(homersBucket3, x="Season", y="hit_distance_sc", box=True,
                 title='Distance for Home Runs with 105-110 MPH Exit Velocity and 20-25 Degree Launch Angle',
                labels={"hit_distance_sc": "Estimated Home Run Distance"}
                )

fig.show()

fig = px.violin(homersBucket1, x="Season", y="hit_distance_sc", box=True,
                 title='Distance for Home Runs with 110-115 MPH Exit Velocity and 20-25 Degree Launch Angle',
                labels={"hit_distance_sc": "Estimated Home Run Distance"}
                )

fig.show()

fig = px.violin(homersBucket5, x="Season", y="hit_distance_sc", box=True,
                 title='Distance for Home Runs with 95-100 MPH Exit Velocity and 25-30 Degree Launch Angle',
                labels={"hit_distance_sc": "Estimated Home Run Distance"}
                )

fig.show()

fig = px.violin(homersBucket6, x="Season", y="hit_distance_sc", box=True,
                 title='Distance for Home Runs with 100-105 MPH Exit Velocity and 25-30 Degree Launch Angle',
                labels={"hit_distance_sc": "Estimated Home Run Distance"}
                )

fig.show()

fig = px.violin(homersBucket7, x="Season", y="hit_distance_sc", box=True,
                 title='Distance for Home Runs with 105-110 MPH Exit Velocity and 25-30 Degree Launch Angle',
                labels={"hit_distance_sc": "Estimated Home Run Distance"}
                )

fig.show()

fig = px.violin(homersBucket8, x="Season", y="hit_distance_sc", box=True,
                 title='Distance for Home Runs with 110-115 MPH Exit Velocity and 25-30 Degree Launch Angle',
                labels={"hit_distance_sc": "Estimated Home Run Distance"}
                )

fig.show()

fig = px.violin(homersBucket9, x="Season", y="hit_distance_sc", box=True,
                 title='Distance for Home Runs with 95-100 MPH Exit Velocity and 30-35 Degree Launch Angle',
                labels={"hit_distance_sc": "Estimated Home Run Distance"}
                )

fig.show()

fig = px.violin(homersBucket10, x="Season", y="hit_distance_sc", box=True,
                 title='Distance for Home Runs with 100-105 MPH Exit Velocity and 30-35 Degree Launch Angle',
                labels={"hit_distance_sc": "Estimated Home Run Distance"}
                )

fig.show()

fig = px.violin(homersBucket11, x="Season", y="hit_distance_sc", box=True,
                 title='Distance for Home Runs with 105-110 MPH Exit Velocity and 30-35 Degree Launch Angle',
                labels={"hit_distance_sc": "Estimated Home Run Distance"}
                )

fig.show()

fig = px.violin(homersBucket12, x="Season", y="hit_distance_sc", box=True,
                 title='Distance for Home Runs with 95-100 MPH Exit Velocity and 35-40 Degree Launch Angle',
                labels={"hit_distance_sc": "Estimated Home Run Distance"}
                )

fig.show()

fig = px.violin(homersBucket13, x="Season", y="hit_distance_sc", box=True,
                 title='Distance for Home Runs with 100-105 MPH Exit Velocity and 35-40 Degree Launch Angle',
                labels={"hit_distance_sc": "Estimated Home Run Distance"}
                )

fig.show()

fig = px.violin(homersBucket14, x="Season", y="hit_distance_sc", box=True,
                 title='Distance for Home Runs with 105-110 MPH Exit Velocity and 35-40 Degree Launch Angle',
                labels={"hit_distance_sc": "Estimated Home Run Distance"}
                )

fig.show()
