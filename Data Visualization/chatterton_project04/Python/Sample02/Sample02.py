import plotly
import pandas as pd
import plotly.express as px

GiantsData = pd.read_csv("Giants_attendance.csv")

#Update the Stadium Data to reference one park per building instead of each new name the park had
for n in range(0,len(GiantsData)):
    if 'Polo' in GiantsData.Stadium[n]:
        GiantsData.Stadium = GiantsData.Stadium.replace(GiantsData.Stadium[n], 'Polo Grounds')
    if GiantsData.Stadium[n] == '3Com Park':
        GiantsData.Stadium = GiantsData.Stadium.replace(GiantsData.Stadium[n], 'CandleStick Park')
    if (GiantsData.Stadium[n] == 'Pacific Bell Park' or GiantsData.Stadium[n] == 'SBC Park' or GiantsData.Stadium[n] == 'AT&T Park'):
        GiantsData.Stadium = GiantsData.Stadium.replace(GiantsData.Stadium[n], 'Oracle Park')

fig = px.line(GiantsData, x="Year", y="Attendance", title='Giants Attendance Year by Year at each Stadium')
fig.add_scattergl(x=GiantsData.Year, y=GiantsData.Attendance.where(GiantsData.Stadium == 'Polo Grounds'), line={'color': 'orange'}, name='Polo Grounds')
fig.add_scattergl(x=GiantsData.Year, y=GiantsData.Attendance.where(GiantsData.Stadium == "Seals Stadium"), line={'color': 'blue'}, name='Seals Stadium')
fig.add_scattergl(x=GiantsData.Year, y=GiantsData.Attendance.where(GiantsData.Stadium == "Candlestick Park"), line={'color': 'red'}, name='Candlestick Park')
fig.add_scattergl(x=GiantsData.Year, y=GiantsData.Attendance.where(GiantsData.Stadium == "Oracle Park"), line={'color': 'black'}, name='Oracle Park')
fig.update_xaxes(dtick=5)
fig.show()
