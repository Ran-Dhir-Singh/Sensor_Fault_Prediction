import sys
import os
from dataclasses import dataclass
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from imblearn.combine import SMOTETomek
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import RobustScaler, FunctionTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from src.logger import logging
from src.exception import CustomException
from src.utils import save_object


@dataclass
class DataTransformationConfig:
    preprocessor_file_path : str = os.path.join('artifacts','preprocessor.pkl')



class DataTransformation:

    def __init__(self):
        self.data_transformation_config = DataTransformationConfig()


    def get_data_transformation_object(self):
        try:
            logging.info("Initiating preprocessor pipeline")
            # Defining lambda function to replace NA with np.nan
            replace_na_with_nan = lambda X: np.where(X == 'na', np.nan, X)

            # steps for preprocessor pipeline
            nan_replacement_step = ('nan_replacement', FunctionTransformer(replace_na_with_nan))
            imputer_step = ('imputer', SimpleImputer(strategy='constant', fill_value=0))
            scaler_step  = ('scaler', RobustScaler())

            preprocessor = Pipeline(
                steps = [
                    nan_replacement_step,
                    imputer_step,
                    scaler_step
                ]
            )
            logging.info("Preprocessor pipeline completed")

            return preprocessor
        
        except Exception as e:
            logging('Exception in get_data_transformation_object() in DataTransformation class')
            raise CustomException(e,sys)
        
    def initiate_data_transformation(self,train_path,test_path):
        try:
            logging.info("Initiated data transformation")

            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)

            preprocessor = self.get_data_transformation_object()

            target_column_name = 'Good/Bad'
            target_column_mapping = {'+1':0, '-1':1}

            # training dataframe
            input_feature_train_df = train_df.drop(columns=[target_column_name],axis=1)
            target_feature_train_df = train_df[target_column_name].map(target_column_mapping)

            # testing dataframe
            input_feature_test_df= test_df.drop(columns=[target_column_name],axis=1)
            target_feature_test_df = test_df[target_column_name].map(target_column_mapping)

            # using preprocessor object for data transformation
            logging.info("Applying Preprocessing on train and test dataset")
            transformed_input_train_feature = preprocessor.fit_transform(input_feature_train_df)
            transformed_input_test_feature = preprocessor.transform(input_feature_test_df)

            # resampling
            logging.info("Applying SMOTETomek on train and test dataset")
            smt = SMOTETomek(sampling_strategy='minority')

            input_feature_train_final, target_feature_train_final = smt.fit_resample(
                transformed_input_train_feature, target_feature_train_df
            )

            input_feature_test_final, target_feature_test_final = smt.fit_resample(
                transformed_input_test_feature, target_feature_test_df
            )

            # concatenating input and target 
            train_arr = np.c_[input_feature_train_final, np.array(target_feature_train_final)]
            test_arr = np.c_[input_feature_test_final, np.array(target_feature_test_final)]

            # saving object
            save_object(self.data_transformation_config.preprocessor_file_path,
                        obj=preprocessor)
            
            logging.info('preprocessor object saved and train array and test array created')
            
            return(
                train_arr,
                test_arr,
                self.data_transformation_config.preprocessor_file_path
            )
        
        except Exception as e:
            logging.info("Exception occured in initiate_data_transformation() in DataTransformation class")
            raise CustomException(e, sys)