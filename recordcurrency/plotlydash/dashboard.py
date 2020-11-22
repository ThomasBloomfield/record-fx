import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_table
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import base64
import os
from recordcurrency.functions import *
# from .layout import html_layout
# from .Dash_fun import apply_layout_with_auth, load_object, save_object


# url_base = 'dash/app1/'
url_base = '/plotlydash/'

# image_directory =  os.getcwd() + '/data/'

def create_dashboard(server):
    dash_app = dash.Dash(
        server=server,
        routes_pathname_prefix=url_base,
        # url_base_pathname=url_base
        )

    def serve_layout():
        """
        By default, Dash apps store the app.layout in memory. This ensures that the 
        layout is only computed once, when the app starts.

        If you set app.layout to a function, then you can serve a dynamic layout on
        every page load.
        """
        return html.Div([
                html.Div(
                    dcc.Slider(
                        id='lookback-slider',
                        min=50,
                        max=300,
                        value=200,
                        marks={
                        str(days): str(days) for days in [50, 100, 150, 200, 250, 300]
                        },
                        step=None
                    ),
                    

                ),




                    # dcc.Loading(id="loading-1",children=[html.Div(id= "loading-output-1")]),

                    
                    html.Div(
                        id='image-div', children=[]
                    ),

        ])


    dash_app.layout = serve_layout

    # apply_layout_with_auth(dash_app, layout) ###############

    # Custom HTML layout
    # dash_app.index_string = html_layout

    # external_stylesheets = [
    #         '/static/dist/css/styles.css',
    #         'https://fonts.googleapis.com/css?family=Lato'
    #     ]


    # @dash_app.callback(
    #     Output("loading-output-1", "children"),
    #     [Input('lookback-slider', 'value')])

    @dash_app.callback(Output('image-div', 'children'),
        [Input(component_id='lookback-slider',component_property='value')
        ]
    )


    def update_image(lookback):

        ccy = [
            'GBP=X', 'EUR=X', 'NZD=X', 'CHF=X', 'JPY=X', 'AUD=X', 'CAD=X',
            'CZK=X', 'HUF=X', 'ZAR=X',  'MXN=X', 'PLN=X', 'TRY=X', 'RUB=X',
            'BRL=X', 'COP=X', 'CLP=X', 'PEN=X', 'RON=X',  'TWD=X', 'THB=X',
            'IDR=X', 'INR=X', 'HKD=X', 'SGD=X', 'CNH=X', 'CNY=X', 'PHP=X', 
            'MYR=X', 'KRW=X', 'DKK=X', 'SEK=X', 'NOK=X'
        ]

        ccys_to_inverse = [
            'USD/EUR', 'USD/GBP', 'USD/AUD', 'USD/NZD', 'GBP/EUR', 'NZD/AUD',
            'CHF/AUD', 'JPY/AUD', 'CHF/CAD', 'SEK/NOK', 'JPY/NOK', 'JPY/SEK',
            'JPY/CAD'
        ]

        # define currency groups
        G10vUSD = [
            'EURUSD', 'USDJPY', 'GBPUSD', 'USDCHF', 'AUDUSD', 'USDCAD',
            'NZDUSD', 'USDNOK', 'USDSEK'
        ]

        otherG10 = [
            'EURGBP', 'EURAUD', 'EURNZD', 'EURCAD', 'EURCHF', 'EURNOK', 
            'EURSEK', 'EURJPY', 'GBPAUD', 'GBPNZD', 'GBPCAD', 'GBPCHF',
            'GBPNOK', 'GBPSEK', 'GBPJPY', 'AUDNZD', 'AUDCAD', 'AUDCHF',
            'AUDNOK', 'AUDSEK', 'AUDJPY', 'NZDCAD', 'NZDCHF', 'NZDNOK',
            'NZDSEK', 'NZDJPY', 'CADCHF', 'CADNOK', 'CADSEK', 'CADJPY',
            'CHFNOK', 'CHFSEK', 'CHFJPY', 'NOKSEK',  'NOKJPY', 'SEKJPY'
            ]

        EMvsUSD = [
            'USDBRL', 'USDCLP', 'USDCNH', 'USDCNY', 'USDCOP', 'USDCZK',
            'USDHUF', 'USDIDR', 'USDINR', 'USDKRW', 'USDMXN', 'USDMYR',
            'USDPEN', 'USDPHP', 'USDPLN', 'USDRON', 'USDRUB', 'USDTRY',
            'USDTWD', 'USDZAR', 'USDTHB'
        ]

        start = datetime.datetime.now() - relativedelta(days=lookback)
        end = datetime.datetime.now()


        df = get_ccy_data(start, end, ccy).interpolate()
        df = calculate_crosses(df)
        df = inverse_currencies(df=df, currencies=ccys_to_inverse)

        df_g10 = return_bar_data(df, ccy_group=G10vUSD)
        df_otherg10 = return_bar_data(df, ccy_group=otherG10)
        df_EM = return_bar_data(df, ccy_group=EMvsUSD)

        allccy_table, allccy_labels = return_heatmap_data([df_g10, df_otherg10, df_EM], rows=6, columns=11)

        print(allccy_table)

        encoded_image = create_heatmap(allccy_table, allccy_labels, theme="RdBu", output_name="ONFXRTN_all")

        # encoded_image = base64.b64encode(
        #     open("recordcurrency/static/images/ONFXRTN_all.png", 'rb').read())



        return html.Img(src='data:image/png;base64,{}'\
            .format(encoded_image.decode()), style={"height": "600px"})







    # dash_app.config.update({'requests_pathname_prefix': '/recordcurrency/'})

    # dash_app.css.config.serve_locally = True
    # dash_app.scripts.config.serve_locally = True

    return dash_app.server

# app = dash.Dash(
#     __name__,
#     requests_pathname_prefix='/app1/'
# )

# app.layout = html.Div("Dash app 1") 