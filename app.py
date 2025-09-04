import streamlit as st
import pandas as pd
from matplotlib.axes import Axes

import preprocessor,helper
from helper import medal_tally
from preprocessor import event_df, region_df
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff

# Call the preprocess function and assign the returned DataFrame to event_df
event_df = preprocessor.preprocess(event_df, region_df)

st.sidebar.title("Olympics Analysis")
st.sidebar.image('https://www.hatchwise.com/wp-content/uploads/2024/08/dopely-olympic7-1024x576-1.jpg')

# making drop menu
user_menu = st.sidebar.radio(
    'Select an option',('Medal Tally','Overall Analysis','Country wise Analysis','Athlete wise Analysis')
)
# To show the dataframe on streamlit
# st.dataframe(event_df)

if user_menu == 'Medal Tally':
    st.sidebar.header("Medal Tally")
    years,country = helper.country_year_list(event_df)

    selected_year = st.sidebar.selectbox("Select Year",years)
    selected_country = st.sidebar.selectbox("Select Country", country)

    medal_tally = helper.fetch_medal_tally(event_df,selected_year,selected_country)
    if selected_year == 'Overall' and selected_country == 'Overall':
        st.title("Overall Tally")
    if selected_year != 'Overall' and selected_country == 'Overall':
        st.title("Medal Tally in " + str(selected_year) + " Summer Olympics")
    if selected_year == 'Overall' and selected_country != 'Overall':
        st.title(selected_country + " overall performance")
    if selected_year != 'Overall' and selected_country != 'Overall':
        st.title(selected_country + " performance in " + str(selected_year) + " Summer Olympics")
    st.table(medal_tally)


if user_menu == 'Overall Analysis':
    st.sidebar.header("Overall Analysis")

    editions = event_df['Year'].unique().shape[0] - 1
    cities = event_df['City'].unique().shape[0]
    sports = event_df['Sport'].unique().shape[0]
    events = event_df['Event'].unique().shape[0]
    athletes = event_df['Name'].unique().shape[0]
    nations = event_df['region'].unique().shape[0]

    st.title("Top Statistics")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Editions")
        st.title(editions)
    with col2:
        st.header("Cities")
        st.title(cities)
    with col3:
        st.header("Sports")
        st.title(sports)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Events")
        st.title(events)
    with col2:
        st.header("Nations")
        st.title(nations)
    with col3:
        st.header("Athletes")
        st.title(athletes)

    nations_overtime = helper.data_over_time(event_df, 'region')
    fig = px.line(nations_overtime, x="Edition", y="region")
    st.title("Participating Nations over the years")
    st.plotly_chart(fig)

    events_over_time = helper.data_over_time(event_df, 'Event')
    fig = px.line(events_over_time, x="Edition", y="Event")
    st.title("Events over the years")
    st.plotly_chart(fig)

    athlete_over_time = helper.data_over_time(event_df, 'Name')
    fig = px.line(athlete_over_time, x="Edition", y="Name",labels={'Name': 'Number of Athletes'})
    st.title("Athletes over the years")
    st.plotly_chart(fig)

    st.title("No. of Events over time(Every Sport)")
    fig, ax = plt.subplots(figsize=(20, 20))
    x = event_df.drop_duplicates(['Year', 'Sport', 'Event'])
    ax = sns.heatmap(
        x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype('int'),annot=True)
    st.pyplot(fig)

    sport_list = event_df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')

    selected_sport = st.selectbox('Select a Sport', sport_list)
    st.title("Top Athletes in " + str(selected_sport))
    x = helper.top_20_successful_sport_wise(event_df, selected_sport)
    st.table(x)

if user_menu == 'Country wise Analysis':
    st.sidebar.title('Country-wise Analysis')

    country_list = event_df['region'].dropna().unique().tolist()
    country_list.sort()

    selected_country = st.sidebar.selectbox('Select a Country', country_list)

    country_df = helper.yearwise_medal_tally(event_df, selected_country)
    fig = px.line(country_df, x="Year", y="Medal")
    st.title(selected_country + " Medal Tally over the years")
    st.plotly_chart(fig)

    heat_map_df = helper.heat_map(event_df, selected_country)
    fig, ax = plt.subplots(figsize=(20, 20))
    ax = sns.heatmap(
        heat_map_df.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype('int'),
        annot=True)
    st.title(selected_country + " Medal Tally Heatmap")
    st.pyplot(fig)

    most_successful_athletes = helper.top_20_successful_country_wise(event_df, selected_country).reset_index(drop=True)
    st.title("Top Athletes of " + selected_country)
    st.table(most_successful_athletes)

if user_menu == 'Athlete wise Analysis':
    athlete_df = event_df.drop_duplicates(subset=['Name', 'region'])

    x1 = athlete_df['Age'].dropna()
    x2 = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna()
    x3 = athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna()
    x4 = athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna()

    fig = ff.create_distplot([x1, x2, x3, x4], ['Overall Age', 'Gold Medalist', 'Silver Medalist', 'Bronze Medalist'],show_hist=False, show_rug=False)
    fig.update_layout(autosize=False,width=1000,height=600)
    st.title("Distribution of Age")
    st.plotly_chart(fig)

    gold = []
    gold_name = []
    famous_sports = ['Basketball', 'Judo', 'Football', 'Tug-Of-War', 'Athletics',
                     'Swimming', 'Badminton', 'Sailing', 'Gymnastics',
                     'Art Competitions', 'Handball', 'Weightlifting', 'Wrestling',
                     'Water Polo', 'Hockey', 'Rowing', 'Fencing',
                     'Shooting', 'Boxing', 'Taekwondo', 'Cycling', 'Diving', 'Canoeing',
                     'Tennis', 'Golf', 'Softball', 'Archery',
                     'Volleyball', 'Synchronized Swimming', 'Table Tennis', 'Baseball',
                     'Rhythmic Gymnastics', 'Rugby Sevens',
                     'Beach Volleyball', 'Triathlon', 'Rugby', 'Polo', 'Ice Hockey']
    for sport in famous_sports:
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        gold.append(temp_df[temp_df['Medal'] == 'Gold']['Age'].dropna())
        gold_name.append(sport)

    silver = []
    silver_name = []

    for sport in famous_sports:
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        silver.append(temp_df[temp_df['Medal'] == 'Silver']['Age'].dropna())
        silver_name.append(sport)

    bronze = []
    bronze_name = []


    fig_gold= ff.create_distplot(gold, gold_name, show_hist=False, show_rug=False)
    fig_gold.update_layout(autosize=False, width=1000, height=600)
    st.title("Distribution of Age wrt Sports(Gold Medalist)")
    st.plotly_chart(fig_gold)

    fig_silver = ff.create_distplot(silver, silver_name, show_hist=False, show_rug=False)
    fig_silver.update_layout(autosize=False, width=1000, height=600)
    st.title("Distribution of Age wrt Sports(Silver Medalist)")
    st.plotly_chart(fig_silver)


    sport_list = event_df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')

    st.title('Height Vs Weight')
    selected_sport = st.selectbox('Select a Sport', sport_list)
    temp_df = helper.weight_v_height(event_df, selected_sport)
    x = temp_df['Weight']
    y = temp_df['Height']
    fig, ax = plt.subplots(figsize=(15, 8))
    ax = sns.scatterplot(x=x, y=y, hue=temp_df['Medal'], style=temp_df['Sex'], s=60)
    st.pyplot(fig)

    st.title("Men vs Women Participation")
    participation = helper.men_v_women(event_df)
    fig_gender = px.line(participation, x='Year', y=['Male','Female'])
    fig_gender.update_layout(autosize=False, width=1000, height=400)
    st.plotly_chart(fig_gender)