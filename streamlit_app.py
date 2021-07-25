#packages
from urllib.request import urlretrieve
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import streamlit as st

#default congif for charts
import matplotlib
sns.set_style('darkgrid')
matplotlib.rcParams['font.size'] = 14
matplotlib.rcParams['figure.figsize'] = (12, 8)
matplotlib.rcParams['figure.facecolor'] = '#00000000'

#title
st.title('COVID-19 Data Analysis 🔬')
st.subheader("Covid-19 makes huge impact in our daily lives, there was't be a person in the world without saying the name 'COVID'. Chick [this link](https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv) to access the daily updating covid details dataset of the world. ")

#import data
data_url = 'https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv'
urlretrieve(data_url, 'covid_data.csv')
raw_df = pd.read_csv('covid_data.csv')

#text
st.header('Analysis on : **_How India affected by this virus_**')

#extract india data
raw_df[raw_df['location'] == 'India']
india_df = inr_df = raw_df[raw_df['location'] == 'India']


#get useful columns
india_df = inr_df[['date',
                'new_cases',
                'new_deaths',
                'new_tests',
                'total_cases',
                'total_deaths',
                'total_tests']]

#q1 chart
st.header('**_Q1. Timeline for the total_case and total_death_**')
if st.checkbox('View total_case Graph', value=False):
	fig1 = px.line(india_df,
        x = india_df.date,
        y = 'total_cases',
        title = 'Timeline of total cases')
	st.plotly_chart(fig1)

if st.checkbox('View total_deaths Graph', value=False):
	fig2 = px.line(india_df,
        x = india_df.date,
        y = 'total_deaths',
        title = 'Timeline of total deaths')
	st.plotly_chart(fig2)

#q2 chart
st.header('**_Q2 : First case of corona in India_**')
first_case = india_df.date.loc[india_df['new_cases'].ne(0).idxmax()]
st.write('The first case of corona virus in India was reported on', first_case)

#q3 chart
st.header('**_Q3 : What was the total case at the time of impliminting the first lockdown in India 25 Mar 2020 _**')
lockdown = '2020-03-25'
lockdown_case = india_df.total_cases.loc[india_df.loc[india_df.date == lockdown].index[0]]
st.write('The total number of case at the time of first lockdown',lockdown,' was ',int(lockdown_case))

#q4 chart
st.header('**_Q4 : What was the total death at the time of impliminting the first lockdown in India 25 Mar 2020 _**')
first_death = india_df.date.loc[india_df.new_deaths.ne(0).idxmax()]
st.write('The first death of the covid was caused in',first_death)

#q5 chart
st.header('**_Q5 : How did the new_cases and new_deaths evolved in india?_**')

if st.checkbox("Plotly Curve",value=False):
	fig3 = px.line(india_df, 
       		 x = 'date',
       		 y = 'new_cases')
	fig3.add_scatter(x = india_df['date'],
                 y = india_df['new_deaths'],
		 name= 'deaths')
	st.plotly_chart(fig3)
st.write('* At the middle month of april 2020 the cases starts increaisng slightly and reaches 2000 	cases. During this period the government starts relaxing some facilities during the lockdown. That 	might leads to the high cases.') 
st.write('* We can clearly see that, the case numbers are completely zero at the month of january, its 	because of the staffs may in leave/government holiday.')
st.write('* The best thing that india did, they predict the third wave at the edge time before when it 	was started. which means the government announse that there will the 3rd wave within a month at feb-	10. After that the cases were starts increasing and reach the peak at the month of may.')
st.write('* Now the cases were starts decreasing and death rate is still in the alerting stage.')

#q6 chart
st.header('**_Q6 : On which date the highest covid case was reported?_**')
st.write('Lets create a dataframe to plot the graph, by taking 350k cases as the threshold point')
high_case_df = india_df[india_df.new_cases > 350000]
high_case_df.sort_values('new_cases',ascending = False)
if st.checkbox("View high case date graph",value=False):	
	fig4 = plt.figure(figsize=(25,10))
	sns.barplot(high_case_df.date, high_case_df.new_cases)
	plt.title('High cases by the date')
	st.pyplot(fig4)
	st.write('On the day 2021-05-06 was recorded the high case', int(india_df.new_cases.max()))

#q7 chart 
st.header('**_Q7 : On which date the highest covid deaths was reported?_**')
high_death_df = india_df[india_df.new_deaths > 500].sort_values('new_cases',ascending=False)
if st.checkbox('View high death date graph',value=False):
	fig5 = plt.figure(figsize=(25,10))
	sns.barplot(high_death_df.date.head(10), high_death_df.new_deaths.head(10))
	plt.title('High deaths by day')
	st.pyplot(fig5)
st.write('On the day 2021-05-07 was recorded the high case', int(india_df.new_deaths.max()))

#q8 chart
st.header('**_Q8 : How many positive cases were reported on india per month in 2021?_**')
#split date year month
india_df['day'] = pd.DatetimeIndex(india_df.date).day
india_df['month'] = pd.DatetimeIndex(india_df.date).month
india_df['year'] = pd.DatetimeIndex(india_df.date).year

#grab the 2021 year details
year_21 = india_df.loc[india_df.year == 2021]
cases_per_month = year_21.groupby('month')[['new_cases','new_deaths','total_cases','total_deaths','total_tests']].sum()

if st.checkbox('View cases per month Graph',value=False):
	fig6 = plt.figure()
	sns.barplot(cases_per_month.index, cases_per_month.new_cases)
	plt.title('Positive cases per month in the year of 2021')
	st.pyplot(fig6)

st.write('On the month of `march 2021` high positive cases', int(cases_per_month.new_cases.max()) ,'were reported ')

#q9 chart
st.header('**_Q9 : How many deaths were reported on india per month in 2021?_**')
if st.checkbox('View deaths per month Graph',value=False):
	fig7 = plt.figure()
	sns.barplot(cases_per_month.index, cases_per_month.new_deaths)
	plt.title('Deaths per month in the year of 2021')
	st.pyplot(fig7)
st.write('On the month of `march 2021` high deaths', int(cases_per_month.new_deaths.max()),'were reported in india')

#q10 chart
st.header('**_Q10 : How many positive cases were reported on india per month in 2020?_**')
year_20 = india_df.loc[india_df.year == 2020]
cases_per_month_20 = year_20.groupby('month')[['new_cases','new_deaths','total_cases','total_deaths','total_tests']].sum()
if st.checkbox('View cases graph', value=False):
	fig8 = plt.figure()
	sns.barplot(cases_per_month_20.index, cases_per_month_20.new_cases)
	plt.title('Positive cases per month in the year of 2020')
	st.pyplot(fig8)
st.write('There were',int(cases_per_month_20.new_cases.max()),'cases reported in india on 2020')

#q11 chart
st.header('**_Q11 : How many deaths were reported on india per month in 2020?_**')
year_20 = india_df.loc[india_df.year == 2020]
cases_per_month_20 = year_20.groupby('month')[['new_cases','new_deaths','total_cases','total_deaths','total_tests']].sum()
if st.checkbox('View deaths graph', value=False):
	fig9=plt.figure()
	sns.barplot(cases_per_month_20.index, cases_per_month_20.new_deaths)
	plt.title('Deaths per month in the year of 2020')
	st.pyplot(fig9)
st.write('There were',int(cases_per_month_20.new_deaths.max()),'deaths reported in india on 2020')

st.write('The below code will be executed soon')
'''
#q12 chart
st.header('**_Q12 : How many tests were taken in india on 2020 and 2021?_**')
st.write('Let s make a subplot in plotly to display the resuts')
if st.checkbox('View subplot', value=True):
	#plotly 'go' add more plot on a sinlge graph chart
	#make_subplots use to make a grid 
	from plotly.subplots import make_subplots
	import plotly.graph_objects as go

	#set the rows and cols of the grid to be displayed
	fig = make_subplots(rows=1, cols=2, subplot_titles=('2021 Covid Tests', '2020 Covid Tests'))

	fig.append_trace(go.Bar(
	   x = cases_per_month_20.index,
	   y = cases_per_month_20.total_tests),
	    row=1 ,col=2)

	fig.append_trace(go.Bar(
	    x = cases_per_month.index,
	    y = cases_per_month.total_tests
	),  row=1, col=1)

	#update_layout used to config the graph display items
	fig.update_xaxes(title_text='Months', row=1, col=1)
	fig.update_xaxes(title_text='Months', row=1, col=2)
	fig.update_layout(showlegend=False, title='Number of tests taken in 2020 and 2021')
		
	st.plotly_chart(graph)'''
