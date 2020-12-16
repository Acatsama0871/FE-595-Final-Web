# app.py
# main function for flask app


# modules
from flask import Flask, render_template
from functions.utility import *


app = Flask(__name__)


# static pages
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/backtest')
def backtest():
    # set begin and end dates
    begin_date = "2020-01-06"
    end_date = "2020-12-07"

    # generate dates seq
    dates_seq = generate_date(begin_date, end_date)

    return render_template('backtest.html', dates=dates_seq)

# response page: report
@app.route('/report')
def report():
    # add table
    table1 = create_dataframe()

    # add plot
    create_plot2(10)

    return render_template('report.html',
                           tables=[table1.to_html(classes="table", header=True, justify="center")],
                           titles=table1.columns.values,
                           text="text\n" * 1000
                           )


if __name__ == '__main__':
    app.run(debug=True)
