
# coding: utf-8

# In[ ]:


import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd

app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})

df = pd.read_csv('econ_indicators.csv')
df = df[~df['GEO'].isin(['European Union (current composition)',
        'European Union (without United Kingdom)',
        'European Union (15 countries)',
        'Euro area (EA11-2000, EA12-2006, EA13-2007, EA15-2008, EA16-2010, EA17-2013, EA18-2014, EA19)',
        'Euro area (19 countries)',
        'Euro area (12 countries)'])]
df = df[df.Value != ':']

app = dash.Dash(__name__)
server = app.server

available_indicators = df['NA_ITEM'].unique()
available_units = df['UNIT'].unique()
available_countries = df['GEO'].unique()

app.layout = html.Div([
    html.H1(children='Economic Indicators in European Countries', 
               style={'textAlign': 'center'}),
    html.H2(children='Interactive Graph 1', 
               style={'textAlign': 'center', 'padding-top':10}),
    html.Div([

        html.Div([
            html.Label('Select indicator (x-axis):'),
            dcc.Dropdown(
                id='xaxis-column',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Wages and salaries' 
            )
        ],
        style={'width': '48%', 'display': 'inline-block', 'padding-top':10, 'padding-bottom':20}),

        html.Div([
            html.Label('Select indicator (y-axis):'),
            dcc.Dropdown(
                id='yaxis-column',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Gross domestic product at market prices'
            )
        ],style={'width': '48%', 'float': 'right', 'display': 'inline-block', 'padding-top':10, 'padding-bottom':20})
    ]),
    
    html.Div([
        html.Label('Select unit:', 
                   style={'width':'100%','display':'inline-block','textAlign':'center'}),
        dcc.RadioItems(
            id='unit_selection',
            options=[{'label': i, 'value': i} for i in available_units],
            value='Current prices, million euro',
            labelStyle={'display': 'inline-block',},
        style={'textAlign':'center'})
    ]),
        
    dcc.Graph(id='indicator-graphic'),

    html.Label('Select year:'),
    dcc.Slider(
        id='TIME--slider',
        min=df['TIME'].min(),
        max=df['TIME'].max(),
        value=df['TIME'].max(),
        step=None,
        marks={str(TIME): str(TIME) for TIME in df['TIME'].unique()}
    ),
    
    html.Div([
        
        html.H2(children='Interactive Graph 2',
                style={'textAlign': 'center', 'padding-top':100}),
        html.Div([
            html.Label('Select country:'),
            dcc.Dropdown(
                id='country_choice',
                options=[{'label': i, 'value': i} for i in available_countries],
                value='Belgium' 
            ),
        ],
        style={'width': '48%', 'display': 'inline-block', 'padding-top':10, 'padding-bottom':20}),

        html.Div([
            html.Label('Select indicator: '),
            dcc.Dropdown(
                id='yaxis',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Gross domestic product at market prices'
            )
        ],style={'width': '48%', 'float': 'right', 'display': 'inline-block', 'padding-top':10, 'padding-bottom':20})
    ]),

    html.Div([
        html.Label('Select unit:', 
                   style={'width':'100%','display':'inline-block','textAlign':'center'}),
        dcc.RadioItems(
            id='unit_selection2',
            options=[{'label': i, 'value': i} for i in available_units],
            value='Current prices, million euro',
            labelStyle={'display': 'inline-block'},
        style={'textAlign':'center'})
    ]),
        
    dcc.Graph(id='country-graphic'),

])


@app.callback(
    dash.dependencies.Output('indicator-graphic', 'figure'),
     [dash.dependencies.Input('xaxis-column', 'value'),
      dash.dependencies.Input('yaxis-column', 'value'),
     dash.dependencies.Input('unit_selection', 'value'),
     dash.dependencies.Input('TIME--slider', 'value')])

def update_graph(xaxis_column_name, yaxis_column_name,
                 select_unit, year_value):
    dff = df[df['TIME'] == year_value]
    dfn = dff[dff['UNIT'] == select_unit]
    return {
        'data': [go.Scatter(
            x=dfn[dfn['NA_ITEM'] == xaxis_column_name]['Value'],
            y=dfn[dfn['NA_ITEM'] == yaxis_column_name]['Value'],
            text=dfn[dfn['NA_ITEM'] == yaxis_column_name]['GEO'],
            mode='markers',
            marker={
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            }
        )],
        'layout': go.Layout(
            xaxis={
                'title': xaxis_column_name},
            yaxis={
                'title': yaxis_column_name},
            margin={'l': 65, 'b': 40, 't': 10, 'r': 0},
            hovermode='closest'
        )
    }

@app.callback(
    dash.dependencies.Output('country-graphic', 'figure'), 
     [dash.dependencies.Input('country_choice', 'value'),
      dash.dependencies.Input('unit_selection2', 'value'), 
      dash.dependencies.Input('yaxis', 'value')])

def update_graph2(country, select_unit2, yaxis_column_name_2):
    dfi = df[df['GEO'] == country]
    dfk = dfi[dfi['UNIT'] == select_unit2]
    
    return {
        'data': [go.Scatter(
            y=dfk[dfk['NA_ITEM'] == yaxis_column_name_2]['Value'], 
            x=dfk['TIME'].unique()
        )],
        'layout': go.Layout(
            xaxis={
                'title': 'Years'},
            yaxis={
                'title': yaxis_column_name_2},
            margin={'l': 75, 'b': 40, 't': 10, 'r': 0},
            hovermode='closest',
        )
    }
    
if __name__ == '__main__':
    app.run_server()

