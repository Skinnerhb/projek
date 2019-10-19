import dash
from dash.dependencies import Output, Input, State
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
import threading

program = dash.Dash(__name__)

colorst = {
    'background':'#b3c4c4',
    'pbackground':'#ffffff',
    'ebackground':'#f2f2f2',
    'text': '#000000'
    }

program.layout = html.Div(
    children=[
        html.Div(
            style={'backgroundColor': colorst['background']},
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
                            {'x': [1, 2, 3, 4, 5], 'y': [4, 1, 2, 3, 4], 'type': 'line', 'name': 'broadband'}
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
                    )
                ]
            ),
        html.Div(
            style={
                'backgroundColor': colorst['background']
                },
            children=[
                html.Label('Enter distance from light source to device:'),
                dcc.Input(
                    placeholder='In meter',
                    type='text'
                    ),
                html.Label('Enter radius of light'),
                dcc.Input(
                    placeholder='In meter',
                    type='text'
                    )
                ]
            ),
        html.Div(
            style={
                'backgroundColor': colorst['background']
                },
            children=[
                html.Label('To save enter light ID'),
                dcc.Input(
                    id='LID',
                    placeholder='ex. Light1',
                    type='text'
                    ),
                html.Label('and type of light'),
                dcc.Input(
                    id='LT',
                    placeholder='ex. Fluorescent',
                    type='text'
                    ),
                html.Label('Then press save'),
                html.Button('Save', id = 'Sbut'),
                html.Div(id='save_con',
                         children='Notice: Save will only start when ID and type in not empty'
                    )
                ]
            )
        ]
    )

###dcc.Markdown('''**bold text** and *italics* [links](https://something.com) 'code' snip can write lists, quotes and more''')
###dcc.Tabs(id ="tabs",value='tab-1',children=[dcc.Tab(label='Tab one',value='tab-1'), dcc.Tab(label='Tan two',value='tab-2')]), htlm.Div(tid='tabs-content')
###dcc.ConfirmDialog(id='confirm',message='warning, you sure you want to continue')
###dcc.Store(id='my-store', data='my-data':'data') must be used with callbacks
###dcc.location(id = 'url', refresh = False) href= "http://127.0.0.1:8050/page-2?a=test#quiz" pathname ="/page2" search ="?a=test" hash="#quiz"

###html.P('paragraph component')
###class is className
###style= 'color','fontSize','marginBottom','marginTop','width':%, 'display':'inline-block', 'float':'right'
###html.Table([html.Tr([html.Td(['x',html.Sup(2)]), html.Td(id='square')])])

@program.callback(
    Output('save_con','children'),
    [Input('Sbut','n_clicks')],
    [State('LID','value')]
    )
def upout(n_clicks, value):
    return 'clicks: {}, ID: "{}"'.format(
        n_clicks,
        value
        )
###program.callback(Output('tabs-content', 'children'), [Input('tabs',value)])
###def render_content(tab):
###if tab == 'tab-1':
###return html.Div([html.H3(Tab content 1)])
###elif tab == 'tab-2':
###return html.Div([html.H3(Tab content 2)])

###Output(component_id='',component_property='children')
###x = threading.Thread(target=thread_function,args(1,))
###x.start()

if __name__=='__main__':
    program.run_server(debug=True, use_reloader=False)