import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas as pd
import datetime
# Connect to main app.py file
from app import app
from app import server

# Connect to your app pages
from apps import senti_map


app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div([
        dcc.Link('World Sentiment Map', href='/apps/senti_map'),
        #dcc.Link('Other Products', href='/apps/global_sales'),
    ], className="row"),
    html.Div(id='page-content', children=[])
])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/apps/senti_map':
        return senti_map.layout
    #if pathname == '/apps/global_sales':
        #return global_sales.layout
    else:
        return "404 Page Error! Please choose a link"


if __name__ == '__main__':
    app.run_server(debug=False)