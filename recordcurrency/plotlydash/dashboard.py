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
# from .layout import html_layout
# from .Dash_fun import apply_layout_with_auth, load_object, save_object


# url_base = 'dash/app1/'
url_base = '/plotlydash/'


encoded_image = base64.b64encode(open("recordcurrency/static/images/ONFXRTN_all.png", 'rb').read())
# image_directory =  os.getcwd() + '/data/'

def create_dashboard(server):
    dash_app = dash.Dash(
        server=server,
        routes_pathname_prefix=url_base,
        # url_base_pathname=url_base
        )

    # apply_layout_with_auth(dash_app, layout) ###############

    # Custom HTML layout
    # dash_app.index_string = html_layout

    # external_stylesheets = [
    #         '/static/dist/css/styles.css',
    #         'https://fonts.googleapis.com/css?family=Lato'
    #     ]

  


    dash_app.layout = html.Div([

        html.Div([
            html.Img(
                src='data:image/png;base64,{}'.format(encoded_image.decode()), style={"height": "600px"}
            )
        ]),

	])

    # dash_app.config.update({'requests_pathname_prefix': '/recordcurrency/'})

    # dash_app.css.config.serve_locally = True
    # dash_app.scripts.config.serve_locally = True

    return dash_app.server

# app = dash.Dash(
#     __name__,
#     requests_pathname_prefix='/app1/'
# )

# app.layout = html.Div("Dash app 1") 