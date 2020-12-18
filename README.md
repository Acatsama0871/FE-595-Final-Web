# FE-595-Final-Web
This is github repo for the trading strategy illustration website: 
[http://18.217.125.148:8000](http://18.217.125.148:8000) and it is part of our
[FE595 Final Project](https://github.com/Acatsama0871/FE-595-Final). Please 
follow the link to see full description.
## Usage
The user of the website are able to choose a time period between 2020-01-06 and
2020-12-07 to backtest the ML trading strategy. After receiving the time period,
the website will generate the P&L plot, strategy performance table, trading actions
and the confusion matrix of the ML prediction.
## Deployment
To deploy the website on other server:
1. Down load the repo to server.
2. Install python and pip(pip3).
2. And run the following in terminal.
```
cd FE-595-Final-Web
pip install -r requirements.txt
python app.py
```
