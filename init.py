import sys
import dash
from dash.dependencies import Output, Input, State
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
import threading
import numpy as np
import board
import busio
import adafruit_tsl2561 as tsl
from timeit import default_timer as timer
import time
import math
import sqlite3
from collections import deque
from Program import program
from connect import connection, close_con
from api import  Register, Main

colorst = {
    'background':'#b3c4c4',
    'pbackground':'#ffffff',
    'ebackground':'#f2f2f2',
    'text': '#000000'
    }

program.layout = html.Div(children=[html.Div(id='initi'),dcc.Interval(id='interinit',interval=900,n_intervals=0)])

@program.callback(
    Output('initi','children'),
    [Input('interinit','n_intervals')]
    )
def changePage(ninterval):
    if defining == 0:
        return 
    elif defining == 1:
        return Main.layout

#login callback
@program.callback(
    Output('show','children'),
    [Input('usrr','value'),
     Input('paas','value'),
     Input('log','n_clicks')
     ]
    )
def log_user(useri,passi,n):
    clicker = 0
    if n != 0:
        clicker = 1
    
    if clicker == 1:
        if useri is not None and passi is not None:
            db = 'Flickermeter.db'
            con = connection(db)
            curs = con.cursor()
            curs.execute("SELECT 1 FROM User WHERE Username = ? AND Password = ?",(useri, passi))
            if curs.fetchone() is not None:
                close_con(con)
                clicker = 0
                defining = 1
                return 'Logging in'
            else:
                close_con(con)
                return 'Username or password incorrect'
        else:
            return 'No Username or Password given'

#debounce login button
@program.callback(
    Output('log','n_clicks'),
    [Input('intervl','n_intervals')]
    )
def resets(nil):
    return 0


if __name__ == '__main__':
    defining = 0
    [start, L, L2, T, FM, FI, data] = Main.start()
    program.run_server(debug=True,use_reloader=False)


