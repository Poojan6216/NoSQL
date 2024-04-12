from pymongo import MongoClient

# Connect to the MongoDB database
client = MongoClient('mongodb+srv://poojanpatel119:Poojan6216@cluster0.sf4gktc.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')
db = client['NoSQL']  # Replace with your database name
collection = db['AmazonProduct']  # Replace with your collection name

# Ensure there's a text index on the 'reviews.text' field
collection.create_index([('reviews.text', 'text')])

# Sample search text
search_text = 'long lasting batteries'  # Replace with your search criteria

# Perform a text search
results = collection.find({'$text': {'$search': search_text}},
                          {'score': {'$meta': 'textScore'}}).sort([('score', {'$meta': 'textScore'})])

# Print out the matched documents
for result in results:
    print(result['name'], result['asins'], result['reviews.text'])

# Don't forget to close the MongoDB connection
client.close()