import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd
from dotenv import load_dotenv
import os

from mdb import MongoDB
########################################################################################################################
# I. DATA ANALYSIS

flag_mongodb = False

if flag_mongodb:
    print('Data is received from MongoDB')
    dotenv_file_path = r'.env'
    load_dotenv(dotenv_file_path)
    host = os.environ.get('MONGODB_HOST')
    port = int(os.environ.get('MONGODB_PORT'))
    db_name = os.environ.get('MONGODB_DB_NAME')
    # Read confirmed
    mdb_confirmed = MongoDB(host, port, db_name, collection_name=os.environ.get('MONGODB_COLLECTION_confirmed'))
    confirmed = mdb_confirmed.download_df()
    # print('confirmed.shape = ', confirmed.shape)

    # Read deaths
    mdb_deaths = MongoDB(host, port, db_name, collection_name=os.environ.get('MONGODB_COLLECTION_deaths'))
    deaths = mdb_deaths.download_df()
    # print('deaths.shape = ', deaths.shape)

    # Read recovered
    mdb_recovered = MongoDB(host, port, db_name, collection_name=os.environ.get('MONGODB_COLLECTION_recovered'))
    recovered = mdb_recovered.download_df()
    # print('recovered.shape = ', recovered.shape)

else:
    print('Data is received from Github')
    # Get url from github: https://github.com/CSSEGISandData/COVID-19
    url_confirmed = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv'
    url_deaths = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv'
    url_recovered = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv'

    confirmed = pd.read_csv(url_confirmed)
    deaths = pd.read_csv(url_deaths)
    recovered = pd.read_csv(url_recovered)

    # Save csv for testing
    confirmed.to_csv('time_series_covid19_confirmed_global.csv', index=False)
    deaths.to_csv('time_series_covid19_deaths_global.csv', index=False)
    recovered.to_csv('time_series_covid19_recovered_global.csv', index=False)

# End of if if flag_mongodb

# Unpivot data frames
date1 = confirmed.columns[4:]
total_confirmed = confirmed.melt(id_vars=['Province/State', 'Country/Region', 'Lat', 'Long'],
                                 value_vars=date1,
                                 var_name='date',
                                 value_name='confirmed')
date2 = deaths.columns[4:]
total_deaths = deaths.melt(id_vars=['Province/State', 'Country/Region', 'Lat', 'Long'],
                           value_vars=date2,
                           var_name='date',
                           value_name='death')
date3 = recovered.columns[4:]
total_recovered = recovered.melt(id_vars=['Province/State', 'Country/Region', 'Lat', 'Long'],
                                 value_vars=date3,
                                 var_name='date',
                                 value_name='recovered')

# Merging data frames: total_confirmed, total_deaths, total_recovered
covid_data = total_confirmed.merge(right = total_deaths,
                                   how = 'left',
                                   on = ['Province/State', 'Country/Region', 'date', 'Lat', 'Long'])
covid_data = covid_data.merge(right = total_recovered,
                              how = 'left',
                              on = ['Province/State', 'Country/Region', 'date', 'Lat', 'Long'])

# Change column datatype from string to proper date format
covid_data['date'] = pd.to_datetime(covid_data['date'])

# At 'recovered' column: Replace NaN with 0
covid_data['recovered'] = covid_data['recovered'].fillna(0)

# Create new column: Active cases
covid_data['active'] = covid_data['confirmed'] - covid_data['death'] - covid_data['recovered']

# Group by date for all countries
covid_data_by_date = covid_data.groupby(['date'])[['confirmed', 'death', 'recovered', 'active']].sum().reset_index()

# Create dictionary of list
covid_data_list = covid_data[['Country/Region', 'Lat', 'Long']]
df = covid_data_list.set_index('Country/Region')[['Lat', 'Long']].T
df = df.loc[:,~df.columns.duplicated()]
dict_of_locations = df.to_dict('dict')

########################################################################################################################
# II. DASH
app = dash.Dash(__name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}])
server = app.server

app.layout = html.Div([
    # First row with 3 columns
    html.Div([
        html.Div([  # image
            html.Img(src=app.get_asset_url('corona-covid19-logo.jpg'),
                     id = 'corona-image',
                     style={'height': '163px',
                            'width': '480px', #
                            'margin-bottom': '15px'})
        ], className='one-third column'),

        html.Div([  # Title. Div and Heading H3, H5
            html.Div([
                html.H2('Covid-19', style={'margin-bottom': '0px', 'color': 'white', 'font-weight': 'bold'}),
                html.H3('Tracking Cases', style={'margin-bottom': '0px', 'color': 'white'})
            ])
        ], className='one-half column', id = 'title'),

        html.Div([ # Time string
            html.H6('Updated: ' + str(covid_data['date'].iloc[-1].strftime('%B %d, %Y')) + ' 00:01 (UTC)',
                    style={'color': 'orange'})
        ], className='one-third column', id = 'title1')
    ], id = 'header', className= 'row flex-display', style={'margin-bottom': '25px'}),

    # Second row: 4 cards. Each card: 3 columns -> 4*3=12 columns
    # Note: html.P: P is a wrapper for the <p> HTML5 element
    html.Div([
        html.Div([ # 'Global Cases' card
            html.H6(children='Global Cases',
                    style={'textAlign': 'center',
                           'color': 'white'}),
            html.P(f"{covid_data_by_date['confirmed'].iloc[-1]:,.0f}",
                    style={'textAlign': 'center',
                           'color': 'orange',
                           'fontSize': 40}),
            html.P('new: ' + f"{covid_data_by_date['confirmed'].iloc[-1] - covid_data_by_date['confirmed'].iloc[-2]:,.0f}"
                   + ' (' + str(round(((covid_data_by_date['confirmed'].iloc[-1] - covid_data_by_date['confirmed'].iloc[-2]) /
                                   covid_data_by_date['confirmed'].iloc[-1]) * 100, 2)) + '%)',
                   style={'textAlign': 'center',
                          'color': 'orange',
                          'fontSize': 15,
                          'margin-top': '-18px'})
        ], className='card_container three columns'),

        html.Div([ # 'Global Active' card
            html.H6(children='Global Active',
                    style={'textAlign': 'center',
                           'color': 'white'}),
            html.P(f"{covid_data_by_date['active'].iloc[-1]:,.0f}",
                    style={'textAlign': 'center',
                           'color': '#e55467',
                           'fontSize': 40}),
            html.P('new: ' + f"{covid_data_by_date['active'].iloc[-1] - covid_data_by_date['active'].iloc[-2]:,.0f}"
                   + ' (' + str(round(((covid_data_by_date['active'].iloc[-1] - covid_data_by_date['active'].iloc[-2]) /
                                   covid_data_by_date['active'].iloc[-1]) * 100, 2)) + '%)',
                   style={'textAlign': 'center',
                          'color': '#e55467',
                          'fontSize': 15,
                          'margin-top': '-18px'})
        ], className='card_container three columns'),

        html.Div([ # 'Global Recovered' card
            html.H6(children='Global Recovered',
                    style={'textAlign': 'center',
                           'color': 'white'}),
            html.P(f"{covid_data_by_date['recovered'].iloc[-1]:,.0f}",
                    style={'textAlign': 'center',
                           'color': 'green',
                           'fontSize': 40}),
            html.P('new: ' + f"{covid_data_by_date['recovered'].iloc[-1] - covid_data_by_date['recovered'].iloc[-2]:,.0f}"
                   + ' (' + str(round(((covid_data_by_date['recovered'].iloc[-1] - covid_data_by_date['recovered'].iloc[-2]) /
                                   covid_data_by_date['recovered'].iloc[-1]) * 100, 2)) + '%)',
                   style={'textAlign': 'center',
                          'color': 'green',
                          'fontSize': 15,
                          'margin-top': '-18px'})

        ], className='card_container three columns'),

        html.Div([ # 'Global Deaths' card
            html.H6(children='Global Deaths',
                    style={'textAlign': 'center',
                           'color': 'white'}),
            html.P(f"{covid_data_by_date['death'].iloc[-1]:,.0f}",
                    style={'textAlign': 'center',
                           'color': '#dd1e35',
                           'fontSize': 40}),
            html.P('new: ' + f"{covid_data_by_date['death'].iloc[-1] - covid_data_by_date['death'].iloc[-2]:,.0f}"
                   + ' (' + str(round(((covid_data_by_date['death'].iloc[-1] - covid_data_by_date['death'].iloc[-2]) /
                                   covid_data_by_date['death'].iloc[-1]) * 100, 2)) + '%)',
                   style={'textAlign': 'center',
                          'color': '#dd1e35',
                          'fontSize': 15,
                          'margin-top': '-18px'})
        ], className='card_container three columns'),

    ], className='row flex display'),

    # Third row: Dropdown list, Donut chart and Bar-Line chart
    html.Div([
        html.Div([ #Dropdown list: Making a label, drop-down list, and KPI indicators
            html.P('Select Country:', className='fix_label', style={'color': 'white'}),
            dcc.Dropdown(id = 'w_countries',
                         multi = False,  # choosing only at a time
                         searchable= True,
                         value='Australia',  # a default value at dropdown
                         placeholder= 'Select Countries',
                         # options are list of values of dropdown
                         options= [{'label': c, 'value': c}
                                   for c in (covid_data['Country/Region'].unique())],
                         className='dcc_compon'),

            # New cases for this chosen country
            html.P('New Cases: ' + ' ' + str(covid_data['date'].iloc[-1].strftime('%B %d, %Y')),
                   className='fix_label', style={'text-align': 'center', 'color': 'white'}),

            # Layout of graph component with id='confirmed' -> so need to write a callback function to do it
            # when selecting a country in dropdown list, it will filter data to that country to display
            dcc.Graph(id = 'confirmed', config={'displayModeBar': False}, className='dcc_compon',
                      style={'margin-top': '20px'}),

            dcc.Graph(id = 'active', config={'displayModeBar': False}, className='dcc_compon',
                      style={'margin-top': '20px'}),

            dcc.Graph(id = 'recovered', config={'displayModeBar': False}, className='dcc_compon',
                      style={'margin-top': '20px'}),

            dcc.Graph(id = 'death', config={'displayModeBar': False}, className='dcc_compon',
                      style={'margin-top': '20px'}),
        ], className='create_container three columns'),

        html.Div([ # Donut chart layout
            dcc.Graph(id = 'donut_chart', config={'displayModeBar': 'hover'})
        ], className='create_container four columns'),

        html.Div([  # bar-line chart layout
            dcc.Graph(id = 'line_chart', config={'displayModeBar': 'hover'})
        ], className='create_container five columns'),
    ], className='row flex-display'),

    # Fourth row: Mapbox Map Layer chart
    html.Div([
        html.Div([
            dcc.Graph(id = 'map_chart', config={'displayModeBar': 'hover'})
        ], className='create_container1 twelve columns')
    ], className='row flex-display')

], id = 'mainContainer', style={'display': 'flex', 'flex-direction': 'column'})

# callback for id='confirmed'. INPUT: id='w_countries' and OUTPUT: id='confirmed'
@app.callback(Output(component_id='confirmed', component_property='figure'),
              [Input(component_id='w_countries', component_property='value')])
def update_confirmed(w_countries):
    '''input argument is w_countries (id of dropdown list) to get a dynamic value
    Since call-back will call the function right below it, name of the function is not important'''
    covid_data_2 = covid_data.groupby(['date', 'Country/Region'])[['confirmed', 'death', 'recovered', 'active']].sum().reset_index()
    # Today
    value_confirmed = covid_data_2[covid_data_2['Country/Region'] == w_countries]['confirmed'].iloc[-1] - covid_data_2[covid_data_2['Country/Region'] == w_countries]['confirmed'].iloc[-2]
    # Yesterday
    value_confirmed_yesterday = covid_data_2[covid_data_2['Country/Region'] == w_countries]['confirmed'].iloc[-2] - covid_data_2[covid_data_2['Country/Region'] == w_countries]['confirmed'].iloc[-3]
    # print(f'value_confirmed = {value_confirmed}, value_confirmed_yesterday = {value_confirmed_yesterday}')
    return {
        'data': [go.Indicator(
               mode='number+delta',
               value=value_confirmed,
               delta = {'reference': value_confirmed_yesterday,
                        'position': 'right',
                        'valueformat': ',g',
                        'relative': False,
                        'font': {'size': 15}},
               number={'valueformat': ',',
                       'font': {'size': 20}},
               domain={'y': [0, 1], 'x': [0, 1]} # it is alignment of the two values
        )],
        'layout': go.Layout(
            title={'text': 'New Confirmed',
                   'y': 1,
                   'x': 0.5,
                   'xanchor': 'center',
                   'yanchor': 'top'},
            font=dict(color='orange'),
            paper_bgcolor='#1f2c56',
            plot_bgcolor='#1f2c56',
            height = 50,
        )
    }

@app.callback(Output('active', 'figure'),
              [Input('w_countries','value')])
def update_active(w_countries):
    covid_data_2 = covid_data.groupby(['date', 'Country/Region'])[['confirmed', 'death', 'recovered', 'active']].sum().reset_index()
    value_active = covid_data_2[covid_data_2['Country/Region'] == w_countries]['active'].iloc[-1] - covid_data_2[covid_data_2['Country/Region'] == w_countries]['active'].iloc[-2]
    value_active_yesterday = covid_data_2[covid_data_2['Country/Region'] == w_countries]['active'].iloc[-2] - covid_data_2[covid_data_2['Country/Region'] == w_countries]['active'].iloc[-3]
    # print(f'value_active = {value_active}, value_active_yesterday = {value_active_yesterday}')
    return {
        'data': [go.Indicator(
               mode='number+delta',
               value=value_active,
               delta = {'reference': value_active_yesterday,
                        'position': 'right',
                        'valueformat': ',g',
                        'relative': False,
                        'font': {'size': 15}},
               number={'valueformat': ',',
                       'font': {'size': 20}},
               domain={'y': [0, 1], 'x': [0, 1]}
        )],
        'layout': go.Layout(
            title={'text': 'New Active',
                   'y': 1,
                   'x': 0.5,
                   'xanchor': 'center',
                   'yanchor': 'top'},
            font=dict(color='#e55467'),
            paper_bgcolor='#1f2c56',
            plot_bgcolor='#1f2c56',
            height = 50,
        )
    }

@app.callback(Output('recovered', 'figure'),
              [Input('w_countries','value')])
def update_recovered(w_countries):
    covid_data_2 = covid_data.groupby(['date', 'Country/Region'])[['confirmed', 'death', 'recovered', 'active']].sum().reset_index()
    value_recovered = covid_data_2[covid_data_2['Country/Region'] == w_countries]['recovered'].iloc[-1] - covid_data_2[covid_data_2['Country/Region'] == w_countries]['recovered'].iloc[-2]
    value_recovered_yesterday = covid_data_2[covid_data_2['Country/Region'] == w_countries]['recovered'].iloc[-2] - covid_data_2[covid_data_2['Country/Region'] == w_countries]['recovered'].iloc[-3]
    # print(f'value_recovered = {value_recovered}, value_recovered_yesterday={value_recovered_yesterday}')
    return {
        'data': [go.Indicator(
               mode='number+delta',
               value=value_recovered,
               delta = {'reference': value_recovered_yesterday,
                        'position': 'right',
                        'valueformat': ',g',
                        'relative': False,
                        'font': {'size': 15}},
               number={'valueformat': ',',
                       'font': {'size': 20}},
               domain={'y': [0, 1], 'x': [0, 1]}
        )],

        'layout': go.Layout(
            title={'text': 'New Recovered',
                   'y': 1,
                   'x': 0.5,
                   'xanchor': 'center',
                   'yanchor': 'top'},
            font=dict(color='green'),
            paper_bgcolor='#1f2c56',
            plot_bgcolor='#1f2c56',
            height = 50,
        )
    }

@app.callback(Output('death', 'figure'),
              [Input('w_countries','value')])
def update_death(w_countries):
    covid_data_2 = covid_data.groupby(['date', 'Country/Region'])[['confirmed', 'death', 'recovered', 'active']].sum().reset_index()
    value_death = covid_data_2[covid_data_2['Country/Region'] == w_countries]['death'].iloc[-1] - covid_data_2[covid_data_2['Country/Region'] == w_countries]['death'].iloc[-2]
    delta_death = covid_data_2[covid_data_2['Country/Region'] == w_countries]['death'].iloc[-2] - covid_data_2[covid_data_2['Country/Region'] == w_countries]['death'].iloc[-3]
    return {
        'data': [go.Indicator(
               mode='number+delta',
               value=value_death,
               delta = {'reference': delta_death,
                        'position': 'right',
                        'valueformat': ',g',
                        'relative': False,
                        'font': {'size': 15}},
               number={'valueformat': ',',
                       'font': {'size': 20}},
               domain={'y': [0, 1], 'x': [0, 1]}
        )],
        'layout': go.Layout(
            title={'text': 'New Death',
                   'y': 1,
                   'x': 0.5,
                   'xanchor': 'center',
                   'yanchor': 'top'},
            font=dict(color='#dd1e35'),
            paper_bgcolor='#1f2c56',
            plot_bgcolor='#1f2c56',
            height = 50,
        )
    }

@app.callback(Output(component_id='donut_chart', component_property='figure'),
              [Input(component_id='w_countries', component_property='value')])
def update_donut_chart(w_countries):
    '''input argument is a dropdown list id to have a dynamic chosen value'''
    covid_data_2 = covid_data.groupby(['date', 'Country/Region'])[['confirmed', 'death', 'recovered', 'active']].sum().reset_index()
    confirmed_value = covid_data_2[covid_data_2['Country/Region'] == w_countries]['confirmed'].iloc[-1]
    death_value = covid_data_2[covid_data_2['Country/Region'] == w_countries]['death'].iloc[-1]
    recovered_value = covid_data_2[covid_data_2['Country/Region'] == w_countries]['recovered'].iloc[-1]
    active_value = covid_data_2[covid_data_2['Country/Region'] == w_countries]['active'].iloc[-1]
    colors = ['#dd1e35', 'green', '#e55467']
    return {
        'data': [go.Pie(
            labels=['Death', 'Recovered', 'Active'],
            values=[death_value, recovered_value, active_value],
            marker=dict(colors=colors),
            hoverinfo='label+value+percent',
            textinfo='label+value',
            hole=0.7,  # hole=0 -> pie chart
            rotation=45,
        )],
        'layout': go.Layout(
            title={'text': 'Total Confirmed Cases in ' + (w_countries) + ': ' + str('{:,}'.format(confirmed_value)),
                   'y': 0.93,  # Position of Title
                   'x': 0.5,   # Position of Title
                   'xanchor': 'center',
                   'yanchor': 'top'},
            titlefont={'color': 'white',
                       'size': 20},
            font=dict(family='sans-serif',
                      color='white',
                      size=14),
            hovermode='closest',
            paper_bgcolor='#1f2c56',
            plot_bgcolor='#1f2c56',
            legend={'orientation': 'v',
                    'bgcolor': '#1f2c56',
                    'xanchor': 'center', 'x': 0.5, 'y': -0.7}
        )
    }

@app.callback(Output('line_chart', 'figure'),
              [Input('w_countries','value')])
def update_bar_line_chart(w_countries):
    covid_data_2 = covid_data.groupby(['date', 'Country/Region'])[['confirmed', 'death', 'recovered', 'active']].sum().reset_index()
    covid_data_3 = covid_data_2[covid_data_2['Country/Region'] == w_countries][['Country/Region', 'date', 'confirmed']].reset_index()
    covid_data_3['daily confirmed'] = covid_data_3['confirmed'] - covid_data_3['confirmed'].shift(1)
    covid_data_3['Moving Average'] = covid_data_3['daily confirmed'].rolling(window=7).mean()
    return {
        'data': [go.Bar(
            x=covid_data_3['date'].tail(30),  # 30 day data
            y=covid_data_3['daily confirmed'].tail(30), # 30 day data
            name='Daily Confirmed Cases',
            marker=dict(color='orange'),
            hoverinfo='text',
            hovertext=
            '<b>Date</b>: ' + covid_data_3['date'].tail(30).astype(str) + '<br>' +
            '<b>Daily Confirmed Cases</b>: ' + [f'{x:,.0f}' for x in covid_data_3['daily confirmed'].tail(30)] + '<br>'
            # + '<b>Country</b>: ' + covid_data_3['Country/Region'].tail(30).astype(str) + '<br>'
        ),
            go.Scatter(
                x=covid_data_3['date'].tail(30),
                y=covid_data_3['Moving Average'].tail(30),
                mode='lines',
                name='Moving Average of the last 7 days',
                line=dict(width=5, color='#FF00FF'),
                hoverinfo='text',
                hovertext=
                '<b>Date</b>: ' + covid_data_3['date'].tail(30).astype(str) + '<br>' +
                '<b>Daily Confirmed Cases</b>: ' + [f'{x:,.0f}' for x in covid_data_3['Moving Average'].tail(30)] + '<br>'
            )],

        'layout': go.Layout(
            title={'text': 'Last 30 Days Daily Confirmed Cases: ' + (w_countries),
                   'y': 0.93,
                   'x': 0.5,
                   'xanchor': 'center',
                   'yanchor': 'top'},
            titlefont={'color': 'white',
                       'size': 20},
            font=dict(family='sans-serif',
                      color='white',
                      size=12),
            hovermode='closest',
            paper_bgcolor='#1f2c56',
            plot_bgcolor='#1f2c56',
            legend={'orientation': 'h',
                    'bgcolor': '#1f2c56',
                    'xanchor': 'center', 'x': 0.5, 'y': -0.7},
            margin=dict(r=0),
            xaxis=dict(title='<b>Date</b>',
                       color = 'white',
                       showline=True,
                       showgrid=True,
                       showticklabels=True,
                       linecolor='white',
                       linewidth=1,
                       ticks='outside',
                       tickfont=dict(
                           family='Aerial',
                           color='white',
                           size=12
                       )),
            yaxis=dict(title='<b>Daily Confirmed Cases</b>',
                       color='white',
                       showline=True,
                       showgrid=True,
                       showticklabels=True,
                       linecolor='white',
                       linewidth=1,
                       ticks='outside',
                       tickfont=dict(
                           family='Aerial',
                           color='white',
                           size=12)
                       )
        )
    }

@app.callback(Output('map_chart', 'figure'),
              [Input('w_countries','value')])
def update_map_chart(w_countries):
    covid_data_4 = covid_data.groupby(['Lat', 'Long', 'Country/Region'])[['confirmed', 'death', 'recovered', 'active']].max().reset_index()
    covid_data_5 = covid_data_4[covid_data_4['Country/Region'] == w_countries]

    if w_countries:
        zoom=2
        zoom_lat = dict_of_locations[w_countries]['Lat']
        zoom_long = dict_of_locations[w_countries]['Long']
    return {
        'data': [go.Scattermapbox(
            lon=covid_data_5['Long'],
            lat=covid_data_5['Lat'],
            mode='markers',
            marker=go.scattermapbox.Marker(size=covid_data_5['confirmed'] / 1500,
                                           color=covid_data_5['confirmed'],
                                           colorscale='HSV',
                                           showscale=False,
                                           sizemode='area',
                                           opacity=0.3),
            hoverinfo='text',
            hovertext=
            '<b>Country</b>: ' + covid_data_5['Country/Region'].astype(str) + '<br>' +
            '<b>Longitude</b>: ' + covid_data_5['Long'].astype(str) + '<br>' +
            '<b>Latitude</b>: ' + covid_data_5['Lat'].astype(str) + '<br>' +
            '<b>Confirmed Cases</b>: ' + [f'{x:,.0f}' for x in covid_data_5['confirmed']] + '<br>' +
            '<b>Death</b>: ' + [f'{x:,.0f}' for x in covid_data_5['death']] + '<br>' +
            '<b>Recovered Cases</b>: ' + [f'{x:,.0f}' for x in covid_data_5['recovered']] + '<br>' +
            '<b>Active Cases</b>: ' + [f'{x:,.0f}' for x in covid_data_5['active']] + '<br>'
        )],

        'layout': go.Layout(
            hovermode='x',
            paper_bgcolor='#1f2c56',
            plot_bgcolor='#1f2c56',
            margin=dict(r=0, l =0, b = 0, t = 0), # right, left, bottom, top
            # Need mapbox token. Goto mapbox.com to sign-up and get one
            mapbox=dict(
                accesstoken='pk.eyJ1IjoicXM2MjcyNTI3IiwiYSI6ImNraGRuYTF1azAxZmIycWs0cDB1NmY1ZjYifQ.I1VJ3KjeM-S613FLv3mtkw',
                center = go.layout.mapbox.Center(lat=zoom_lat, lon=zoom_long),
                style='dark',
                zoom=zoom,
            ),
            autosize=True
        )
    }

if __name__ == '__main__':
    app.run_server(debug=True)

