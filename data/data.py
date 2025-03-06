from superlinked import framework as sl
from superlinked_app import index
import pandas as pd
from pathlib import Path
from loguru import logger
import os

ROOT_DIR = Path(__file__).parent
ENV_FILE = ROOT_DIR / ".env"
logger.info("Loading environment variables from .env file: %s", ENV_FILE)



class DataReader:
    def __init__(self) -> None:
        #self.path = os.getenv('DATA_PATH')
        self.path = "listings.csv"
    def read(self):
        data = pd.read_csv(self.path)
        return data
    
    def preprocess(self, data):
        data['price'] = data['price'].apply(lambda x: float(x[1:].replace(',', '')) if isinstance(x, str) else x)
        data['host_is_superhost']=data['host_is_superhost'].apply(lambda x: 1 if x == 't' else 0)
        data['last_scraped'] = pd.to_datetime(data['last_scraped'])
        data['review_scores_rating'].fillna(-1.0, inplace=True)
        data['price'].fillna(-1.0, inplace=True)
        return data

if __name__ == "__main__":
    data_reader = DataReader()
    data = data_reader.read()
    data = data_reader.preprocess(data)
    
    data.to_csv('listings.csv', index=False)




