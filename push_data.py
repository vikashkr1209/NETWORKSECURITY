# ETL pipeline setup after pymongo setup
import os
import sys
import json

from dotenv import load_dotenv

load_dotenv()

MONGO_DB_URL = os.getenv("MONGO_DB_URL")
print(MONGO_DB_URL)

import certifi

ca = certifi.where()

import pandas as pd
import numpy as np
import pymongo
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

class NetworkDataExtract():

    def __init__(self):
        try:
            pass
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    # read all the csv data to convert json data
    def cv_to_json_convertor(self,file_path):
        try:
            data = pd.read_csv(file_path)
            # drop index
            data.reset_index(drop=True,inplace=True)
            records=list(json.loads(data.T.to_json()).values()) # this will gives as the list of records 
            return records
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        

    def insert_data_mongodb(self,records,database,collection):
        try:
            self.database = database
            self.collection = collection
            self.records = records
            self.mongo_clients= pymongo.MongoClient(MONGO_DB_URL)
            self.database = self.mongo_clients[self.database]

            self.collection = self.database[self.collection]
            self.collection.insert_many(self.records)
            return(len(self.records))
        except Exception as e:
            raise NetworkDataExtract(e,sys)


if __name__=='__main__':
    FILE_PATH = "Network_Data\phisingData.csv"
    DATABASE="VIKASHKR"
    Collection="NetworkData"
    networkobj=NetworkDataExtract()
    records = networkobj.cv_to_json_convertor(file_path=FILE_PATH)
    print(records)
    no_of_records = networkobj.insert_data_mongodb(records,DATABASE,Collection)
    print(no_of_records)
