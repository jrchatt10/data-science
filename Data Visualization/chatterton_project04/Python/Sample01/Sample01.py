import plotly
import pandas as pd
import plotly.express as px

teamData = pd.read_csv("Team_attendance.csv")
fig = px.scatter(teamData, x="Est. Payroll", y="Attendance", color="#A-S", color_continuous_scale=px.colors.sequential.Emrld, title='Team Payroll and Influence on Attendance and All Stars over last 4 Years', labels={"#A-S": "All Stars"})
fig.update_traces(marker=dict(size=12,
                              line=dict(width=2,
                                        color='DarkSlateGrey')),
                  selector=dict(mode='markers'))
fig.show()
