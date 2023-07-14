import pandas as pd
from pymongo import MongoClient

# MongoDB client URL
mongo_url = 'mongodb+srv://Randhir_Singh:bp2HeWb6Hb5M3zqD@cluster0.fdttuly.mongodb.net/?retryWrites=true&w=majority'

# CSV file path
csv_file = 'data\sensor_data.csv'

# Read CSV file into a pandas DataFrame
data = pd.read_csv(csv_file)

# Convert DataFrame to a list of dictionaries (one per row)
records = data.to_dict(orient='records')

# Connect to MongoDB
client = MongoClient(mongo_url)
db = client.sensor_data
collection = db.sensor_data

# Insert records into the collection
collection.insert_many(records)

# Close MongoDB connection
client.close()

print("CSV data uploaded to MongoDB successfully!")
