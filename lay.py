import dash_core_components as dcc
import dash_html_components as html

colorst = {
    'background':'#b3c4c4',
    'pbackground':'#ffffff',
    'ebackground':'#f2f2f2',
    'text': '#000000'
    }

#login layout
     #main division start
layout1 = html.Div([
    html.Div(
        id = 'loginlayout',
        style ={
            'textAlign': 'center',
            'color': colorst['text'],
            'fontSize':18
            },
        children=[
            #sub division header start
            html.Div(
                children=[
                    html.H1(children= 'Log in or Register',
                        style ={
                            'textAlign': 'center',
                            'color': colorst['text']
                            }
                        ),
                    ]
                ),
            #sub division header ends
            #sub division login start
            html.Div(
                style ={
                    'textAlign': 'center',
                    'color': colorst['text'],
                    'fontSize':18
                    },
                children=[
                    html.Label('Username:'),
                    dcc.Input(
                        id='usrr',
                        placeholder='ex. User1',
                        type='text'
                        )
                    ]
                ),
            html.Div(
                style ={
                    'textAlign': 'center',
                    'color': colorst['text'],
                    'fontSize':18
                    },
                children=[
                    html.Label('Password:'),
                    dcc.Input(
                        id='paas',
                        placeholder='ex. Passy1!word',
                        type='password'
                        )
                    ]
                ),
            html.Div(
                style ={
                    'textAlign': 'center',
                    'color': colorst['text'],
                    'fontSize':18
                    },
                children=[
                    dcc.Link(
                        html.Button('Login',id='log'),
                        href = '/api/Main',
                        id = 'logmain'
                        ),
                    dcc.Link(
                        html.Button('Register',id='reg'),
                        href = '/api/register',
                        id = 'logreg'
                        )
                    ]
                ),
            html.Div(
                id = 'show'
                )
            #sub division login ends
            ]
        )
    ])#end main division

#app layout
layout2 = html.Div([#head division
    html.Div(
        #sub division with header and explanation
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
            ]
        ),
        #end sub division
    html.Div(
        style={'backgroundColor': colorst['background']},
        #sub division with tabs
        children=[
            dcc.Tabs(
                id='tabbing',
                value='tab-1',
                children=[
                    dcc.Tab(
                        label='Broadband',
                        value='tab-1',
                        children =[
                            html.H2(
                                children= 'Broadband measurent (nm)',
                                style ={
                                    'textAlign': 'center',
                                    'color': colorst['text']
                                    }
                                ),
                            dcc.Graph(
                                id = 'graph-1'
                                ),
                            dcc.Interval(
                                id='inter',
                                interval=500,
                                n_intervals=0
                                )
                            ]
                        ),
                    html.Div(id='graphing1'),
                    dcc.Tab(
                        label='Illuminance',
                        value='tab-2',
                        children =[
                            html.H2(
                                children= 'Illuminance measurent (lx)',
                                style ={
                                    'textAlign': 'center',
                                    'color': colorst['text']
                                    }
                                ),
                            dcc.Graph(
                                id = 'graph-2'
                                ),
                            dcc.Interval(
                                id='inter2',
                                interval=500,
                                n_intervals=0
                                )
                            ]
                        ),
                    html.Div(id='graphing2'),
                    dcc.Tab(
                        label='Flicker',
                        value='tab-3',
                        children =[
                            html.H2(
                                children= 'Flicker measurent (%)',
                                style ={
                                    'textAlign': 'center',
                                    'color': colorst['text']
                                    }
                                ),
                            dcc.Graph(
                                id = 'graph-3'
                                ),
                            dcc.Interval(
                                id='inter3',
                                interval=500,
                                n_intervals=0
                                )
                            ]
                        ),
                    html.Div(id='graphing3')
                    ]
                 ),
            html.Div(id='tab-stuff')
            ]
        #end tab division
        ),
    html.Div(
        #start sub save division
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
        #end sub save division
        ),
    html.Div(
        #start sub flux division
        style={
            'backgroundColor': colorst['background']
            },
        children=[
            html.Label('Enter distance from light source to device:'),
            dcc.Input(
                id = 'fli',
                placeholder='In meter',
                type='text'
                ),
            html.Label('Enter radius of light'),
            dcc.Input(
                id = 'cdi',
                placeholder='In meter',
                type='text'
                )
            ]
        #end sub flux division
        ),
    html.Div(
        #start dropdown sub division
        style={
            'backgroundColor': colorst['background']
            },
        children = [
            dcc.Dropdown(
                id='property',
                options=[
                    {'label':'Broadband (nm)','value':'nm'},
                    {'label':'Infrared (nm)','value':'inf'},
                    {'label':'Visible Light (nm)','value':'VL'},
                    {'label':'Illuminance (lx)','value':'lx'},
                    {'label':'Flicker Modulation (%)','value':'flicm'},
                    {'label':'Flicker Index','value':'flici'},
                    {'label':'Long Term Flicker (%)','value':'Lflic'},
                    {'label':'Luminous Flux (lm)','value':'lm'},
                    {'label':'Luminous Intensity (cd)','value':'cd'}
                    ],
                placeholder="Select a property to display"
                ),
            dcc.Interval(
                id='inter4',
                interval=500,
                n_intervals=0
                ),
            html.Label(id = 'prop')
            ]
        #end dropdown sub division
        )    
    ])#end main division

#register layout
layout3 = html.Div([#main division start
    html.Div(
        style ={
            'textAlign': 'center',
            'color': colorst['text'],
            'fontSize':18
            },
        children=[
            #sub division header start
            html.Div(
                children=[
                    html.H1(children= 'Register',
                        style ={
                            'textAlign': 'center',
                            'color': colorst['text']
                            }
                        ),
                    ]
                ),
            #sub division header ends
            #sub division Register start
            html.Div(
                style ={
                    'textAlign': 'center',
                    'color': colorst['text'],
                    'fontSize':18
                    },
                children=[
                    html.Label('Username:'),
                    dcc.Input(
                        id='usrreg',
                        placeholder='ex. User1',
                        type='text'
                        )
                    ]
                ),
            html.Div(
                style ={
                    'textAlign': 'center',
                    'color': colorst['text'],
                    'fontSize':18
                    },
                children=[
                    html.Label('Name:'),
                    dcc.Input(
                        id='namreg',
                        placeholder='ex. John',
                        type='text'
                        )
                    ]
                ),
            html.Div(
                style ={
                    'textAlign': 'center',
                    'color': colorst['text'],
                    'fontSize':18
                    },
                children=[
                    html.Label('Surname:'),
                    dcc.Input(
                        id='surreg',
                        placeholder='ex. Doe',
                        type='text'
                        )
                    ]
                ),
            html.Div(
                style ={
                    'textAlign': 'center',
                    'color': colorst['text'],
                    'fontSize':18
                    },
                children=[
                    html.Label('Password:'),
                    dcc.Input(
                        id='pasreg',
                        placeholder='ex. Passy1!word',
                        type='password'
                        )
                    ]
                ),
            html.Div(
                style ={
                    'textAlign': 'center',
                    'color': colorst['text'],
                    'fontSize':18
                    },
                children=[
                    html.Label('Confirm Password:'),
                    dcc.Input(
                        id='cpasreg',
                        placeholder='ex. Passy1!word',
                        type='password'
                        )
                    ]
                ),
            html.Div(
                style ={
                    'textAlign': 'center',
                    'color': colorst['text'],
                    'fontSize':18
                    },
                children=[
                    html.Button('Register',id='regg'),
                    html.Button('Cancel',id='can'),
                    dcc.Interval(
                        id='interv',
                        interval=500,
                        n_intervals=0
                        )
                    ]
                ),
            html.Div(
                style ={
                    'textAlign': 'center',
                    'color': colorst['text'],
                    'fontSize':18
                    },
                children=[
                    html.Label(id = 'showreg')
                    ]
                )
            #sub division Register ends
            
            ]
        )
    ])#end main division
