from pymongo import MongoClient
import datetime
import plotly.graph_objs as go
from plotly.offline import plot

# MongoDB connection setup
client = MongoClient('mongodb+srv://poojanpatel119:Poojan6216@cluster0.sf4gktc.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')
db = client['NoSQL']
collection = db['AmazonProduct']

def customer_ratings_over_time_graph_plotly():
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

    # Create a Plotly graph
    trace = go.Scatter(
        x=dates,
        y=avg_ratings,
        mode='lines+markers',
        name='Average Rating',
        marker=dict(color='blue')
    )

    layout = go.Layout(
        title='Average Product Ratings Over Time',
        xaxis=dict(title='Date'),
        yaxis=dict(title='Average Rating'),
        hovermode='closest'
    )

    fig = go.Figure(data=[trace], layout=layout)
    plot(fig, filename='interactive_graph.html')

def main():
    customer_ratings_over_time_graph_plotly()

if __name__ == "__main__":
    main()