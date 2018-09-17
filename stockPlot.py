import matplotlib.pyplot as plt
from alpha_vantage.timeseries import TimeSeries

def plotStock(ticker):
    ts = TimeSeries(key='TQ7BPG6XJANGKSNS', output_format='pandas')
    data, meta_data = ts.get_daily(symbol=ticker, outputsize='full')
    data = data.tail(30)
    data['4. close'].plot()
    plt.title('30 Day - {} stock'.format(ticker))
    plt.savefig('static/img/temp.png')