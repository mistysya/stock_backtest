import datetime
import sys
sys.path.append('..')
from .load_stock_data import Data

def load_stock_data(pickle_filename="stock_data.pickle"):
    print("Loading stock database...")
    stock_database = Data(pickle_filename)
    stock_database.load_data_from_pickle()
    stock_data = stock_database.get_data()
    print("Load stock database finish")
    return stock_data