import matplotlib.pyplot as plt
from alpha_vantage.timeseries import TimeSeries
from resources import apiKey

def plotStock(ticker):
    ts = TimeSeries(key=apiKey.timeSeries_Key, output_format='pandas')
    data, meta_data = ts.get_daily(symbol=ticker, outputsize='full')
    data = data.tail(30)
    data['4. close'].plot()
    plt.title('30 Day - {} stock'.format(ticker))
    plt.savefig('static/img/temp.png')