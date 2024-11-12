import praw
import pandas as pd
from datetime import datetime


def get_submission_date(submission):
    """
    Get the submission date of a Reddit submission

    Args:
        submission: Reddit submission

    Returns:
        date: Submission date
    """
    time = submission.created
    return datetime.utcfromtimestamp(time).strftime('%Y-%m-%d')


def get_comments(submission, limit):
    """
    Gets comments from a Reddit submission

    Args:
        submission: Reddit submission
        limit: Number of comments to retrieve

    Returns:
        comments: List of comments
    """
    submission.comments.replace_more(limit=0)
    comments = []

    # limit to 300 comments per post
    num_comments = 0
    for comment in submission.comments.list():
        if num_comments >= limit:
            break
        comments.append(comment.body)
        num_comments += 1
    return comments


def get_articles(subreddit, time_filter, limit):
    """
    Get articles from a Reddit subreddit

    Args:
        subreddit: Reddit subreddit
        time_filter: Time filter for the subreddit
        limit: Number of articles to retrieve

    Returns:
        articles: List of articles
    """
    submissions = subreddit.top(time_filter=time_filter, limit=limit)
    articles = []
    for submission in submissions:
        articles.append({
            'id': submission.id,
            'title': submission.title,
            'url': submission.url,
            'date': get_submission_date(submission),
            'num_upvotes': submission.ups,
            'num_comments': submission.num_comments
        })
    return articles


