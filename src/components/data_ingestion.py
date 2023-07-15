import os
import sys
import pandas as pd
from dataclasses import dataclass
import configparser

from sklearn.model_selection import train_test_split

from src.logger import logging
from src.exception import CustomException
from src.utils import export_collection_as_dataframe


config = configparser.ConfigParser()
config.read('config\mongo_df.ini')

CLIENT_URL = config.get('Credentials', 'url')
MONGO_DATABASE_NAME = config.get('Database','database')
MONGO_COLLECTION_NAME = config.get('Database','collection')

@dataclass
class DataIngestionConfig:
    train_data_path : str = os.path.join('artifacts','train.csv')
    test_data_path : str = os.path.join('artifacts','test.csv')
    raw_data_path : str = os.path.join('artifacts','raw_data.csv')


class DataIngestion:

    def __init__(self):
        self.data_ingestion_config = DataIngestionConfig()

    def initiate_data_ingestion(self):
        logging.info("Entered initiate_data_ingestion method in DataIngestion class")

        try:
           
           df : pd.DataFrame = export_collection_as_dataframe(
                db_name=MONGO_DATABASE_NAME,
                collection_name=MONGO_COLLECTION_NAME,
                db_url=CLIENT_URL
            )
           
           logging.info("Exported collection as dataframe")

           os.makedirs(
               os.path.dirname(self.data_ingestion_config.raw_data_path),exist_ok=True
           )
           df.to_csv(self.data_ingestion_config.raw_data_path, index=False, header=True)

           train_set, test_set = train_test_split(df, test_size=0.2, random_state=123)

           train_set.to_csv(self.data_ingestion_config.train_data_path, index=False, header=True)
           test_set.to_csv(self.data_ingestion_config.test_data_path, index=False, header=True)

           logging.info(f"Data ingested from mongoDB to {self.data_ingestion_config.raw_data_path}")

           return(
               self.data_ingestion_config.train_data_path,
               self.data_ingestion_config.test_data_path
           )


        
        except Exception as e:
            raise CustomException(e, sys)


