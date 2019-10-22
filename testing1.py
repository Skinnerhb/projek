import dash_core_components as dcc
import dash_html_components as html

colorst = {
    'background':'#b3c4c4',
    'pbackground':'#ffffff',
    'ebackground':'#f2f2f2',
    'text': '#000000'
    }

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
                        ),
                    dcc.Interval(
                        id='intervl',
                        interval=2000,
                        n_intervals=0
                        )
                    ]
                ),
            html.Div(
                id = 'show'
                )
            #sub division login ends
            ]
        )
    ])

layout2 = html.Div([
    html.Div('App 2'),
    dcc.Dropdown(
        id = 'drop2',
        options = [
            {'label':'App 2 - {}'.format(i),'value':i} for i in [
                'NYC','MTL','LA'
                ]
            ]
        ),
    html.Div(id='app-2'),
    dcc.Link(
        html.Button('Go1',id = 'app2b'),
        href='/api/api1',
        id='app2'
        )
    ])

