import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd
import dash_table as dt

# Part I. Data Analysis
sales = pd.read_csv('sales.csv')
sales['Order Date'] = pd.to_datetime(sales['Order Date'])
sales['Year'] = sales['Order Date'].dt.year
sales['Month'] = sales['Order Date'].dt.month_name()


# Part II. Build a dashboard
app = dash.Dash(__name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}])

app.layout = html.Div([
    # First row
    html.Div([
        # Title
        html.Div([
            html.H3('Sales Dashboard', style={'margin-bottom': '0px', 'color': 'white'})
        ], className='one-third column', id='title1'),
        # Slider: choose a single value. (Note: RangeSlider choose a range of values)
        html.Div([
            html.P('Year', className='fix_label', style={'color': 'white'}),
            dcc.Slider(id='select_years',
                       included=False,  #If False value from chosen year. Eg. at 2017 only
                                        #If True sum from previous to the chosen years.
                                        #        Eg. value sum from 2015, 2016, 2017
                       updatemode='drag', # changing value by drag
                       tooltip={'always_visible': True}, # just a decoration to make clear which value are chosen
                       min=min(sales['Year']),  # Eg. 2015
                       max=max(sales['Year']),  # Eg. 2018
                       step=1,
                       value=max(sales['Year']),# default value. Eg. 2018
                       marks={str(yr): str(yr) for yr in range(min(sales['Year']),
                                                               max(sales['Year']))}, # marks on Slider
                       className='dcc_compon'),
        ], className='one-half column', id='title2'),
        # Radio Items (buttons) for Segment column of sales dataframe
        html.Div([
            html.P('Segment', className='fix_label', style={'color': 'white'}),
            dcc.RadioItems(id='radio_items',
                           labelStyle={'display': 'inline-block'},
                           value='Consumer', # default value getting from sales['Segment'].unique()
                                             # sales['Segment'].unique() -> ['Consumer', 'Corporate', 'Home Office']
                           options=[{'label': i, 'value': i} for i in sales['Segment'].unique()],
                           style={'text-align': 'center', 'color': 'white'},
                           className='dcc_compon'),
        ], className='one-third column', id='title3')
    ], id='header', className='row flex-display', style={'margin-bottom': '25px'}),

], id='mainContainer', style={'display': 'flex', 'flex-direction': 'column'})

if __name__ == '__main__':
    app.run_server(debug=True)
