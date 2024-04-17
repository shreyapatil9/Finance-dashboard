import dash
from dash import dcc, html, Input, Output
from datetime import date
from server import fetch_update_graph
from server import calculate_daily_change
# Initial setup
app = dash.Dash(__name__)
app.title = 'Stock Market Dashboard'

# Custom CSS styling
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# Layout of the dashboard
app.layout = html.Div(style={'backgroundColor': '#f2f2f2', 'fontFamily': 'Arial, sans-serif'}, children=[
    html.H1('Stock Market Dashboard', style={'textAlign': 'center', 'color': '#1585E2', 'marginTop': '20px', 'marginBottom': '20px'}),

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
        multi=True, # Allow multiple stock selection
        style={'width': '50%', 'margin': 'auto', 'marginBottom': '20px'}
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
    html.Div(id='daily-change-text'),
    # Graph to display stock prices
    dcc.Graph(id='stock-graph')
])

# Callback to update the graph based on selected stock and date range
@app.callback(
    Output('stock-graph', 'figure'),
    [Input('stock-dropdown', 'value'),
     Input('date-picker', 'start_date'),
     Input('date-picker', 'end_date')]
)
def update_graph(selected_stock, start_date, end_date):   
    return fetch_update_graph(selected_stock, start_date, end_date)

@app.callback(
    Output('daily-change-text', 'children'),
    [Input('stock-dropdown', 'value'),
     Input('date-picker', 'start_date'),
     Input('date-picker', 'end_date')]
)
def update_daily_change_text(selected_stocks, start_date, end_date):
    if start_date is not None and end_date is not None:
        text = []
        if selected_stocks is not list:
            selected_stocks = [selected_stocks]
        for stock_symbol in selected_stocks:
            daily_change = calculate_daily_change(stock_symbol, start_date, end_date)
            color = 'green' if daily_change >= 0 else 'red'
            text.append(
                html.P([
                    f'{stock_symbol}: ', 
                    html.Span(f'{daily_change:.2f}', style={'color': color, 'marginLeft': '5px'})
                    ] , 
                    style={'display': 'inline', 'color': '#333333'}
                ))
        return text
    else:
        return ''   


if __name__ == '__main__':
    app.run_server(debug=True)

