import sys
import os
import pickle
import numpy as np
import pandas as pd

from pymongo import MongoClient

from src.logger import logging
from src.exception import CustomException

from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error

def save_object(file_path, obj):
    try:
        dir_path = os.path.dirname(file_path)

        os.makedirs(dir_path, exist_ok=True)

        with open(file_path,'wb') as file_obj:
            pickle.dump(obj, file_obj)

    except Exception as e:
        raise CustomException(e, sys)
    


def evaluate_model(X_train, y_train, X_test, y_test, models):
    try:
        report = {}
        for i in range(len(models)):
            model = list(models.values())[i]
            model.fit(X_train, y_train)


            y_test_pred = model.predict(X_test)

            test_model_score = r2_score(y_test, y_test_pred)

            report[list(models.keys())[i]] = test_model_score

        return report
    

    except Exception as e:
        logging.info("Exception occured during model training")
        raise CustomException(e, sys)
    


def load_object(file_path):
    try:
        with open(file_path, 'rb') as file_obj :
            return pickle.load(file_obj)
        
    except Exception as e:
        logging.info("Exception occured in load_object function utils")
        raise CustomException(e, sys)


def export_collection_as_dataframe(collection_name, db_name,db_url):
    try:
        
        # Connect to MongoDB
        client = MongoClient(db_url)
        db = client[db_name]
        collection = db[collection_name]

        # Retrieve all documents from the collection
        cursor = collection.find()
        records = list(cursor)

        # Convert list of documents to a DataFrame
        df = pd.DataFrame(records)
        df.drop('_id', axis=1, inplace=True)


        # Close MongoDB connection
        client.close()

    

        return df

    except Exception as e:
        raise CustomException(e, sys)