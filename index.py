from app import app
from app import server
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
from datetime import datetime
import dash_table
import pandas as pd
from PriceIndices import MarketHistory, Indices
history = MarketHistory()

colors = {
    'background': '#111111',
    'background2': '#FF0',
    'text': 'yellow'
}
coin_list = ['bitcoin', 'ethereum', 'ripple', 'bitcoin-cash']


app.layout = html.Div([html.H1('Crypto Price Graph',
                               style={
                                   'textAlign': 'center',
                                   "background": "yellow"}),
                       html.Div(['Date selector for graphs',
                                 dcc.DatePickerRange(
                                     id='date-input',
                                     stay_open_on_select=False,
                                     min_date_allowed=datetime(2013, 4, 28),
                                     max_date_allowed=datetime.now(),
                                     initial_visible_month=datetime.now(),
                                     start_date=datetime(2019, 1, 1),
                                     end_date=datetime.now(),
                                     number_of_months_shown=2,
                                     month_format='MMMM,YYYY',
                                     display_format='YYYY-MM-DD',
                                     style={
                                         'color': '#11ff3b',
                                         'font-size': '18px',
                                         'margin': 0,
                                         'padding': '8px',
                                         'background': 'yellow',
                                     }
                                 ),
                                 '-|- Select coin here',
                                 dcc.Dropdown(id='dropdown',
                                              options=[{'label': i, 'value': i} for i in coin_list],
                                              value='bitcoin',
                                              optionHeight=10,
                                              style={
                                                  'height': '50px',
                                                  'font-weight': 100,
                                                  'font-size': '16px',
                                                  'line-height': '10px',
                                                  'color': 'gray',
                                                  'margin': 0,
                                                  'padding': '8px',
                                                  'background': 'yellow',
                                                  'position': 'middle',
                                                  'display': 'inline-block',
                                                  'width': '150px',
                                                  'vertical-align': 'middle',
                                              }
                                              ),
                                 html.Div(id='date-output'),
                                 html.Div(id='intermediate-value', style={'display': 'none'}),
                                 ], className="row ",
                                style={'marginTop': 0, 'marginBottom': 0, 'font-size': 30, 'color': 'white',
                                       'display': 'inline-block'}),
                       html.Div(id='graph-output'),
                       html.Div(children=[html.H1(children="Data Table",
                                                  style={
                                                      'textAlign': 'center',
                                                      "background": "yellow"})
                                          ]
                                ),
                       html.Div(children=[html.Table(id='table'), html.Div(id='table-output')]),
                       html.Div(children=[dcc.Markdown(
                           " © 2019 [DCAICHARA](https://github.com/dc-aichara)  All Rights Reserved.")], style={
                           'textAlign': 'center',
                           "background": "yellow"}),
                       ],
                      style={"background": "#000080"}
                      )


@app.callback(Output('table-output', 'children'),
              [Input('dropdown', 'value')])
def get_data_table(option):
    df = history.get_price(option, '20130428', '20200510')  # Get Bitcoin price data
    df['date'] = pd.to_datetime(df['date'])
    data_table = dash_table.DataTable(
        id='datatable-data',
        data=df.to_dict('records'),
        columns=[{'id': c, 'name': c} for c in df.columns],
        style_table={'overflowY': 'scroll'},
        fixed_rows={'headers': True, 'data': 10},
        style_cell={'width': '100px'},
        style_header={
            'backgroundColor': 'rgb(230, 230, 230)',
            'fontWeight': 'bold'
        }
    )
    return data_table


@app.callback(Output('graph-output', 'children'),
              [Input('date-input', 'start_date'),
               Input('date-input', 'end_date'),
               Input('dropdown', 'value')])
def render_graph(start_date, end_date, option):
    df = history.get_price(option, '20130428', '20200510')  # Get Bitcoin price data
    df['date'] = pd.to_datetime(df['date'])
    data = df[(df.date >= start_date) & (df.date <= end_date)]
    return dcc.Graph(
        id='graph-1',
        figure={
            'data': [
                {'x': data['date'], 'y': data['price'], 'type': 'line', 'name': 'value1'},
            ],
            'layout': {
                'title': f'{option.capitalize()} Price Vs Time ',
                'plot_bgcolor': colors['background'],
                'paper_bgcolor': colors['background'],
                'font': {
                    'color': colors['text'],
                    'size': 18
                },
                'xaxis': {
                    'title': 'Time',
                    'showspikes': True,
                    'spikedash': 'dot',
                    'spikemode': 'across',
                    'spikesnap': 'cursor',
                },
                'yaxis': {
                    'title': 'Price',
                    'showspikes': True,
                    'spikedash': 'dot',
                    'spikemode': 'across',
                    'spikesnap': 'cursor'
                },

            }
        }
    )


if __name__ == '__main__':
    app.run_server(debug=True)