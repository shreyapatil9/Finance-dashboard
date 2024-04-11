import dash
from dash import dcc, html, Input, Output
from datetime import date
from server import fetch_update_graph

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
        value='AAPL',  # Default selected stock
        style={'width':'40%','display':'inline-block'}
    ),

    

    # Date picker
    dcc.DatePickerRange(
        id='date-picker',
        min_date_allowed=date(2014, 4, 11),
        max_date_allowed=date(2024, 4, 11),
        initial_visible_month=date(2024, 4, 11),
        end_date=date.today(),
        start_date=date(2024,1,1),
        style={'width':'40%','display':'inline-block'}
    ),
    # Graph to display stock prices
    dcc.Graph(id='stock-graph')
],style={'font-family':'Arial'})

# Callback to update the graph based on selected stock and date range
@app.callback(
    Output('stock-graph', 'figure'),
    [Input('stock-dropdown', 'value'),
     Input('date-picker', 'start_date'),
     Input('date-picker', 'end_date')]
)
def update_graph(selected_stock, start_date, end_date):
    return fetch_update_graph(selected_stock, start_date, end_date)
if __name__ == '__main__':
    app.run_server(debug=True)
