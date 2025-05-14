import openai
import re

openai.api_key = ''

def is_ai_generated(tweet_text):
    prompt = f"Is that text similar to a tweet AI generated? just answer 'yes' or 'no'.\n\nTweet: \"{tweet_text}\""
    response = openai.ChatCompletion.create(
        model='gpt-4',
        messages=[
            {"role": "system", "content": "You're an expert of analizing AI generated text."},
            {"role": "user", "content": prompt}
        ]
    )
    answer = response['choices'][0]['message']['content'].strip().lower()
    return 'Yes' in answer

def check_ai_usage(tweets):
    ai_count = sum(1 for tweet in tweets if is_ai_generated(tweet))
    if len(tweets) == 0:
        return False
    return ai_count / len(tweets) >= 0.5

def generate_ai_summary(username, user_data, ai_used, influencers_count):
    prompt = f"""
Analize a twitter account @{username} and make a short summary in 2-3 sentences.

Data of account:
- Registration date: {user_data['created_at'][:10]}
- Followers: {user_data['followers_count']}
- Tweets: {user_data['tweet_count']}
- If AI used: {'Yes' if ai_used else 'No'}
- Influencers subscribed: {influencers_count}

Use your own ideas also to analize
Formulate your answer as if you were an analyst making a summary judgment on the suspiciousness of a cryptoproject account.
"""

    response = openai.ChatCompletion.create(
        model='gpt-4',
        messages=[
            {"role": "system", "content": "You're an expert at analyzing suspicious crypto projects on Twitter. Write clearly and to the point. Give also the percent of perspectivity of account"},
            {"role": "user", "content": prompt}
        ]
    )
    full_response = response['choices'][0]['message']['content'].strip()


    match = re.search(r'(\d{1,3})\s*%', full_response)
    if match:
        score = int(match.group(1))
    else:
        score = 50

    return full_response, score