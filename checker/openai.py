import openai
import re

openai.api_key = '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'

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

def generate_fake_activity_summary(user_data):
    prompt = f"""
Analyze the following Twitter user data to detect potential fake activity such as fake followers, inflated likes, or suspicious engagement patterns. 
Summarize your findings in one short sentence suitable for non-technical users.

Data:
- Username: {user_data.get('username')}
- Followers: {user_data.get('followers_count')}
- Friends: {user_data.get('friends_count')}
- Tweets: {user_data.get('tweet_count')}
- Verified: {user_data.get('verified')}
- Account Created: {user_data.get('created_at')}
- Protected: {user_data.get('protected')}
"""

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an expert in social media analysis."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=80,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return "Could not generate analysis at this time."

def generate_ai_summary(username, user_data, ai_used, influencers_count):
    prompt = f"""
    Write a short review of a twitter crypto project @{username}. Analyze it with your own metrics, give a short opinion about it in 2-3 sentences. 
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