from dash.dependencies import Input, Output
import sqlite3
from connect import connection, close_con
from Program import program

@program.callback(
    Output('show','children'),
    [Input('usrr','value'),
     Input('paas','value'),
     Input('url','pathname')
     ]
    )
def log_user(useri,passi,pathname):
    if pathname == '/api/Main':
        if useri is not None and passi is not None:
            db = 'Flickermeter.db'
            con = connection(db)
            curs = con.cursor()
            curs.execute("SELECT 1 FROM User WHERE Username = ? AND Password = ?",(useri, passi))
            if curs.fetchone() is not None:
                close_con(con)
                return 'Logging in'
            else:
                close_con(con)
                return 'Username or password incorrect'
        else:
            return 'No Username or Password given'

#@program.callback(
   # Output('url','pathname'),
    #[Input('intervl','n_intervals')]
   # )
#def resets(nil):
    #return '/api/login'

@program.callback(
    Output('app-2','children'),
    [Input('drop2','value')]
    )
def display1(value):
    return 'You have selected "{}"'.format(value)