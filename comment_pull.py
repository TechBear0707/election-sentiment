import pandas as pd
import numpy as np
from helper import *
from sentiment_model import *
import praw
import dotenv
import os

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

# Load the data
submission_df = pd.read_csv('submissions.csv')

print(submission_df.head())

# Get the average sentiment score for each candidate
avg_sentiment = submission_df.groupby('candidate')['sentiment'].mean()

print(avg_sentiment)

print(len(submission_df[submission_df['candidate'] == 'Harris']))
print(len(submission_df[submission_df['candidate'] == 'Trump']))

# pull 200 comments from each submission (row) from the df
comments_df = pd.DataFrame(columns=['id', 'comment', 'sentiment_score', 'sentiment_label'])
for index, row in submission_df.iterrows():
    submission = reddit.submission(id=row['id'])
    comments = get_comments(submission, 50)
    for comment in comments:
        comment_sentiment = get_sentiment_score(comment)
        comment_date = get_submission_date(submission)
        # mapping sentiment score to sentiment
        if comment_sentiment == 1:
            sentiment = 'Very Negative'
        elif comment_sentiment == 2:
            sentiment = 'Negative'
        elif comment_sentiment == 3:
            sentiment = 'Neutral'
        elif comment_sentiment == 4:
            sentiment = 'Positive'
        elif comment_sentiment == 5:
            sentiment = ' Very Positive'
        # sub_df to concat to comments_df
        sub_df = pd.DataFrame({'id': [row['id']],
                               'comment': [comment],
                               'sentiment_score': [comment_sentiment],
                               'sentiment_label': [sentiment]})
        comments_df = pd.concat([comments_df, sub_df])

    print(f'Comments for submission {row["id"]} pulled')



# Save the comments to a CSV file
comments_df.to_csv('comments.csv', index=False)
print(comments_df.head())