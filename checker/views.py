import matplotlib
matplotlib.use('Agg')

from django.shortcuts import render, redirect
from .forms import TwitterCheckerForm
import re
from .influencers import load_influencer_usernames
from .twitter_api import get_user_data, get_followers_usernames, get_recent_tweets
from .openai import check_ai_usage, generate_ai_summary
from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd
import os

def generate_pie_chart(score, username):
    values = [score, 100 - score]
    colors = ['#012A36', '#29274C']

    fig, ax = plt.subplots(figsize=(4, 4))

    wedges, texts, autotexts = ax.pie(
        values,
        labels=['Perspectivity', ''],
        startangle=140,
        colors=colors,
        autopct=lambda pct: f'{int(round(pct))}%' if pct > 10 else '',
        wedgeprops={
            'linewidth': 1,
            'edgecolor': '#161528',
            'width': 0.6,
        },
        textprops={'fontsize': 12, 'color': 'white'},
    )

    wedges[0].set_linewidth(2)
    wedges[0].set_edgecolor('#000F14')
    wedges[0].set_capstyle('round')

    ax.axis('equal')
    for text in texts[1:]:
        text.set_text('')

    img_path = f'static/charts/{username}_chart.png'
    os.makedirs(os.path.dirname(img_path), exist_ok=True)
    plt.savefig(img_path, bbox_inches='tight', transparent=True)
    plt.close()
    return img_path

def extract_username(twitter_url):
    match = re.search(r'x\.com/([A-za-z0-9)]{1,15})', twitter_url)
    return match.group(1) if match else None

def format_date(iso_date_str):
    dt = datetime.fromisoformat(iso_date_str.replace("Z", "+00:00"))
    return dt.strftime('%d %B %Y')

def index(request):
    if request.method == 'POST':
        form = TwitterCheckerForm(request.POST)
        if form.is_valid():
            twitter_url = form.cleaned_data['twitter_url']
            username = extract_username(twitter_url)
            if username:
                return redirect('project_result', username=username)
    else:
        form = TwitterCheckerForm()

    return render(request, 'checker/index.html', {'form': form})

def project_result(request, username):
    return render(request, 'checker/result.html', {'username': username})

def result(request):
    return render(request, 'checker/result.html')

def project_result(request, username):
    user_data = get_user_data(username)

    if not user_data:
        return render(request, 'checker/result.html', {'error': 'No user found', 'username': username})

    formatted_date = format_date(user_data['created_at'])

    influencer_usernames = load_influencer_usernames()

    user_id = user_data['id']

    followers = get_followers_usernames(user_id)

    influencers_following = influencer_usernames.intersection(followers)
    influencers_count = len(influencers_following)
    recent_tweets = get_recent_tweets(user_data['id'], count=10)
    ai_used = check_ai_usage(recent_tweets)
    fake_activity = 'Yes'
    summary, score = generate_ai_summary(
        username=username,
        user_data=user_data,
        ai_used=ai_used,
        influencers_count=influencers_count,
    )
    perspectivity = generate_pie_chart(score, username)

    return render(request, 'checker/result.html', {
        'username': username,
        'created_at': formatted_date,
        'followers_count': user_data['followers_count'],
        'tweet_count': user_data['tweet_count'],
        'influencer_count': influencers_count,
        'ai_used': ai_used,
        'fake_activity': fake_activity,
        'summary': summary,
        'perspectivity': perspectivity,
    })