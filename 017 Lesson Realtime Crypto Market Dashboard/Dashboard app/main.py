import dash
import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objects as go
import pandas as pd
from dash.dependencies import Input, Output
import requests
import json


# Initialize the app
app = dash.Dash(__name__)
#app.config.suppress_callback_exceptions = True


apikey = 'enter your API KEY GET IT FROM https://www.coinapi.io/'



##################################################################################################################
############################################  Layout #############################################################
##################################################################################################################



app.layout = html.Div(children=[




##########################################header##########################################

    html.Div([

        # Logo Div
        html.Div([
            # image
            html.Img(src=app.get_asset_url('btc.png'), id='ads-image', style={
                'height': '60px',
                'width': 'auto',
                'margin-bottom': '25px'
            })

        ], className='one-third column'),

        # ads heading   DIV
        html.Div([
            # heading
            html.Div([
                html.H3('Africa Data School ', style={'margin-bottom': '0px', 'color': 'white'}),
                html.H5('Cryptocurrency Prices', style={'margin-bottom': '0px', 'color': 'white'})
            ])

        ], className='one-half column', id='title'),

        # date

        html.Div([


        ], className='one-third column', id='title1')

    ], id='header', className='row flex-display', style={'margin-bottom': '25px'}),



####################################################  SELECTORS #########################################################

html.Div([

# select Crypto Asset
html.Div([

    html.Label('Crypto Asset'),
    dcc.Dropdown(
        id='coin',
        options=[
            {'label': 'Bitcoin', 'value': 'BTC'},
            {'label': 'Ethereum', 'value': 'ETH'},
            {'label': 'Bitcoin Cash', 'value': 'BCH'},
            {'label': 'Litecoin', 'value': 'LTC'}
        ],
        value='BTC'
    ),

], className='card_container three columns'),

####### select  Time
html.Div([

    html.Label('Time'),
    dcc.Dropdown(
        id='time',
        options=[
            {'label': 'Minute', 'value': '1MIN'},
            {'label': 'Day', 'value': '10DAY'},
            {'label': 'Month', 'value': '6MTH'},
            {'label': 'year', 'value': '5YRS'}
        ],
        value='10DAY'
    ),

    dcc.Interval(
        id='graph-update',
        interval=1 * 1000,
        n_intervals=0
    ),

], className='card_container three columns'),

], className='row flex display'),


#########################################################  TODAY PRICES CARD  ############################################

    html.Div([
        # Revenue card div
        html.Div([
            html.H6(children='Price open',
                    style={'textAlign': 'center',
                           'color': 'white'}),
            html.P(id='price_open',
                   style={'textAlign': 'center',
                          'color': 'orange',
                          'fontSize': 40}),

        ], className='card_container three columns'),

        # Number of students
        html.Div([
            html.H6(children='Price close',
                    style={'textAlign': 'center',
                           'color': 'white'}),
            html.P(id='price_close',
                   style={'textAlign': 'center',
                          'color': 'orange',
                          'fontSize': 40}),

        ], className='card_container three columns'),

        # Average revenue per student
        html.Div([
            html.H6(children='Price High',
                    style={'textAlign': 'center',
                           'color': 'white'}),
            html.P(id='price_high',
                   style={'textAlign': 'center',
                          'color': 'orange',
                          'fontSize': 40}),

        ], className='card_container three columns'),

        # number of countries
        html.Div([
            html.H6(children='Volume_traded',
                    style={'textAlign': 'center',
                           'color': 'white'}),
            html.P(id='Volume_traded',
                   style={'textAlign': 'center',
                          'color': 'orange',
                          'fontSize': 40}),

        ], className='card_container three columns')

    ], className='row flex display'),


 ##################################################  cANDLE CHART #####################################################

html.Div([

    html.Div([

    dcc.Graph(id='graph',config={'displayModeBar': False}),

    ], className='card_container twelve columns')



], className='row flex display'),







],id = 'mainContainer', style={'display': 'flex', 'flex-direction': 'column'})





##################################################################################################################
############################################  Callbacks  #############################################################
##################################################################################################################


###  Price  open
@app.callback(Output('price_open', 'children'),
              [
               Input('coin', 'value'),
               Input('time', 'value'),


               ])
def update_graph(currency, time_change, apikey=apikey):

    url = f'https://rest.coinapi.io/v1/ohlcv/{currency}/USD/latest?period_id={time_change}'


    headers = {'X-CoinAPI-Key': apikey}
    response = requests.get(url, headers=headers)
    data = json.loads(response.text)
    df = pd.DataFrame(data)
    price_open=df['price_open'][0]

    return   price_open



#  Price close
@app.callback(Output('price_close', 'children'),
              [
               Input('coin', 'value'),
               Input('time', 'value'),


               ])
def update_graph(currency,time_change,apikey=apikey):

    url = f'https://rest.coinapi.io/v1/ohlcv/{currency}/USD/latest?period_id={time_change}'


    headers = {'X-CoinAPI-Key': apikey}
    response = requests.get(url, headers=headers)
    data = json.loads(response.text)
    df = pd.DataFrame(data)
    price_close=df['price_close'][0]

    return price_close





#  Price High
@app.callback(Output('price_high', 'children'),
              [
               Input('coin', 'value'),
               Input('time', 'value'),
               ])
def update_graph(currency,time_change,apikey=apikey):

    url = f'https://rest.coinapi.io/v1/ohlcv/{currency}/USD/latest?period_id={time_change}'


    headers = {'X-CoinAPI-Key': apikey}
    response = requests.get(url, headers=headers)
    data = json.loads(response.text)
    df = pd.DataFrame(data)
    price_high=df['price_high'][0]
    return   price_high




#  Volume Traded
@app.callback(Output('Volume_traded', 'children'),
              [
               Input('coin', 'value'),
               Input('time', 'value'),
               ])
def update_graph(currency,time_change,apikey=apikey):

    url = f'https://rest.coinapi.io/v1/ohlcv/{currency}/USD/latest?period_id={time_change}'


    headers = {'X-CoinAPI-Key': apikey}
    response = requests.get(url, headers=headers)
    data = json.loads(response.text)
    df = pd.DataFrame(data)
    Volume_traded=df['volume_traded'][0]
    return  Volume_traded



# Candle Stick chart

@app.callback(
    Output('graph', 'figure'),
    [   Input('coin', 'value'),
        Input('time', 'value'),

     ]
)
def update_figure(currency,time_change,apikey=apikey):

    url = f'https://rest.coinapi.io/v1/ohlcv/{currency}/USD/latest?period_id={time_change}'

    headers = {'X-CoinAPI-Key': apikey}
    response = requests.get(url, headers=headers)
    data = json.loads(response.text)
    df = pd.DataFrame(data)

    fig = go.Figure(data=[go.Candlestick(x=df.time_period_start,
                                         open=df.price_open,
                                         high=df.price_high,
                                         low=df.price_low,
                                         close=df.price_close, )],

                    #   layout= go.Layout(
                    #     paper_bgcolor='rgba(0,0,0,0)',
                    #     plot_bgcolor='rgba(0,0,0,0)'
                    # )

                    )

    fig.update_layout( colorway=["#5E0DAC", '#FF4F00', '#375CB1', '#FF7400', '#FFF400', '#FF0056'],
                  template='plotly_dark',
                  paper_bgcolor='rgba(0, 0, 0, 0)',
                  plot_bgcolor='rgba(0, 0, 0, 0)',
                  margin={'b': 15},
                  hovermode='x',
                  autosize=True,
                  title={'text': 'Cryptocurrency Prices', 'font': {'color': 'white'}, 'x': 0.5},)



    return fig




if __name__ == '__main__':
    app.run_server(debug=True,port=806)