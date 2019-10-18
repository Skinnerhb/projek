import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go

program = dash.Dash(__name__)

colorst = {
    'background':'#b3c4c4',
    'pbackground':'#ffffff',
    'ebackground':'#f2f2f2',
    'text': '#000000'
    }

program.layout = html.Div(
    html.Div(style={'backgroundColor': colorst['background']},
             children =[
                 html.H1(children= 'Flicker Analyser',
                         style ={
                             'textAlign': 'center',
                             'color': colorst['text']
                             }
                         ),
                 html.Div(children = '''
                    This aplicaton analyses light input through the use of a TSL2561 and a TSL257, input is analysed with the use of dash and python, through Raspberry Pi.
                    '''
                          ),
                 html.Label('Select Property'),
                 dcc.Dropdown(
                     options=[
                         {'label':'Broadband (nm)','value':'nm'},
                         {'label':'Illuminance (lx)','value':'lx'},
                         {'label':'Flicker (%)','value':'flic'}
                         ],
                     value=['nm'],
                     multi=True
                     ),
                 dcc.Graph(
                     id = 'Main graph',
                     figure ={
                         'data': [
                             {'x': [1, 2, 3, 4, 5], 'y': [4, 1, 2, 3, 4], 'type': 'line', 'name': 'broadband'},
                             ],
                         'layout': {
                             'title': 'Broadband (nm)',
                             'plot_bgcolor': colorst['pbackground'],
                             'paper_bgcolor': colorst['ebackground'],
                             'font': {
                                 'color': colorst['text']
                                 }
                             }
                         }
                     ),
                 html.Label('Enter Distance from light source to device:'),
                 dcc.Input(
                     placeholder='In meter',
                     type='text'
                     value='m'
                     )
                 ]
             ),
    html.Div(style={'backgroundColor': colorst['background']
                    
                    }
        )
    )


if __name__=='__main__':
    program.run_server(debug=True)