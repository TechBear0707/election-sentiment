from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import re
import pandas as pd

# Load the comments and submissions data
df_comments = pd.read_csv('comments.csv')
df_submissions = pd.read_csv('submissions.csv')

# Merge dataframes on 'id' column to associate each comment with its respective candidate
merged_df = pd.merge(df_comments, df_submissions[['id', 'candidate']], on='id', how='inner')

# Combine all comments for each candidate into one string
candidate_comments = merged_df.groupby('candidate')['comment'].apply(lambda x: ' '.join(x))

# Create a comprehensive stopwords set
basic_stopwords = set(STOPWORDS)
custom_stopwords = {
    'trump', 'harris', 'donald', 'kamala', 'biden', 'walz', 'wills', 'will', 's', 'like', 'get', 'one', 'also',
    'people',
    'said', 'time', 'going', 'think', 'want', 'say', 'know', 'make', 'see', 'us', 'take', 'would', 'could', 'should',
    'may', 'might', 'must', 'many', 'much', 'still', 'even', 'way', 'back', 'come', 'first', 'last', 'since', 'made',
    'well', 'thing', 'things', 'two', 'year', 'years', 'today', 'day', 'days', 'another', 'new', 'need', 'right',
    'left',
    'go', 'look', 'give', 'mean', 'never', 'always', 'every', 'part', 'feel', 'around', 'said', 'say', 'mr', 'ms',
    'mrs', 'dr', 'etc', 'u', 'r', 'll', 're', 've'
}
# Combine basic and custom stopwords
advanced_stopwords = basic_stopwords.union(custom_stopwords)


# Text preprocessing function to clean and lemmatize comments
def preprocess_text(text):
    # Lowercase the text
    text = text.lower()
    # Remove possessive endings ('s) and punctuation
    text = re.sub(r"\b(\w+)'s\b", r"\1", text)
    text = re.sub(r'[^\w\s]', '', text)  # Remove punctuation
    return text


# Apply preprocessing and generate word clouds for each candidate
for candidate, comments in candidate_comments.items():
    # Preprocess the combined comments text
    processed_comments = preprocess_text(comments)

    # Generate the word cloud
    wordcloud = WordCloud(width=800, height=400, background_color='white', stopwords=advanced_stopwords).generate(
        processed_comments)

    # Plot the word cloud
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.title(f'Word Cloud for {candidate}')
    plt.show()
