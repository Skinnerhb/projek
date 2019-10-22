import sys
import dash
from dash.dependencies import Output, Input, State
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import numpy as np
import board
import busio
import adafruit_tsl2561 as tsl
from timeit import default_timer as timer
import time
import math
import sqlite3

from Program import program
from connect import connection, close_con
from lay import layout1, layout2, layout3
import caller

program.layout = html.Div([
    dcc.Location(id='url',pathname='/api/login', refresh = False),
    html.Div(id = 'patherr'),
    html.Div(id = 'hideme1', style={'display':'none'}),
    html.Div(id = 'hideme2', style={'display':'none'})
    ])


if __name__ == '__main__':
    program.run_server(debug=True)

