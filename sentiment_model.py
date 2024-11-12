from transformers import BertTokenizer, BertForSequenceClassification
import torch
import pandas as pd

# Load pre-trained BERT tokenizer and model for sentiment analysis
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertForSequenceClassification.from_pretrained('nlptown/bert-base-multilingual-uncased-sentiment')  # Pre-trained for sentiment analysis


def get_sentiment_score(text):
    """
    Get sentiment score from a text

    Args:
        text: Text to analyze

    Returns:
        sentiment_score: Sentiment score
    """
    inputs = tokenizer(text, return_tensors='pt', padding=True, truncation=True)
    outputs = model(**inputs)
    probs = torch.nn.functional.softmax(outputs.logits, dim=1)  # Now we have logits from BertForSequenceClassification
    sentiment_score = torch.argmax(probs, dim=1).item() + 1  # Output is a score between 1 and 5
    return sentiment_score