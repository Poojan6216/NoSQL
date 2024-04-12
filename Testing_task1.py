import pandas as pd
from pymongo import MongoClient
import matplotlib.pyplot as plt
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from collections import Counter

# Connect to MongoDB
client = MongoClient('mongodb+srv://poojanpatel119:Poojan6216@cluster0.sf4gktc.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')
db = client['NoSQL']
reviews = db['AmazonProduct']

# Fetch reviews with necessary fields
cursor = reviews.find({}, {'reviews.date': 1, 'reviews.text': 1, 'reviews.rating': 1})

# Sentiment Analyzer
sid = SentimentIntensityAnalyzer()

# Data Preprocessing
def preprocess_text(text):
    stop_words = set(stopwords.words('english'))
    tokens = word_tokenize(text)
    filtered_tokens = [word.lower() for word in tokens if word.lower() not in stop_words and word.isalpha()]
    return filtered_tokens

# Analyze sentiment and prepare for aggregation
results = []
for document in cursor:
    abc = str(document['reviews']['text'])
    sentiment = sid.polarity_scores(abc)['compound']
    rating = document['reviews']['rating']
    try:
        rating = float(rating)
    except ValueError:
        rating = None  # Convert problematic value to NaN
    results.append({
        'date': pd.to_datetime(document['reviews']['date']),
        'sentiment': sentiment,
        'rating': rating,
        'text': abc
    })

# Convert to DataFrame
df = pd.DataFrame(results)

# Group by date and calculate mean sentiment and rating
daily_means = df.groupby(df['date'].dt.date).mean()

# Plotting
plt.figure(figsize=(12, 6))
plt.subplot(1, 2, 1)
df['rating'].hist(bins=5)
plt.title('Distribution of Ratings')
plt.xlabel('Rating')
plt.ylabel('Frequency')

plt.subplot(1, 2, 2)
df['sentiment'].hist(bins=20)
plt.title('Distribution of Sentiment Scores')
plt.xlabel('Sentiment Score')
plt.ylabel('Frequency')
plt.show()

plt.figure(figsize=(12, 6))
plt.plot(daily_means.index, daily_means['sentiment'], color='blue', marker='o')
plt.title('Mean Sentiment Over Time')
plt.xlabel('Date')
plt.ylabel('Mean Sentiment Score')
plt.show()

positive_sentiment = df[df['sentiment'] > 0]['sentiment']
negative_sentiment = df[df['sentiment'] < 0]['sentiment']
neutral_sentiment = df[df['sentiment'] == 0]['sentiment']

plt.figure(figsize=(10, 6))
plt.hist([positive_sentiment, negative_sentiment, neutral_sentiment], bins=20, color=['green', 'red', 'grey'], label=['Positive', 'Negative', 'Neutral'])
plt.title('Distribution of Sentiment Scores')
plt.xlabel('Sentiment Score')
plt.ylabel('Frequency')
plt.legend()
plt.show()

# Analyze most frequent words
df['tokens'] = df['text'].apply(preprocess_text)
all_words = [word for tokens in df['tokens'] for word in tokens]
word_freq = Counter(all_words)
common_words = word_freq.most_common(20)

plt.figure(figsize=(10, 6))
plt.bar(range(len(common_words)), [val for word, val in common_words], align='center')
plt.xticks(range(len(common_words)), [word for word, val in common_words])
plt.title('Top 20 Most Common Words')
plt.xlabel('Word')
plt.ylabel('Frequency')
plt.xticks(rotation=45)
plt.show()
