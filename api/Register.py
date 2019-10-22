import dash
from dash.dependencies import Output, Input, State
import dash_core_components as dcc
import dash_html_components as html
import sqlite3
from connect import connection, close_con
from Program import program


colorst = {
    'background':'#b3c4c4',
    'pbackground':'#ffffff',
    'ebackground':'#f2f2f2',
    'text': '#000000'
    }

layout = html.Div(
    #main division start
    children = [
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
        ]
    #end main division
    )

@program.callback(
    Output('showreg','children'),
    [Input('usrreg','value'),
     Input('namreg','value'),
     Input('surreg','value'),
     Input('pasreg','value'),
     Input('cpasreg','value'),
     Input('regg','n_clicks')
     ]
    )
def reg_user(userreg,namereg,snamereg,passreg,cpassreg,n):
    clicked = 0
    if n != 0:
        clicked = 1
        
    if clicked == 1:
        if userreg is not None and namereg is not None and snamereg is not None and passreg is not None and cpassreg is not None:
            db = 'Flickermeter.db'
            con = connection(db)
            curs = con.cursor()
            curs.execute("SELECT 1 FROM User WHERE Username = ?",(userreg,))
            if curs.fetchone() is None:
                if passreg == cpassreg:
                    curs.execute("INSERT INTO User (Username,Name,Surname,Password) VALUES (?,?,?,?);", (userreg, namereg, snamereg, passreg))
                    con.commit()
                    close_con(con)
                    clicked = 0
                    return userreg
                else:
                    close_con(con)
                    return 'Passwords do not match'
            else:
                close_con(con)
                return 'Username already exists'
        else:
            return 'Missing Information'

@program.callback(
    Output('regg','n_clicks'),
    [Input('interv','n_intervals')]
    )
def reset(ni):
    return 0

    


