import pandas as pd
import matplotlib.pyplot as plt

pop = pd.read_csv('population.csv', index_col=0)
print(pop.head())

print(pop.isna().any())
print(pop.isna().sum())

# Dropping all rows that have no population value
pop_drop = pop.dropna(subset='population')
# Checking to see if there are any more missing values
print(pop_drop.isna().sum())

# Question 1 - How many countries had no recorded population data
#  (0) for the year 2000? List these countries along with their continent..
pop_0_2000 = (pop_drop['population']==0) & (pop_drop['year']==2000)
length = len(pop_drop[pop_0_2000][['country name','continent']])

print(f'The number of countries that have no recorded population data ' 
      f'for the year 2000 is: {length}')

# Question 2 - Calculate the total population for all African countries in 2010. 
# Create a bar chart showing the population distribution across African 
# countries in 2010.
africa_2010 = (pop_drop['continent'] == 'Africa') & (pop_drop['year'] == 2010)
africa_2010_total = pop_drop[africa_2010]['population'].sum()

print(f'The total population for all African countries in 2010 is ' 
      f'{africa_2010_total} million')

africa_2010_filt = pop_drop[africa_2010].sort_values('population')

plt.barh(africa_2010_filt['country name'], africa_2010_filt['population'])
plt.xlabel('Population (millions)')
plt.ylabel('Country')
plt.title('Population Distribution Across African Countries in 2010')
plt.grid(axis='x')
plt.show()

# Question 3 - Determine the average population of countries in South 
# America for the year 2000. Highlight countries with populations above
# and below this average. Include the lists in your analysis.

south_america = (pop_drop['continent']==
                 'South America') & (pop_drop['year']==2000)
avg_sa_2000 = pop_drop[south_america]['population'].mean()

print(f'The average population of countries in South America for '
      f'the year 2000 is {avg_sa_2000} million')

# Finding countries that are above and below the average. 
sa_filt = pop_drop[south_america]
print('The South American countries with populations above average are:')
print(sa_filt[sa_filt['population']>avg_sa_2000]['country name'])
print('The South American countries with populations below average are:')
print(sa_filt[sa_filt['population']<avg_sa_2000]['country name'])

# Question 4 - Identify the countries with populations exceeding 
# 1000 million in 2007. Create a bar chart or scatter plot to display 
# all countries' populations in 2007, marking those above 1000.#

pop_greater_2007 = (pop_drop['population']>1000) & (pop_drop['year']==2007)
print('The countries with populations exceeding 1000 million in 2007 '
      'are:')
print(pop_drop[pop_greater_2007]['country name'])

# Filtering countries in 2007 and soritng them by population 
# in descending order to make it easier to locate
pop_2007 = pop_drop[pop_drop['year']==2007].sort_values('population', 
                                                        ascending=False)
plt.scatter(range(len(pop_2007)), pop_2007['population'], alpha=0.5)
plt.text(0, pop_2007['population'].iloc[0], pop_2007['country name'].iloc[0])
plt.text(1, pop_2007['population'].iloc[1], pop_2007['country name'].iloc[1])

plt.title('Global Population of Countries in 2007')
plt.xlabel('Rank (Sorted by Size)')
plt.ylabel('Population (millions)')
plt.grid()
plt.show()

# Question 5 - Calculate the total population growth in Europe 
# between 2000 and 2010. Identify the top 5 European countries by 
# population growth during this period and create a line plot showing 
# the population changes of these countries from 2000 to 2010.
europe_2000 = (pop_drop['continent']=='Europe') & (pop_drop['year']==2000)
total_pop_europe_2000 = pop_drop[europe_2000]['population'].sum()

europe_2010 = (pop_drop['continent']=='Europe') & (pop_drop['year']==2010)
total_pop_europe_2010 = pop_drop[europe_2010]['population'].sum()
difference = total_pop_europe_2010 - total_pop_europe_2000

print(f'The total population growth in Europe between 2000 and 2010 is '
      f'{difference} million')

# Identifying the top 5 countries
pop_drop_europe = pop_drop[pop_drop['continent']=='Europe']
pivot_europe = pop_drop_europe.pivot_table(
    index='country name',
    columns='year',
    values='population',
)

pivot_europe['Growth_2000_2010'] = pivot_europe[2010] - pivot_europe[2000]
top5 = pivot_europe.sort_values('Growth_2000_2010', ascending=False).head()
print('The top 5 European Countries in terms of population growth '
      'between 2000 and 2010 are:')
print(top5[[2000, 2010, 'Growth_2000_2010']])

# Filtering for the line graph
europe = pop_drop[pop_drop['continent'] == 'Europe']
europe_totals = europe.groupby('year')['population'].sum()

europe_totals.plot(kind='line')
plt.title('Population growth of Europe from 2000 to 2010')
plt.xlabel('Year')
plt.ylabel('Population (millions)')
plt.grid()
plt.show()