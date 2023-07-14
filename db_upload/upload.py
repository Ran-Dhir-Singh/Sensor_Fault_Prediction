import pandas as pd
from pymongo import MongoClient
import configparser


config = configparser.ConfigParser()
config.read('config/mongo_df.ini')

username = config.get('Credentials', 'username')
password = config.get('Credentials', 'password')



def upload_to_mongo_db(client_url,database,collection_name,file_path):
    
   
    #Read CSV file into pandas dataframe
    data = pd.read_csv(file_path)

    # Convert Dataframe to a list of dictionaries
    records = data.to_dict(orient='records')

    # Connect to MongoDB
    client = MongoClient(client_url)
    db = client[database]
    collection = db[collection_name]

    # Insert records into the collection
    collection.insert_many(records)

    # Close MongoDB connection
    client.close()

    print("CSV data uploaded to MongoDB successfully!")


# MongoDB client URL
mongo_url = 'mongodb+srv://'+username+':'+password+'@cluster0.fdttuly.mongodb.net/?retryWrites=true&w=majority'

# CSV file path
csv_file = 'data\sensor_data.csv'

# database name
database = "sensor_data"

#collection name
collection = "sensor_data_raw"


upload_to_mongo_db(mongo_url,database,collection,csv_file)