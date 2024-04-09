import dash
from dash import dcc, html, Input, Output
import plotly.graph_objs as go
import pandas as pd
import yfinance as yf

# Function to fetch stock data using Yahoo Finance API
def get_stock_data(symbol, start_date, end_date):
    stock = yf.download(symbol, start=start_date, end=end_date)
    return stock

# Initial setup
app = dash.Dash(__name__)
app.title = 'Stock Market Dashboard'

# Layout of the dashboard
app.layout = html.Div([
    html.H1('Stock Market Dashboard'),

    # Dropdown to select stock
    dcc.Dropdown(
        id='stock-dropdown',
        options=[
            {'label': 'Apple Inc. (AAPL)', 'value': 'AAPL'},
            {'label': 'Microsoft Corporation (MSFT)', 'value': 'MSFT'},
            {'label': 'Google LLC (GOOGL)', 'value': 'GOOGL'}
            # Add more stocks as needed
        ],
        value='AAPL'  # Default selected stock
    ),

    # Graph to display stock prices
    dcc.Graph(id='stock-graph'),

    # Date picker
    dcc.DatePickerRange(
        id='date-picker',
        start_date_placeholder_text="Start Date",
        end_date_placeholder_text="End Date",
        calendar_orientation='vertical'
    )
])

# Callback to update the graph based on selected stock and date range
@app.callback(
    Output('stock-graph', 'figure'),
    [Input('stock-dropdown', 'value'),
     Input('date-picker', 'start_date'),
     Input('date-picker', 'end_date')]
)
def update_graph(selected_stock, start_date, end_date):
    if start_date is not None and end_date is not None:
        stock_data = get_stock_data(selected_stock, start_date, end_date)
        trace = go.Scatter(x=stock_data.index, y=stock_data['Close'], mode='lines', name='Close Price')
        layout = go.Layout(title=f'{selected_stock} Stock Price', xaxis={'title': 'Date'}, yaxis={'title': 'Price'})
        return {'data': [trace], 'layout': layout}
    else:
        return {}

if __name__ == '__main__':
    app.run_server(debug=True)
