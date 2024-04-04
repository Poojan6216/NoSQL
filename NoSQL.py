from textblob import TextBlob
import pandas as pd
from pymongo import MongoClient
import matplotlib.pyplot as plt

# Connect to MongoDB
client = MongoClient('mongodb+srv://poojanpatel119:Poojan6216@cluster0.sf4gktc.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')
db = client['NoSQL']
reviews = db['AmazonProduct']

# Fetch reviews with necessary fields
cursor = reviews.find({}, {'reviews.date': 1, 'reviews.text': 1, 'reviews.rating': 1})

# Analyze sentiment and prepare for aggregation
results = []
for document in cursor:
    sentiment = TextBlob(document['reviews']['text']).sentiment.polarity
    results.append({
        'date': pd.to_datetime(document['reviews']['date']),
        'sentiment': sentiment,
        'rating': document['reviews']['rating']
    })

# Convert to DataFrame
df = pd.DataFrame(results)

# Group by date and calculate mean sentiment and rating
daily_means = df.groupby(df['date'].dt.date).mean()

# Plotting
daily_means.plot(y=['sentiment', 'rating'], figsize=(14, 7), title="Sentiment and Rating Trend Over Time")
plt.show()