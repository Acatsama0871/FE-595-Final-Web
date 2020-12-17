# utility.py
# the utilities function for Flask app

# module
import os
import pystore
import pandas as pd


# generate date series for day select
def generate_date(begin_date, end_date):
    dates_seq = pd.date_range(begin_date, end_date).tolist()[::7]
    dates_seq = [date.to_pydatetime().strftime("%Y-%m-%d") for date in dates_seq]

    return dates_seq

# get data by dates
def get_data(begin_date, end_date):
    # set database path
    pystore.set_path(os.path.join(os.getcwd(), "database"))

    # load data
    features_data = pystore.store("market_data").collection("feature").item("features").to_pandas()
    market_data = pystore.store("market_data").collection("download").item("downloads").to_pandas()

    # subset the data
    features_data = features_data[features_data["Date"] >= begin_date]
    features_data = features_data[features_data["Date"] <= end_date]
    market_data = market_data[market_data["Date"] >= begin_date]
    market_data = market_data[market_data["Date"] <= end_date]

    return market_data, features_data
