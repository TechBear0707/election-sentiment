import pandas as pd
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt  # Correct import for pyplot
import seaborn as sns
import dotenv
import os
from helper import *
from sentiment_model import *

# Load environment variables
dotenv.load_dotenv()

# username and passwords from environment variables
username = os.getenv('USERNAME')
password = os.getenv('PASSWORD')
client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')

# Create a Reddit instance
reddit = praw.Reddit(client_id=client_id,
                         client_secret=client_secret,
                         user_agent='election_sentiment',
                         username=username,
                         password=password)

# Define candidate keywords
trump_keywords = ['trump', 'donald', 'MAGA', 'vance', 'eric trump', 'ivanka trump', 'donald trump jr']
harris_keywords = ['kamala', 'harris', 'walz', 'douglas emhoff']

# Get top 1000 submissions from r/politics in the past year
submissions = get_articles(reddit.subreddit('politics'), 'year', 1000)

# Filter for Trump-related submissions
trump_submissions = [
    submission for submission in submissions
    if any(keyword.lower() in submission['title'].lower() for keyword in trump_keywords)
]
# filter out submissions that also mention Harris
trump_submissions = [
    submission for submission in trump_submissions
    if not any(keyword.lower() in submission['title'].lower() for keyword in harris_keywords)
]
trump_df = pd.DataFrame(trump_submissions)
trump_df['candidate'] = 'Trump'

# Filter for Harris-related submissions
harris_submissions = [
    submission for submission in submissions
    if any(keyword.lower() in submission['title'].lower() for keyword in harris_keywords)
]
# filter out submissions that also mention Trump
harris_submissions = [
    submission for submission in harris_submissions
    if not any(keyword.lower() in submission['title'].lower() for keyword in trump_keywords)
]
harris_df = pd.DataFrame(harris_submissions)
harris_df['candidate'] = 'Harris'

# concatenate the dataframes
submission_df = pd.concat([trump_df, harris_df])

# Get sentiment scores for each submission
submission_df['sentiment'] = submission_df['title'].apply(get_sentiment_score)

# Mapping scores to labels
score_labels = {
    1: 'Very Negative',
    2: 'Negative',
    3: 'Neutral',
    4: 'Positive',
    5: 'Very Positive'
}
submission_df['sentiment_label'] = submission_df['sentiment'].map(score_labels)

# write to csv
submission_df.to_csv('submissions.csv', index=False)

print(submission_df.head())

