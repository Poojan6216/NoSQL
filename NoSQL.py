from pymongo import MongoClient
from textblob import TextBlob
import pandas as pd
import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# MongoDB connection setup
client = MongoClient('mongodb+srv://poojanpatel119:Poojan6216@cluster0.sf4gktc.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')
db = client['NoSQL']
collection = db['AmazonProduct']

####################################################################
# Task 1 - 

reviews = db['AmazonProduct']
cursor = reviews.find({}, {'reviews.date': 1, 'reviews.text': 1, 'reviews.rating': 1})

# Analyze sentiment and prepare for aggregation
results = []
for document in cursor:
    abc = str(document['reviews']['text'])
    sentiment = TextBlob(abc).sentiment.polarity
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


###############################################################################
# Task 2 - 

def create_text_index():
    # Create a text index on the 'reviews.text' field
    collection.create_index([("reviews.text", "text")])

def product_recommendation_by_text_graph(search_text):
    query = {'$text': {'$search': search_text}}
    projection = {'name': 1, 'asins': 1, '_id': 0}
    results = collection.find(query, projection)
    
    product_counts = {}
    for product in results:
        # Convert the first five words back into a string to use as a dictionary key
        product_name = ' '.join(product['name'].split()[:3])
        if product_name in product_counts:
            product_counts[product_name] += 1
        else:
            product_counts[product_name] = 1

    plt.figure(figsize=(10, 8))
    plt.bar(product_counts.keys(), product_counts.values())
    plt.xlabel('Product Names')
    plt.ylabel('Number of Matches')
    plt.title('Product Recommendations Based on Review Text')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()


##############################################################################
# Task 3 -    

def aggregate_ratings_by_product_graph():
    pipeline = [
        {'$group': {'_id': '$name', 'averageRating': {'$avg': '$reviews.rating'}}}
    ]
    results = collection.aggregate(pipeline)
    
    product_names = []
    avg_ratings = []
    for result in results:
        trimmed_name = ' '.join(result['_id'].split()[:3])
          # Limit to the first two words
        product_names.append(trimmed_name)
        avg_ratings.append(result['averageRating'])
    
    plt.figure(figsize=(10, 8))
    plt.bar(product_names, avg_ratings, color='skyblue')
    plt.xlabel('Product Names')
    plt.ylabel('Average Rating')
    plt.title('Average Ratings by Product')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()


##############################################################################
# Task 4 -  

def customer_ratings_over_time_graph():
    # This pipeline filters reviews, groups them by date, and calculates the average rating for each date
    pipeline = [
        {'$unwind': '$reviews'},
        {'$group': {
            '_id': '$reviews.date',
            'averageRating': {'$avg': '$reviews.rating'}
        }},
        {'$sort': {'_id': 1}}  # Sorting by date in ascending order
    ]
    results = collection.aggregate(pipeline)
    
    dates = []
    avg_ratings = []
    for result in results:
        if result['_id'] and result['averageRating']:  # Ensure the date and rating are not None
            dates.append(result['_id'])
            avg_ratings.append(result['averageRating'])

    if not dates:  # Check if data is available
        print("No data found for the given criteria.")
        return

    plt.figure(figsize=(12, 6))
    plt.plot(dates, avg_ratings, marker='o', linestyle='-', color='blue')
    plt.xlabel('Date')
    plt.ylabel('Average Rating')
    plt.title('Average Product Ratings Over Time')
    plt.gca().xaxis.set_major_locator(mdates.YearLocator())
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def main():
    create_text_index()  # Uncomment this line if text index is not already created
    product_recommendation_by_text_graph("great battery life")
    aggregate_ratings_by_product_graph()
    customer_ratings_over_time_graph()

if __name__ == "__main__":
    main()
