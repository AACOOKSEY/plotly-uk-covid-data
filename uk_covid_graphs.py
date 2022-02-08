import requests

from plotly.subplots import make_subplots
import plotly.graph_objects as go
from plotly import offline

#Make an API call and store the response.
url = 'https://api.coronavirus.data.gov.uk/v1/data'
headers = {'Accept': 'application/vnd.PHE-COVID19.v1+json'}
r = requests.get(url, headers=headers)
print(f"Status code: {r.status_code}")

#Process the results, storing the required data.
response_dict = r.json()
repo_dicts = response_dict['data']
date, daily_cases, total_cases = [], [], []
daily_deaths, total_deaths = [], []
for repo_dict in repo_dicts:
    date.append(repo_dict['date'])
    daily_cases.append(repo_dict['latestBy'])
    total_cases.append(repo_dict['confirmed'])
    daily_deaths.append(repo_dict['deathNew'])
    total_deaths.append(repo_dict['death'])

#Set-up the subplots
fig = make_subplots(rows=2, cols=2, subplot_titles=(
    "Daily Cases", "Daily Deaths", "Total Cases", "Total Deaths"))

#Create each graph and assign to the correct subplot.
fig.add_trace(go.Scatter(
    x=date, y=daily_cases, name='Daily Cases', fill='tozeroy'),row=1, col=1)
fig.add_trace(go.Scatter(
    x=date, y=daily_deaths, name='Daily Deaths', fill='tozeroy'), row=1, col=2)
fig.add_trace(go.Scatter(
    x=date, y=total_cases, name='Total Cases', fill='tozeroy'), row=2, col=1)
fig.add_trace(go.Scatter(
    x=date, y=total_deaths, name='Total Deaths', fill='tozeroy'), row=2, col=2)

#Update labels and titles.
fig.update_yaxes(title_text="People")
fig.update_xaxes(title_text="Date")
fig.update_layout(title_text=f"UK COVID Data ({date[-1]} - {date[0]})", hovermode="x")

#Configure the range slider and selector.
range_selector = xaxis=dict(rangeselector=dict(buttons=list([
                dict(count=1, label="1m", step="month", stepmode="backward"),
                dict(count=6, label="6m", step="month", stepmode="backward"),
                dict(count=1, label="YTD", step="year", stepmode="todate"),
                dict(count=1, label="1y", step="year", stepmode="backward"),
                dict(step="all"),])))

#Apply the range selector to each subplot.
fig.update_layout(xaxis1=dict(range_selector),)
fig.update_layout(xaxis2=dict(range_selector),)
fig.update_layout(xaxis3=dict(range_selector),)
fig.update_layout(xaxis4=dict(range_selector),)

#Resize the rangeslider.
fig.update_xaxes(rangeslider_thickness = 0.05)

offline.plot(fig, filename='uk_covid_graphs.html')