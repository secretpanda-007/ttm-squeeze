import os, pandas
import plotly.graph_objects as go
dataframes = {}

for filename in os.listdir('datasets'):
    
    symbol = filename.split(".")[0]
    
    df = pandas.read_csv('datasets/{}'.format(filename))
    if df.empty:
        continue

    df['20sma'] = df['Close'].rolling(window=20).mean()
    df['50sma'] = df['Close'].rolling(window=50).mean()
    df['stddev'] = df['Close'].rolling(window=20).std()
    df['lower_band'] = df['20sma'] - (2 * df['stddev'])
    df['upper_band'] = df['20sma'] + (2 * df['stddev'])

    df['TR'] = abs(df['High'] - df['Low'])
    df['ATR'] = df['TR'].rolling(window=20).mean()

    df['lower_keltner'] = df['20sma'] - (df['ATR'] * 1.5)
    df['upper_keltner'] = df['20sma'] + (df['ATR'] * 1.5)
    df['volume'] = df['Volume'] / 1000000

    # save all dataframes to a dictionary
    dataframes[symbol] = df

stock = input("Enter the stock symbol : ")

def chart(df):
    candlestick = go.Candlestick(x=df['Date'], open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'], increasing_line_color= '#17becf', decreasing_line_color= '#e377c2')
    upper_band = go.Scatter(x=df['Date'], y=df['upper_band'], name='Upper Bollinger Band', line={'color': 'lightgreen'})
    lower_band = go.Scatter(x=df['Date'], y=df['lower_band'], name='Lower Bollinger Band', line={'color': 'lightgreen'})

    upper_keltner = go.Scatter(x=df['Date'], y=df['upper_keltner'], name='Upper Keltner Channel', line={'color': 'lightgray'})
    lower_keltner = go.Scatter(x=df['Date'], y=df['lower_keltner'], name='Lower Keltner Channel', line={'color': 'lightgray'})

    sma20 = df['20sma']
    sma50 = df['50sma']

    smaS = go.Scatter(x=df['Date'], y=sma20, name='SMA20', line={'color': 'blue'})
    smaD = go.Scatter(x=df['Date'], y=sma50, name='SMA50', line={'color': 'crimson'})


    
    fig = go.Figure(data=[candlestick, upper_band, lower_band, upper_keltner, lower_keltner, smaS, smaD])
    fig.update_layout(title='boogiePANDA Charts', yaxis_title= stock +' Stock')
    fig.layout.xaxis.type = 'category'
    fig.layout.xaxis.rangeslider.visible = False

    fig.show()

df = dataframes[stock]
chart(df)

