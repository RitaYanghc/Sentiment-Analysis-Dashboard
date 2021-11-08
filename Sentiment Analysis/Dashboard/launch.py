import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
import plotly.express as px
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objects as go
import glob
import dash_table as dtab
#from apps import senti_map
#from app import app
#from app import server
#from apps import home
#import senti_map

app = dash.Dash(__name__,suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.SKETCHY])
#server = app.server

# styling the sidebar
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

# padding for the page content
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

sidebar = html.Div(
    [
        html.H4("Sidebar", className="display-4"),
        html.Hr(),
        #html.P(
            #"Number of students per education level", className="lead"
        #),
        dbc.Nav(
            [
                dbc.NavLink("Home", href="/home", active="exact"),
                dbc.NavLink("World Sentiment Map", href="/senti_map", active="exact"),
                dbc.NavLink("Hashtag_Sentiment", href="/hashtag", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

content = html.Div(id="page-content", children=[], style=CONTENT_STYLE)

app.layout = html.Div([
    dcc.Location(id="url"),
    sidebar,
    content
])


layout_1 = dbc.Container([
     dbc.Row(
        dbc.Col([html.H1("Social Media COVID-19 Sentiment Analysis",
                        className='text-center text-info mb-4'),
                html.Hr(className='mb-4'),
                ],
                width=12),
         className="h-10",
    ),
     dbc.Row(
        dbc.Col([
            html.H6("Select Sentiment:",
                   style={"textDecoration": "underline"}),
            dcc.Dropdown(
                    id = "my-dropdown",
                    options=[
                            {'label': 'Positive', 'value': "pos"},
                            {'label': 'Negative', 'value': "neg"},
                            {'label': 'Neutral', 'value': "neu"}
                        ],
                    value='pos'
                ),            
        ], width={'size':5, 'offset':1},
        ),
        className="h-5",
     ),
     dbc.Row(
         dbc.Col(
            dcc.Graph(id="sentiment_over_time", figure={}),
            width = 12),
         className="h-45",
     ),
     dbc.Row([
         dbc.Col(
            html.H5("Topic Cloud of this sentiment"),
            width={'size':4, 'offset':1, 'order':1}
         ),
         dbc.Col(
             html.H5("Bigrams of this sentiment"),
             width={'size':3, 'offset':4, 'order':2}
         )
     ],
     className="h-10",
     ),
     dbc.Row([
        html.Hr(),
        dbc.Col(
           #dcc.Graph(id="topic_graph",figure={}),
           html.Img(id="topic_graph", style={'height':'95%', 'width':'100%'}),
           width={'size':8, 'offset':0, 'order':1}
        ),
        dbc.Col(
           html.Div(id="bigram_table"),
           width={'size':4, 'offset':0, 'order':2}
        )
     ],
     className="h-30",)
  ],
   style={"height": "100vh"},
   fluid=True
)

df = pd.read_csv('/Users/feng/Dashboard/datasets/time_series.csv')
import pandas as pd
df_pos = pd.read_csv('/Users/feng/Dashboard/datasets/grams/pos_bigram.csv')
df_pos = df_pos.drop(axis=1,columns='Unnamed: 0')
df_neu = pd.read_csv('/Users/feng/Dashboard/datasets/grams/neu_bigram.csv')
df_neu = df_neu.drop(axis=1,columns='Unnamed: 0')
df_neg = pd.read_csv('/Users/feng/Dashboard/datasets/grams/neg_bigram.csv')
df_neg = df_neg.drop(axis=1,columns='Unnamed: 0')
#Output("topic_graph",'figure'),
#Output("bigram_table",'children')
#app.get_asset_url('my-image.png')
@app.callback(
    [Output(component_id="sentiment_over_time",component_property="figure"),
    Output("bigram_table","children"),
    Output("topic_graph","src")],
    [Input(component_id="my-dropdown",component_property="value")]
)
def update_graph(sentiment):
   if(sentiment=="pos"):
      figure = go.Figure(
            data = [go.Scatter(
               x=df['date'],
               y=df['pos_density'],
               mode='lines',
               line_color='#FF0000')
               ]
      )
      figure.update_layout(
         title_text="Positive Sentiment Density Over Time",
         title_font={'color':'#FF0000'},
         title_xanchor="center",
         title_x=0.7,
         xaxis_title="Date",
         yaxis_title="Positive Density",
         title_font_size=20,
       )
      table = dbc.Table.from_dataframe(df_pos)
      src = app.get_asset_url('positive.png')
      #src = app.get_asset_url('/Users/feng/Dashboard/datasets/positive.png')
   elif(sentiment=="neg"):
      figure = go.Figure(
            data = [go.Scatter(
               x=df['date'],
               y=df['neg_density'],

               mode='lines',
               line_color='#0000FF')
               ]
      )
      figure.update_layout(
         title_text="Negative Sentiment Density Over Time",
         title_font={'color':'#0000FF'},
         title_xanchor="center",
         title_x=0.7,
         xaxis_title="Date",
         yaxis_title="Negtive Density",
         title_font_size=20,
       )
      table = dbc.Table.from_dataframe(df_neg)
      src = app.get_asset_url('negative.png')
   else:
      figure = go.Figure(
            data = [go.Scatter(
               x=df['date'],
               y=df['neu_density'],
               mode='lines',
               line_color='#808000')
               ]
      )
      figure.update_layout(
         title_text="Neutral Sentiment Density Over Time",
         title_font={'color':'#808000'},
         title_xanchor="center",
         title_x=0.7,
         xaxis_title="Date",
         yaxis_title="Neutral Density",
         title_font_size=20,
       )
      table = dbc.Table.from_dataframe(df_neu)
      src = app.get_asset_url('neutral.png')
   return figure, table,src
   


layout_2 = dbc.Container([
    dbc.Row(
        dbc.Col([html.H1("World Sentiment Map",
                        className='text-center text-info mb-4'),
                html.Hr(className='mb-4'),
                ],
                width=12),
         className="h-5",
    ), #width={'size':11, 'offset':1}
    dbc.Row(
        dbc.Col([
            dcc.Slider(id="selected_month",
                 min=0,
                 max=11,
                 marks={
                     0:{'label': 'Mar.20', 'style': {'color': '#77b0b1'}},
                     1:{'label': 'Apr.20', 'style': {'color': '#77b0b1'}},
                     2:{'label': 'May.20', 'style': {'color': '#77b0b1'}},
                     3:{'label': 'Jun.20', 'style': {'color': '#77b0b1'}},
                     4:{'label': 'Jul.20', 'style': {'color': '#77b0b1'}},
                     5:{'label': 'Aug.20', 'style': {'color': '#77b0b1'}},
                     6:{'label': 'Sep.20', 'style': {'color': '#77b0b1'}},
                     7:{'label': 'Oct.20', 'style': {'color': '#77b0b1'}},
                     8:{'label': 'Nov.20', 'style': {'color': '#77b0b1'}},
                     9:{'label': 'Dec.20', 'style': {'color': '#77b0b1'}},
                     10:{'label': 'Jan.21', 'style': {'color': '#77b0b1'}},
                     11:{'label': 'Feb.21', 'style': {'color': '#77b0b1'}}
                 },
                 value=0
                 ),
            dcc.Graph(id='world_map', figure={})
        ],
        width={'size':12, 'offset':0}
        ),
        className="h-40",
    ),
    dbc.Row([
        dbc.Col(
            dcc.Dropdown(
                    id = "tweet_dropdown",
                    options=[
                            {'label': 'US', 'value': 'United States',},
                            {'label': 'UK', 'value': 'United Kingdom'},
                            {'label': 'India', 'value': 'India'},
                            {'label': 'Nigeria', 'value': 'Nigeria'},
                            {'label': 'Australia', 'value': 'Australia'},
                        ],
                    value='United Kingdom'
                ), 
            width={'size':3, 'offset':1}
        ),
        dbc.Col([
            html.H4("Tweets From Different Countries"),
            html.Hr()
        ],
        width={'size':7, 'offset':1}
        )
    ],
        className="h-10", 
    ),
    dbc.Row(
        dbc.Col(
            html.Div(id="tweets_table"),
            width={'size':11,'offset':1}
        ), 
        className="h-30",  
    )
],
style={"height": "100vh"},
fluid=True
)
    


country_path = "/Users/feng/Dashboard/datasets/Country/*.csv"
country_list = sorted(glob.glob(country_path))
list_1 = country_list[3:10]
list_2 = country_list[0:3]
list_3 = country_list[10:]
country_list= list_1+list_2+list_3

tweet_path = "/Users/feng/Dashboard/datasets/Country_Tweets/*.csv"
tweet_list = sorted(glob.glob(tweet_path))
tlist_1 = tweet_list[3:10]
tlist_2 = tweet_list[0:3]
tlist_3 = tweet_list[10:]
tweet_list= tlist_1+tlist_2+tlist_3

country_name = ['United States','United Kingdom','India','Nigeria','Australia']

@app.callback(
    [Output('world_map','figure'),
    Output("tweets_table","children")],
    [Input('selected_month','value'),
     Input("tweet_dropdown","value")]
)
def update_map(month,ctry):
    tw_df = pd.read_csv(tweet_list[month])
    idx = country_name.index(ctry)
    ctry_df = pd.DataFrame()
    ctry_df['tweets'] = tw_df[country_name[idx]+"_tweets"]
    ctry_df['Sentiment'] = tw_df[country_name[idx]+"_sentiment"]

    map_df = pd.read_csv(country_list[month])
    map_figure = go.Figure(
         data = [go.Choropleth(locations=map_df['country'],
                          z=map_df['target'],
                          locationmode = 'country names',
                          text=map_df['country'],
                          colorscale = "RdBu",
                          autocolorscale=False,
                          reversescale=True,
                          colorbar_title="Sentiment Density")]
    )
    map_figure.update_layout(
         title_text="World Sentiment Map",
         title_font={'color': '#7FDBFF'},
         title_xanchor="center",
         font_family="Courier New",
         title_font_family="Times New Roman",
         title_font_color= '#7FDBFF',
         title_x=0.7,
         title_font_size=20,
         height=600,
         #paper_bgcolor=colors['background'],
    )
    return map_figure,dbc.Table.from_dataframe(ctry_df)

df_vac = pd.read_csv('/Users/feng/Dashboard/datasets/vaccine_result.csv')
vac_figure = go.Figure(
                        data = [go.Bar(
                            x=df_vac['Vaccine_Name'],
                            y=df_vac['Positive'],
                            width=0.3,
                            name='positive',
                            marker=dict(color='#FFD700')
                                ),
                                go.Bar(
                            x=df_vac['Vaccine_Name'],
                            y=df_vac['Negative'],
                            width=0.3,
                            name='negative',
                            marker=dict(color='#0000FF')
                                ),
                                go.Bar(
                            x=df_vac['Vaccine_Name'],
                            y=df_vac['Neutral'],
                            width=0.3,
                            name='neutral',
                            marker=dict(color='#808080')
                                )
                            ]
                        )
vac_figure.update_layout(
         #title_text="Vaccines Sentiment",
         #title_font={'color':colors['text']},
         title_xanchor="center",
         #font_family="Courier New",
         #font_color=colors['text'],
         font_size=15,
         legend_title_font_color="green",
         title_font_family="Times New Roman",
         #title_font_color=colors['text'],
         title_x=0.7,
         title_font_size=20,
         height=600,
         barmode='stack',
         #paper_bgcolor=colors['background'],
    )

layout_3 = dbc.Container([
     dbc.Row(
        dbc.Col([html.H1("Vaccine Sentiment",
                        className='text-center text-info mb-4'),
                html.Hr(className='mb-4'),
                ],
                width=12),
         className="h-10",
    ), 
    dbc.Row(
        dbc.Col(
            dcc.Graph(id='stacked_bar',figure=vac_figure),
            width=12
        ),
        className="h-70",
    ),
],
style={"height": "100vh"},
fluid=True
)






@app.callback(
    Output("page-content", "children"),
    [Input("url", "pathname")]
)
def render_page_content(pathname):
    if pathname == "/home":
        return layout_1
    elif pathname == "/senti_map":
        return layout_2
    elif pathname == "/hashtag":
        return layout_3
    # If the user tries to reach a different page, return a 404 message
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
    )



if __name__=='__main__':
    app.run_server(debug=True, port=3000)