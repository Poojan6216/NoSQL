from pymongo import MongoClient
import datetime

# MongoDB connection setup
client = MongoClient('mongodb+srv://poojanpatel119:Poojan6216@cluster0.sf4gktc.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')
db = client['NoSQL']
collection = db['AmazonProduct']

def create_text_index():
    # Create a text index on the 'reviews.text' field
    collection.create_index([("reviews.text", "text")])

def product_recommendation_by_text(search_text):
    # Search for products with similar review text
    query = {'$text': {'$search': search_text}}
    projection = {'name': 1, 'asins': 1, '_id': 0}
    results = collection.find(query, projection)
    for product in results:
        print(product)

def aggregate_ratings_by_product():
    # Aggregate average ratings by product
    pipeline = [
        {'$group': {'_id': '$name', 'averageRating': {'$avg': '$reviews.rating'}}}
    ]
    results = collection.aggregate(pipeline)
    for result in results:
        print(result)

def customer_sentiment_over_time():
    # Analyze sentiment changes over time (example uses dateAdded)
    pipeline = [
        {'$match': {'dateAdded': {'$gte': datetime.datetime(2020, 1, 1)}}},
        {'$group': {'_id': '$dateAdded', 'averageSentiment': {'$avg': '$reviews.sentiment'}}}
    ]
    results = collection.aggregate(pipeline)
    for result in results:
        print(result)

def main():
    # Uncomment the functions below to run them
    create_text_index()
    product_recommendation_by_text("great battery life")
    aggregate_ratings_by_product()
    customer_sentiment_over_time()

if __name__ == "__main__":
    main()




# The task involves connecting to a MongoDB database, performing a text search on a collection of Amazon products, and retrieving documents that match a specific search criteria. The search is based on the presence of certain keywords in the reviews of the products.

# To achieve this, the code establishes a connection to the MongoDB database, ensures the existence of a text index on the 'reviews.text' field, and performs a text search using the `$text` operator with the specified search text. The results are then sorted based on the relevance score obtained from the text search.

# However, during the execution of the query, there was an error related to memory limits being exceeded during sorting. To address this issue, external sorting was enabled using the `allow_disk_use(True)` option. But subsequently, another error occurred due to the combination of text search and hint in the same query, which is not allowed.

# As a resolution, the hint part was removed from the query, and the text search was performed without it.

# The conclusion drawn from this task is the importance of understanding MongoDB query limitations and the necessity to handle memory constraints when dealing with large datasets. Additionally, ensuring compatibility between different query operators is crucial to avoid errors during execution.