import plotly.graph_objs as go
import yfinance as yf

# Function to fetch stock data using Yahoo Finance API
def get_stock_data(symbol, start_date, end_date):
    stock = yf.download(symbol, start=start_date, end=end_date)
    return stock

def fetch_update_graph(selected_stock, start_date, end_date):
    if start_date is not None and end_date is not None:
        stock_data = get_stock_data(selected_stock, start_date, end_date)
        trace = go.Scatter(x=stock_data.index, y=stock_data['Close'], mode='lines', name='Close Price')
        layout = go.Layout(title=f'{selected_stock} Stock Price', xaxis={'title': 'Date'}, yaxis={'title': 'Price'})
        return {'data': [trace], 'layout': layout}
    else:
        return {}