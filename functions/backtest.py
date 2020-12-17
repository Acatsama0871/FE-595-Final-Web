# backtest.py
# functions for backtest

# modules
import base64
from io import BytesIO
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn import metrics
from scipy.stats import skew, kurtosis, norm


# PNL plot function
def strategy_profitability_performance(features, y_pred, principal=1, bool_return=False):
    # 1+r return 
    log_return = features['SPY_log'][1:len(features)].values
    simple_return = np.exp(log_return) - 1

    spy_return_ = simple_return + 1
    strategy_return = np.where(y_pred[0:len(features) - 1] == 1, spy_return_, 1)

    # cumulative return 
    strategy_cumulative_return = np.cumprod(strategy_return)
    # benchmark return 
    benchmark_cumulative_return = np.cumprod(spy_return_)

    # save the result
    res = pd.DataFrame()
    res['Date'] = features['Date'][0:len(features) - 1]
    res['StrategyCumulativePnL'] = strategy_cumulative_return * principal
    res['BenchmarkCumulativePnl'] = benchmark_cumulative_return * principal

    plt.grid(True)
    plt.xlabel('Date')
    plt.ylabel('CumulativeP&L')
    dates = pd.to_datetime(res['Date'], dayfirst=True)
    plt.plot(dates, res['StrategyCumulativePnL'].values, label='My Strategy')
    plt.plot(dates, res['BenchmarkCumulativePnl'].values, label='Always holding SP500')
    plt.xticks(rotation=30)
    plt.title('The Strategy VS Benchmark P&L')
    plt.legend(fancybox=True, framealpha=0.5)

    # convert to html
    buffer = BytesIO()
    plt.savefig(buffer, bbox_inches="tight", transparent=True)
    plt.close()
    plot_data = buffer.getvalue()
    imb = base64.b64encode(plot_data)
    ims = imb.decode()
    imd = "data:image/png;base64," + ims

    if bool_return:
        return imd, res
    else:
        return imd


# strategy stats
def strategy_stats_performance(pnl_table):
    row = len(pnl_table)
    strategy_return = np.diff(pnl_table['StrategyCumulativePnL'], 1) / pnl_table['StrategyCumulativePnL'][1:row]
    benchmark_return = np.diff(pnl_table['BenchmarkCumulativePnl'], 1) / pnl_table['BenchmarkCumulativePnl'][1:row]

    strategy = []
    benchmark = []

    # annual return
    strategy_annual_return = strategy_return * 52
    benchmark_annual_return = benchmark_return * 52

    # annual average return
    strategy.append(np.mean(strategy_annual_return))
    benchmark.append(np.mean(benchmark_annual_return))

    # annual vol
    strategy.append(np.std(strategy_annual_return) / np.sqrt(52))
    benchmark.append(np.std(benchmark_annual_return) / np.sqrt(52))

    # annual skewness
    strategy.append(skew(strategy_annual_return))
    benchmark.append(skew(benchmark_annual_return))

    # annual kurtosis
    strategy.append(kurtosis(strategy_annual_return))
    benchmark.append(kurtosis(benchmark_annual_return))

    # 95% VaR
    strategy.append(norm.ppf(1 - 0.95, np.mean(strategy_return),
                             np.std(strategy_return)))
    benchmark.append(norm.ppf(1 - 0.95, np.mean(benchmark_return),
                              np.std(benchmark_return)))

    # Return rate
    strategy.append(pnl_table['StrategyCumulativePnL'].values[-1])
    benchmark.append(pnl_table['BenchmarkCumulativePnl'].values[-1])

    # sharpe ratio
    strategy.append(np.mean(strategy_annual_return) / np.std(strategy_annual_return))
    benchmark.append(np.mean(benchmark_annual_return) / np.std(benchmark_annual_return))

    res = pd.DataFrame()
    res['My_Strategy'] = strategy
    res['Benchmark'] = benchmark
    res.index = ['Annual_Average_Return', 'Annual_Volality',
                 'Annual_Sknewness', 'Annual_Kurtosis', '95%_VaR',
                 'P&L', 'Annual_Sharpe_Ratio']
    return res


# trading actions
def trading_action(features, y_pred, shares=100):
    initial_position = 0
    table = []
    n_row = len(y_pred)
    date = features['Date'].values
    direction = y_pred
    for i in range(n_row):
        if direction[i] == 0 and initial_position == 1:
            temp = str(date[i]) + ": Sell " + str(shares) + " Position"
            table.append(temp)
            initial_position = initial_position - 1
        elif direction[i] == 1 and initial_position == 0:
            temp = str(date[i]) + ": Buy " + str(shares) + " Position"
            table.append(temp)
            initial_position = initial_position + 1
    return table


# generate confusion matrix plot
def plot_confusion_matrix(features, the_pred):
    the_true = features["direction"].values
    # generate confusion matrix
    confusion_matrix = metrics.confusion_matrix(the_pred, the_true)
    # generate the plot
    plot_df = pd.DataFrame(confusion_matrix, index=["0", "1"], columns=["0", "1"])
    fig, ax = plt.subplots(figsize=(6, 5))
    sns.heatmap(plot_df, annot=True, cmap="YlGnBu", fmt="g", ax=ax)
    plt.xticks(rotation=30)
    plt.xlabel("True")
    plt.ylabel("Predicted")
    plt.title("ML Model Confusion Matrix")
    buffer = BytesIO()
    fig.savefig(buffer, bbox_inches="tight", transparent=True)
    plt.close()
    plot_data = buffer.getvalue()
    imb = base64.b64encode(plot_data)
    ims = imb.decode()
    imd = "data:image/png;base64," + ims

    return imd
