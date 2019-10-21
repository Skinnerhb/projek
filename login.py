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

#fetch user info
def fetch(con):
    try:
        usr = []
        pas = []
        ids = []
        curs = con.cursor()
        curs.execute("SELECT UserID, Username, Password FROM user")
        rows = curs.fetchall()
        for i in rows:
            if len(i) > 1:
                ids.append(i[0])
                usr.append(i[1])
                pas.append(i[2])
        return usr, pas, ids
    except con.Error as e:
        print(e)
        close_con(con)
        
external_stylesheets = ['bWLwgP.css']
program = dash.Dash(__name__,external_stylesheets = external_stylesheets)

colorst = {
    'background':'#b3c4c4',
    'pbackground':'#ffffff',
    'ebackground':'#f2f2f2',
    'text': '#000000'
    }

program.layout(
    #main division start
    html.Div(
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
                children=[
                    html.Label('Username'),
                    dcc.Input(
                        id='usrr',
                        placeholder='ex. User1',
                        type='text'
                        ),
                    html.Label('Password'),
                    dcc.Input(
                        id='paas',
                        placeholder='ex. Passy1!word',
                        type='text'
                        ),
                    html.Button('Login',id='log'),
                    html.Button('Register',id='reg'),
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
    if n >= 1:
        if useri is not None:
            db = 'Flickermeter.db'
            con = connection(db)
            curs = con.cursor()
            curs.execute("SELECT 1 FROM user WHERE Username = ? AND Password",[useri, passi])
            if q.fetchone() is not None:
                close_con(con)
                return useri 
            else:
                close_con(con)
                return 'Username or password incorrect'   
        

if __name__ == '__main__':
    main()
    

