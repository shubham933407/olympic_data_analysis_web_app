import numpy as np

def medal_tally(event_df):
    medal_tally = event_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Medal', 'Sport', 'Event'])

    medal_tally = medal_tally.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold',ascending=False).reset_index()

    medal_tally['total'] = medal_tally['Gold'] + medal_tally['Silver'] + medal_tally['Bronze']
    return medal_tally

def country_year_list(event_df):
    years = event_df['Year'].unique().tolist()
    years.sort()
    years.insert(0, 'Overall')

    country = np.unique(event_df['region'].dropna().values).tolist()
    country.sort()
    country.insert(0, 'Overall')

    return years, country

def fetch_medal_tally(df,year,country):
  medal_df = df.drop_duplicates(subset=['Team','NOC','Games','Year','City','Medal','Sport','Event'])
  flag = 0
  if year == 'Overall' and country == 'Overall':
    temp_df = medal_df
  if year == 'Overall' and country != 'Overall':
    flag = 1
    temp_df = medal_df[medal_df['region'] == country]
  if year != 'Overall' and country == 'Overall':
    temp_df = medal_df[medal_df['Year'] == int(year)]
  if year != 'Overall' and country != 'Overall':
    temp_df = medal_df[(medal_df['Year'] == int(year)) & (medal_df['region'] == country)]

  if flag == 1:
    x = temp_df.groupby('Year').sum()[['Gold','Silver','Bronze']].sort_values('Year').reset_index()
  else:
    x = temp_df.groupby('region').sum()[['Gold','Silver','Bronze']].sort_values('Gold',ascending = False).reset_index()
  x['total'] = x['Gold'] + x['Silver'] + x['Bronze']

  return x

def data_over_time(event_df,col):

    x = event_df.drop_duplicates(['Year', col])['Year'].value_counts().reset_index().sort_values(
        'Year')
    x.rename(columns={'Year': 'Edition', 'count': col}, inplace=True)
    return x

def top_20_successful_sport_wise(df,sport):
  temp_df = df.dropna(subset=['Medal'])
  if sport != 'Overall':
    temp_df = temp_df[temp_df['Sport'] == sport]

  # Rename columns after reset_index to 'Name' and 'count'
  athlete_medal_counts = temp_df['Name'].value_counts().reset_index()
  x = athlete_medal_counts.head(20).merge(temp_df,left_on='Name',right_on='Name',how='left').drop_duplicates('Name')
  return x[['Name','count','region']].reset_index()

def yearwise_medal_tally(df,country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)

    new_df = temp_df[temp_df['region'] == country]
    new_df = new_df.groupby('Year').count()['Medal'].reset_index()

    return new_df

def heat_map(event_df,country):
  x = event_df[event_df['region'] == country].drop_duplicates(['Year', 'Sport', 'Event'])
  x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype('int')
  return x


def top_20_successful_country_wise(df, country):
    temp_df = df.dropna(subset=['Medal'])

    temp_df = temp_df[temp_df['region'] == country]

    # Rename columns after reset_index to 'Name' and 'count'
    athlete_medal_counts = temp_df['Name'].value_counts().reset_index()
    x = athlete_medal_counts.head(20).merge(temp_df, left_on='Name', right_on='Name', how='left').drop_duplicates('Name')
    return x[['Name', 'count']]

def weight_v_height(df,sport):
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])
    athlete_df['Medal'].fillna('No Medal', inplace=True)
    if sport != 'Overall':
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        return temp_df
    else:
        return athlete_df

def men_v_women(df):
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])
    male = athlete_df[athlete_df['Sex'] == 'M'].groupby('Year').count()['Name'].reset_index()
    female = athlete_df[athlete_df['Sex'] == 'F'].groupby('Year').count()['Name'].reset_index()

    final = male.merge(female, on='Year', how='left')
    final.fillna(0, inplace=True)
    final.rename(columns={'Name_x': 'Male', 'Name_y': 'Female'}, inplace=True)
    return final