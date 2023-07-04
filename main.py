import pandas as pd 
import seaborn as sns
import numpy as np
# plotting data 
import matplotlib.pyplot as plt
import plotly.express as px
from plotly.subplots import make_subplots
from datetime import datetime

covid19_df = pd.read_csv('/Users/playo/Desktop/data-analysis/covid/covid_19_india.csv')
covid19_df.drop(["Sno", 'Time', 'ConfirmedIndianNational', 'ConfirmedForeignNational'],inplace = True, axis = 1)
# change format of date 
covid19_df['Date'] = pd.to_datetime(covid19_df['Date'])
# covid19_df["month"] = covid19_df["Date"].dt.month

# current cases
covid19_df['Active Cases'] = covid19_df['Confirmed'] - (covid19_df['Cured']+ covid19_df['Deaths'])
# create new table
bystate = pd.pivot_table(covid19_df, index = 'State/UnionTerritory',values = ['Deaths','Cured', 'Confirmed'],aggfunc = max)
bystate['Survival Rate'] = (bystate['Cured'] / bystate['Confirmed']) * 100
bystate['Mortality Rate'] = (bystate['Deaths'] / bystate['Confirmed']) * 100
bystate = bystate.sort_values(by='Survival Rate',ascending=False)

# Top 10 effected states
top_ten_active = covid19_df.groupby(by = 'State/UnionTerritory').max()[['Active Cases', 'Date']].sort_values(by =['Active Cases'], ascending = False).reset_index()

figure = plt.figure(figsize = (20,10))
plt.title("Top 10 Most Affected State/Union Territories", size = 20)

sns.barplot(data = top_ten_active.iloc[:10], x = "State/UnionTerritory", y = "Active Cases", color = 'steelblue', edgecolor = 'blue')

# Trends for 5 highest States
figure1 = plt.figure(figsize = (20,10))
graph = sns.lineplot(data = covid19_df[covid19_df['State/UnionTerritory'].isin(['Maharashtra', 'Kerala', 'Tamil Nadu','Karnataka','Uttar Pradesh'])], x = "Date", y = "Active Cases", hue = "State/UnionTerritory")
graph.set_title('Trends for COVID Cases in Top 5 Affected States', size = 20)

# vaccine data set 
vaccine_df = pd.read_csv('/Users/playo/Desktop/data-analysis/covid/covid_vaccine_statewise.csv')
vaccine_df.rename(columns = {'Updated On': 'Vaccine Date'}) 
vaccine_df.isnull().sum()
# drop missing columns 
vaccine_dropped = vaccine_df.drop(['Sputnik V (Doses Administered)', 'AEFI', '18-44 Years (Doses Administered)','45-60 Years (Doses Administered)','60+ Years (Doses Administered)'], axis = 1)
# plot for male vs female vaccination
male = vaccine_dropped['Male(Individuals Vaccinated)'].sum()
female = vaccine_dropped['Female(Individuals Vaccinated)'].sum()
df = px.data.tips()
fig = px.pie(names=['Male','Female'], values = [male,female], title = 'Pie Chart for Population Vaccines', color_discrete_sequence=px.colors.sequential.RdBu)
fig.show()

# drop rows that have India as a state
vaccine = vaccine_df[vaccine_df.State != 'India']
vaccine.rename(columns = {"Total Individuals Vaccinated": "Total"}, inplace = True)
# state with most people vaccinated
max_vaccination = vaccine.groupby('State')['Total'].sum().to_frame('Total')
max_vaccination = max_vaccination.sort_values('Total', ascending = False)[:5]
max_vaccination
fig = plt.figure(figsize = (20,10))
plt.title("Top 5 vaccinated states in India", size = 20)
x = sns.barplot(data = max_vaccination.iloc[:5], y = max_vaccination.Total,x = max_vaccination.index,color = 'steelblue', edgecolor = 'blue')
plt.xlabel("States")
plt.ylabel("Vaccination")
plt.show()
