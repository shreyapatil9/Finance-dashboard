import plotly.graph_objs as go
import yfinance as yf

# Function to fetch stock data using Yahoo Finance API
def get_stock_data(symbol, start_date, end_date):
    stock = yf.download(symbol, start=start_date, end=end_date)
    return stock

def calculate_daily_change(stock_symbol, start_date, end_date):
    stock_data = get_stock_data(stock_symbol, start_date, end_date)
    close_prices = stock_data['Close']
    # Calculate absolute change in stock prices for each day
    daily_change = close_prices.diff()
    # Get the last available date and its corresponding daily change
    last_date = daily_change.index[-1]
    last_daily_change = daily_change[-1]
    return f'{stock_symbol}: {last_daily_change:.2f}'   

def fetch_update_graph(selected_stock, start_date, end_date):
    if start_date is not None and end_date is not None and selected_stock:
        traces = []
        for stock_symbol in selected_stock:
            stock_data = get_stock_data(stock_symbol, start_date, end_date)
            close_prices = stock_data['Close']
            # Calculate percentage change in stock prices
            #pct_change = (close_prices - close_prices.iloc[0]) / close_prices.iloc[0] * 100
            trace = go.Scatter(x=stock_data.index, y=close_prices, mode='lines', name=f'{stock_symbol} Price')
            traces.append(trace)
        layout = go.Layout(title='Stock Prices', xaxis={'title': 'Date'}, yaxis={'title': 'Price'})
        return {'data': traces, 'layout': layout}
    else:
        return {}