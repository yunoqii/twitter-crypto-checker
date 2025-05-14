import csv
import os

INFLUENCERS_CSV = os.path.join(os.path.dirname(__file__), 'influencers.csv')

def load_influencer_usernames():
    usernames = set()
    with open(INFLUENCERS_CSV, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            username = row.get("Username")
            if username:
                usernames.add(username.lower())
    return usernames
