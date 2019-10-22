from flask import Flask
import dash
from dash.dependencies import Output, Input, State
import dash_core_components as dcc
import dash_html_components as html
import sqlite3

#Database connection
def connection(db):
    con = None
    try:
        con = sqlite3.connect(db)
    except con.Error as e:
        print(e)
    
    return con

#close connection
def close_con(con):
    con.close()
        
external_stylesheets = ['bWLwgP.css']
program = dash.Dash(__name__,external_stylesheets = external_stylesheets)

colorst = {
    'background':'#b3c4c4',
    'pbackground':'#ffffff',
    'ebackground':'#f2f2f2',
    'text': '#000000'
    }

program.layout = (
    #main division start
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
                    html.Button('Login',id='log'),
                    html.Button('Register',id='reg'),
                    dcc.Interval(
                        id='intervl',
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
                    html.Label(id = 'show')
                    ]
                )
            #sub division login ends
            
            ]
        )
    #end main division
    )

@program.callback(
    Output('show','children'),
    [Input('usrr','value'),
     Input('paas','value'),
     Input('log','n_clicks')
     ]
    )
def log_user(useri,passi,n):
    clicker - 0
    if n != 0:
        clicker = 1
    
    if clicker == 1:
        if useri is not None and passi is not None:
            db = 'Flickermeter.db'
            con = connection(db)
            curs = con.cursor()
            curs.execute("SELECT 1 FROM user WHERE Username = ? AND Password = ?",(useri, passi))
            if curs.fetchone() is not None:
                close_con(con)
                clicker = 0
                return useri
            else:
                close_con(con)
                return 'Username or password incorrect'
        else:
            return 'No Username or Password given'

@program.callback(
    Output('log','n_clicks'),
    [Input('intervl','n_intervals')]
    )
def resets(nil):
    return 0

if __name__ == '__main__':
    program.run_server(debug=True,use_reloader=False)
    

