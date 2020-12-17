# app.py
# main function for flask app


# modules
from datetime import datetime
from flask import Flask, render_template, request, abort, Markup
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

    return render_template('backtest.html',
                           dates=dates_seq,
                           action_content='/report')


# response page: report
@app.route('/report', methods=['GET', 'POST'])
def report():
    if request.method == 'GET':  # block direct access
        abort(403)
    elif request.method == 'POST':
        # retrieve dates
        begin_date = request.form['begin_date']
        end_date = request.form['end_date']
        FMT = "%Y-%m-%d"
        begin_date_time = datetime.strptime(begin_date, FMT)
        end_date_time = datetime.strptime(end_date, FMT)
        time_delta = end_date_time - begin_date_time
        
        # check dates
        if time_delta.days >= 4 * 7:
            # add table
            table1 = create_dataframe()

            # add plot
            create_plot2(10)

            return render_template('report.html',
                                   tables=[table1.to_html(classes="table", header=True, justify="center")],
                                   titles=table1.columns.values,
                                   text="text\n" * 1000
                                   )
        else:
            abort(406)


# Error handler
@app.errorhandler(403)
def forbidden(error):
    error_type = "403 Forbidden"
    error_message = "The direct access to report page are not allowed. Please try to use Backtest page to generate report."

    return render_template('errors/error_template.html',
                           error_type=error_type,
                           error_message=error_message), 403

@app.errorhandler(404)
def not_found(error):
    error_type = "404 Not Found"
    error_message = "The requested URL was not found on this server."

    return render_template('errors/error_template.html',
                           error_type=error_type,
                           error_message=error_message), 404

@app.errorhandler(406)
def not_acceptable(error):
    error_type = "406 Not Acceptable"
    error_message = Markup("The end date is less than the begin date or the time interval is less than 4 weeks. "
                           "<br> Please return to Backtest page and choose valid dates.")

    return render_template('errors/error_template.html',
                           error_type=error_type,
                           error_message=error_message), 406


if __name__ == '__main__':
    app.run(debug=True)
