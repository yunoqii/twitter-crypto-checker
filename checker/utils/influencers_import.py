import csv
from checker.models import Influencer, InfluencerFollow
from checker.twitter_api import get_user_id, get_following

def import_influencers_and_follows_from_csv(csv_path):
    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            username = row['Username'].lower()
            influencer, _ = Influencer.objects.get_or_create(
                username=username,
                defaults={'name': row.get('Name', '')}
            )

            user_id = get_user_id(username)
            if not user_id:
                print(f"[WARN] No user ID for {username}")
                continue

            following = get_following(user_id)
            if not following:
                print(f"[WARN] No following for {username}")
                continue

            for followed in following:
                InfluencerFollow.objects.get_or_create(
                    influencer=influencer,
                    followed_username=followed.lower()
                )
