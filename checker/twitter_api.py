import requests
import time
import os

BEARER_TOKEN = os.getenv('BEARER_TOKEN')

HEADERS = {
    'Authorization': f'Bearer {BEARER_TOKEN}'
}


def get_user_data(username):
    headers = {
        'Authorization': f'Bearer {BEARER_TOKEN}',
    }
    url = f"https://api.twitter.com/2/users/by/username/{username}"
    params = {
        'user.fields': 'profile_image_url,public_metrics,created_at'
    }
    response = requests.get(url, headers=headers, params=params)
    if response.status_code != 200:
        return None

    user_info = response.json().get('data', {})
    return {
        'id': user_info.get('id'),
        'username': user_info.get('username'),
        'followers_count': user_info.get('public_metrics', {}).get('followers_count', 0),
        'tweet_count': user_info.get('public_metrics', {}).get('tweet_count', 0),
        'created_at': user_info.get('created_at'),
        'profile_image_url': user_info.get('profile_image_url'),
    }



def get_followers_usernames(user_id, max_results=1000):
    followers = set()
    url = f'https://api.twitter.com/2/users/{user_id}/followers'
    params = {
        'max_results': 1000,
        'user.fields': 'username'
    }
    response = requests.get(url, headers=HEADERS, params=params)
    if response.status_code == 200:
        data = response.json()
        print(data)
        for user in data.get("data", []):
            followers.add(user['username'].lower())
    return followers


def get_recent_tweets(user_id, count=10):
    url = f'https://api.twitter.com/2/users/{user_id}/tweets'
    params = {
        'max_results': count,
        'tweet.fields': 'text'
    }
    response = requests.get(url, headers=HEADERS, params=params)

    if response.status_code == 200:
        tweets = response.json().get('data', [])
        return [tweet['text'] for tweet in tweets]
    return []


def get_user_id(username):
    url = f"https://api.twitter.com/2/users/by/username/{username}"
    headers = {"Authorization": f"Bearer {BEARER_TOKEN}"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()['data']['id']
    print(response.status_code)
    return None

def get_following(user_id):
    url = f"https://api.twitter.com/2/users/{user_id}/following"
    headers = {"Authorization": f"Bearer {BEARER_TOKEN}"}
    params = {"max_results": 1000, "user.fields": "username"}

    following = []
    next_token = None

    while True:
        if next_token:
            params["pagination_token"] = next_token

        response = requests.get(url, headers=headers, params=params)
        if response.status_code != 200:
            print(f"[ERROR] {response.status_code} — {response.text}")
            break

        data = response.json()
        following += [user['username'].lower() for user in data.get("data", [])]

        if "next_token" in data.get("meta", {}):
            next_token = data["meta"]["next_token"]
        else:
            break

    return following

def is_user_following(source_id, target_id):
    url = f'https://api.twitter.com/2/users/{source_id}/following'
    params = {'max_results': 1000}
    while True:
        response = requests.get(url, headers=HEADERS, params=params)
        if response.status_code != 200:
            return False
        data = response.json()
        if 'data' in data:
            if any(user['id'] == target_id for user in data['data']):
                return True
        if 'meta' in data and 'next_token' in data['meta']:
            params['pagination_token'] = data['meta']['next_token']
            time.sleep(1)
        else:
            break
    return False