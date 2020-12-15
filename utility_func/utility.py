# utility.py
# the utilities function for Flask app

# module
from datetime import datetime
import pandas as pd


# generate date series for day select
def generate_date(begin_date, end_date):
    dates_seq = pd.date_range(begin_date, end_date).tolist()[::7]
    dates_seq = [date.to_pydatetime().strftime("%Y-%m-%d") for date in dates_seq]

    return dates_seq
