import plotly
import pandas as pd
import plotly.express as px

MetsResults = pd.read_csv("mets_2019_results.csv")

#Make new column for run differential based on R (runs) and RA (runs against)
MetsResults['RDiff'] = MetsResults.R - MetsResults.RA

#Consolidate all Ws and Ls into one type of W and L for the W/L column
for n in range(0,len(MetsResults)):
    if MetsResults['W/L'][n] == 'L-wo':
        MetsResults['W/L'] = MetsResults['W/L'].replace(MetsResults['W/L'][n], 'L')
    if MetsResults['W/L'][n] == 'W-wo':
        MetsResults['W/L'] = MetsResults['W/L'].replace(MetsResults['W/L'][n], 'W')

fig = px.scatter_polar(MetsResults, r="RDiff", theta="Opp",
                   color="W/L",
                   color_discrete_sequence= px.colors.qualitative.D3,
                   title='Mets 2019 Wins and Losses with Run Differential', labels={"RDiff": "Run Differential", "Opp": "Opponent"})
fig.update_traces(marker=dict(size=8,
                              line=dict(width=1,
                                        color='DarkSlateGrey')),
                  selector=dict(mode='markers'))
fig.show()
