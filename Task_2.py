# from pymongo import MongoClient
# import datetime

# # MongoDB connection setup
# client = MongoClient('mongodb+srv://poojanpatel119:Poojan6216@cluster0.sf4gktc.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')
# db = client['NoSQL']
# collection = db['AmazonProduct']

# def create_text_index():
#     # Create a text index on the 'reviews.text' field
#     collection.create_index([("reviews.text", "text")])

# def product_recommendation_by_text(search_text):
#     # Search for products with similar review text
#     query = {'$text': {'$search': search_text}}
#     projection = {'name': 1, 'asins': 1, '_id': 0}
#     results = collection.find(query, projection)
#     for product in results:
#         print(product)

# def aggregate_ratings_by_product():
#     # Aggregate average ratings by product
#     pipeline = [
#         {'$group': {'_id': '$name', 'averageRating': {'$avg': '$reviews.rating'}}}
#     ]
#     results = collection.aggregate(pipeline)
#     for result in results:
#         print(result)

# def customer_sentiment_over_time():
#     # Analyze sentiment changes over time (example uses dateAdded)
#     pipeline = [
#         {'$match': {'dateAdded': {'$gte': datetime.datetime(2020, 1, 1)}}},
#         {'$group': {'_id': '$dateAdded', 'averageSentiment': {'$avg': '$reviews.sentiment'}}}
#     ]
#     results = collection.aggregate(pipeline)
#     for result in results:
#         print(result)

# def main():
#     # Uncomment the functions below to run them
#     create_text_index()
#     product_recommendation_by_text("great battery life")
#     aggregate_ratings_by_product()
#     customer_sentiment_over_time()

# if __name__ == "__main__":
#     main()




# The task involves connecting to a MongoDB database, performing a text search on a collection of Amazon products, and retrieving documents that match a specific search criteria. The search is based on the presence of certain keywords in the reviews of the products.

# To achieve this, the code establishes a connection to the MongoDB database, ensures the existence of a text index on the 'reviews.text' field, and performs a text search using the `$text` operator with the specified search text. The results are then sorted based on the relevance score obtained from the text search.

# However, during the execution of the query, there was an error related to memory limits being exceeded during sorting. To address this issue, external sorting was enabled using the `allow_disk_use(True)` option. But subsequently, another error occurred due to the combination of text search and hint in the same query, which is not allowed.

# As a resolution, the hint part was removed from the query, and the text search was performed without it.

# The conclusion drawn from this task is the importance of understanding MongoDB query limitations and the necessity to handle memory constraints when dealing with large datasets. Additionally, ensuring compatibility between different query operators is crucial to avoid errors during execution.







from pymongo import MongoClient
import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# MongoDB connection setup
client = MongoClient('mongodb+srv://poojanpatel119:Poojan6216@cluster0.sf4gktc.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')
db = client['NoSQL']
collection = db['AmazonProduct']

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
