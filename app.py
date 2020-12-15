# app.py
# main function for flask app


# modules
from flask import Flask, render_template, request
from utility_func.utility import generate_date


app = Flask(__name__)


# static pages
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/day_select')
def day_select():
    # set begin and end dates
    begin_date = "2020-01-06"
    end_date = "2020-12-07"

    # generate dates seq
    dates_seq = generate_date(begin_date, end_date)

    return render_template('day_select.html',
                           dates=dates_seq)

if __name__ == '__main__':
    app.run(debug=True)
