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
import time
# from .layout import html_layout
# from .Dash_fun import apply_layout_with_auth, load_object, save_object


# url_base = 'dash/app1/'
url_base = '/plotlydash/'

# image_directory =  os.getcwd() + '/data/'

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

def create_dashboard(server):
    dash_app = dash.Dash(
        server=server,
        routes_pathname_prefix=url_base,
        external_stylesheets=external_stylesheets
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
                html.Div([
                    html.H3("Look-back Period"),
                    dcc.Slider(
                        id='lookback-slider',
                        min=50,
                        max=300,
                        value=200,
                        marks={
                            50: {'label': '50 days'},
                            100: {'label': '100 days'},
                            150: {'label': '150 days'},
                            200: {'label': '200 days'},
                            250: {'label': '250 days'},
                            300: {'label': '300 days'}
                        }
                      # marks={
                        # str(days): str(days) for days in [50, 100, 150, 200, 250, 300]
                        # },
                                            )
                    

                ], style={"width": "50%", "display": "inline-block"} # "padding": "15px"
                ),

                html.Div([

                    html.Div([
                        dcc.Loading(
                            type="dot", # 'graph', 'cube', 'circle', 'dot', 'default'
                            id="heatmap-loader-1",
                            children=[
                                html.Div(id="loading-output-1", 
                                    children=[]
                                )
                            ],
                        )
                    ], style={
                        "margin-top": "3%",
                        # "border":"2px black solid",
                        "width": "20%",
                        "display": "inline-block",
                        "vertical-align": "top"
                        }
                    ),

                    html.Div([
                        dcc.Loading(
                            type="dot", # 'graph', 'cube', 'circle', 'dot', 'default'
                            id="heatmap-loader-2",
                            children=[
                                html.Div(id="loading-output-2", 
                                    children=[]
                                )
                            ],
                        )
                    ], style={
                        "margin-top": "3%",
                        # "border":"2px black solid",
                        "width": "33%",
                        "display": "inline-block",
                        "vertical-align": "top"

                        }
                    ),

                    html.Div([
                        dcc.Loading(
                            type="dot", # 'graph', 'cube', 'circle', 'dot', 'default'
                            id="heatmap-loader-3",
                            children=[
                                html.Div(id="loading-output-3", 
                                    children=[]
                                )
                            ],
                        )
                    ], style={
                        "margin-top": "3%",
                        # "border":"2px black solid",
                        "width": "35%",
                        "display": "inline-block",
                        "vertical-align": "top"

                        }
                    ),

                    # # keep this for working example
                    # html.Div(
                    #     id='image-div', children=[]
                    # ),
            ]),
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



    @dash_app.callback(
        [Output("loading-output-1", "children"),
        Output("loading-output-2", "children"),
        Output("loading-output-3", "children")],
        [Input("lookback-slider", "value")])

    def return_image(lookback):

        ccy = [
            'GBP=X', 'EUR=X', 'NZD=X', 'CHF=X', 'JPY=X', 'AUD=X', 'CAD=X',
            'CZK=X', 'HUF=X', 'ZAR=X', 'MXN=X', 'PLN=X', 'TRY=X', 'RUB=X',
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

        # allccy_table, allccy_labels = return_heatmap_data([df_g10, df_otherg10, df_EM], rows=6, columns=11)
        g10_table, g10_labels = return_heatmap_data([df_g10], rows=3, columns=3)
        otherg10_table, otherg10_labels = return_heatmap_data([df_otherg10], rows=6, columns=6)
        em_table, em_labels = return_heatmap_data([df_EM], rows=3, columns=7)

        g10_encoded_image = create_heatmap(g10_table, g10_labels, 
            theme="RdBu", lookback=lookback)
        g10_decoded_image = html.Img(src='data:image/png;base64,{}'\
            .format(g10_encoded_image.decode()), 
                style={
                    # "height": "600px"
                    })

        otherg10_encoded_image = create_heatmap(otherg10_table, otherg10_labels,
            theme="RdBu", lookback=lookback)
        otherg10_decoded_image = html.Img(src='data:image/png;base64,{}'\
            .format(otherg10_encoded_image.decode()), 
                style={
                    # "height": "600px"
                    })

        em_encoded_image = create_heatmap(em_table, em_labels,
            theme="RdBu", lookback=lookback)
        em_decoded_image = html.Img(src='data:image/png;base64,{}'\
            .format(em_encoded_image.decode()), 
                style={
                    # "height": "600px"
                    })


        # encoded_image = base64.b64encode(
        #     open("recordcurrency/static/images/ONFXRTN_all.png", 'rb').read())



        return g10_decoded_image, otherg10_decoded_image, em_decoded_image





    # # keep this for working example
    # @dash_app.callback(Output('image-div', 'children'),
    #     [Input(component_id='lookback-slider',component_property='value')
    #     ]
    # )

    # def update_image(lookback):

    #     ccy = [
    #         'GBP=X', 'EUR=X', 'NZD=X', 'CHF=X', 'JPY=X', 'AUD=X', 'CAD=X',
    #         'CZK=X', 'HUF=X', 'ZAR=X', 'MXN=X', 'PLN=X', 'TRY=X', 'RUB=X',
    #         'BRL=X', 'COP=X', 'CLP=X', 'PEN=X', 'RON=X',  'TWD=X', 'THB=X',
    #         'IDR=X', 'INR=X', 'HKD=X', 'SGD=X', 'CNH=X', 'CNY=X', 'PHP=X', 
    #         'MYR=X', 'KRW=X', 'DKK=X', 'SEK=X', 'NOK=X'
    #     ]

    #     ccys_to_inverse = [
    #         'USD/EUR', 'USD/GBP', 'USD/AUD', 'USD/NZD', 'GBP/EUR', 'NZD/AUD',
    #         'CHF/AUD', 'JPY/AUD', 'CHF/CAD', 'SEK/NOK', 'JPY/NOK', 'JPY/SEK',
    #         'JPY/CAD'
    #     ]

    #     # define currency groups
    #     G10vUSD = [
    #         'EURUSD', 'USDJPY', 'GBPUSD', 'USDCHF', 'AUDUSD', 'USDCAD',
    #         'NZDUSD', 'USDNOK', 'USDSEK'
    #     ]

    #     otherG10 = [
    #         'EURGBP', 'EURAUD', 'EURNZD', 'EURCAD', 'EURCHF', 'EURNOK', 
    #         'EURSEK', 'EURJPY', 'GBPAUD', 'GBPNZD', 'GBPCAD', 'GBPCHF',
    #         'GBPNOK', 'GBPSEK', 'GBPJPY', 'AUDNZD', 'AUDCAD', 'AUDCHF',
    #         'AUDNOK', 'AUDSEK', 'AUDJPY', 'NZDCAD', 'NZDCHF', 'NZDNOK',
    #         'NZDSEK', 'NZDJPY', 'CADCHF', 'CADNOK', 'CADSEK', 'CADJPY',
    #         'CHFNOK', 'CHFSEK', 'CHFJPY', 'NOKSEK',  'NOKJPY', 'SEKJPY'
    #         ]

    #     EMvsUSD = [
    #         'USDBRL', 'USDCLP', 'USDCNH', 'USDCNY', 'USDCOP', 'USDCZK',
    #         'USDHUF', 'USDIDR', 'USDINR', 'USDKRW', 'USDMXN', 'USDMYR',
    #         'USDPEN', 'USDPHP', 'USDPLN', 'USDRON', 'USDRUB', 'USDTRY',
    #         'USDTWD', 'USDZAR', 'USDTHB'
    #     ]

    #     start = datetime.datetime.now() - relativedelta(days=lookback)
    #     end = datetime.datetime.now()


    #     df = get_ccy_data(start, end, ccy).interpolate()
    #     df = calculate_crosses(df)
    #     df = inverse_currencies(df=df, currencies=ccys_to_inverse)

    #     df_g10 = return_bar_data(df, ccy_group=G10vUSD)
    #     df_otherg10 = return_bar_data(df, ccy_group=otherG10)
    #     df_EM = return_bar_data(df, ccy_group=EMvsUSD)

    #     allccy_table, allccy_labels = return_heatmap_data([df_g10, df_otherg10, df_EM], rows=6, columns=11)

    #     print(allccy_table)

    #     encoded_image = create_heatmap(allccy_table, allccy_labels, theme="RdBu", output_name="ONFXRTN_all", lookback=lookback)

    #     # encoded_image = base64.b64encode(
    #     #     open("recordcurrency/static/images/ONFXRTN_all.png", 'rb').read())



    #     return html.Img(src='data:image/png;base64,{}'\
    #         .format(encoded_image.decode()), style={"height": "600px"})




    # dash_app.config.update({'requests_pathname_prefix': '/recordcurrency/'})

    # dash_app.css.config.serve_locally = True
    # dash_app.scripts.config.serve_locally = True

    return dash_app.server




# app = dash.Dash(
#     __name__,
#     requests_pathname_prefix='/app1/'
# )

# app.layout = html.Div("Dash app 1") 