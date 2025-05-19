import csv
import os

INFLUENCERS_CSV = os.path.join(os.path.dirname(__file__), 'influencers.csv')

import pandas as pd

def load_influencer_usernames(csv_path='checker/influencers.csv'):
    df = pd.read_csv(csv_path)
    usernames = set(df['Username'].dropna().str.lower().str.strip())
    return usernames

