import requests

BEARER_TOKEN = ''

HEADERS = {
    'Authorization': f'Bearer {BEARER_TOKEN}'
}

def get_user_data(username):
    url = f'https://api.twitter.com/2/users/by/username/{username}?user.fields=created_at,public_metrics'
    response = requests.get(url, headers=HEADERS)

    if response.status_code == 200:
        data = response.json()['data']
        print(data)
        return {
            'id': data['id'],
            'username': data['username'],
            'created_at': data['created_at'],
            'followers_count': data['public_metrics']['followers_count'],
            'tweet_count': data['public_metrics']['tweet_count'],
        }
    else:
        return None


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
