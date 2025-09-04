import pandas as pd

event_df = pd.read_csv('athlete_events.csv')
region_df = pd.read_csv('noc_regions.csv')

def preprocess(event_df, region_df):
    ## filtering summer season
    event_df = event_df[event_df['Season'] == 'Summer']
    ## merge with region_df
    event_df = event_df.merge(region_df, on='NOC', how='left')
    ## dropping duplicates
    event_df.drop_duplicates(inplace=True)

    # Drop existing 'Gold', 'Silver', and 'Bronze' columns if they exist
    event_df = event_df.drop(['Gold', 'Silver', 'Bronze'], axis=1, errors='ignore')

    ## one hot encoding
    ohe_medal = pd.get_dummies(event_df['Medal'], dtype=int)
    event_df = pd.concat([event_df, ohe_medal], axis=1)

    return event_df