#######################################################################################################################################################
##############################################################Imports##################################################################################
#######################################################################################################################################################
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

#######################################################################################################################################################
##############################################################Initialize Program##################################################################################
#######################################################################################################################################################

program = dash.Dash(__name__)

colorst = {
    'background':'#b3c4c4',
    'pbackground':'#ffffff',
    'ebackground':'#f2f2f2',
    'text': '#000000'
    }

#X = deque(maxlen=50)
#Y = deque(maxlen=50)
#X.append(1)
#Y.append(1)

#######################################################################################################################################################
##############################################################Program Layout##################################################################################
#######################################################################################################################################################

program.layout = html.Div(
    #head division
    children=[
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
            #start sub flux division
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
            #en sub flux division
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
            )
        ]
    #end main division
    )


##################################################possible extra features
###dcc.Markdown('''**bold text** and *italics* [links](https://something.com) 'code' snip can write lists, quotes and more''')
###dcc.Tabs(id ="tabs",value='tab-1',children=[dcc.Tab(label='Tab one',value='tab-1'), dcc.Tab(label='Tan two',value='tab-2')]), htlm.Div(tid='tabs-content')
###dcc.ConfirmDialog(id='confirm',message='warning, you sure you want to continue')
###dcc.Store(id='my-store', data='my-data':'data') must be used with callbacks
###dcc.location(id = 'url', refresh = False) href= "http://127.0.0.1:8050/page-2?a=test#quiz" pathname ="/page2" search ="?a=test" hash="#quiz"
#html.Label('Select Property'),
        #dcc.Dropdown(
        #options=[
        #{'label':'Broadband (nm)','value':'nm'},
        #{'label':'Illuminance (lx)','value':'lx'},
        #{'label':'Flicker (%)','value':'flic'}
        #],
        #value=['nm'],
        #multi=True
        #),


###html.P('paragraph component')
###class is className
###style= 'color','fontSize','marginBottom','marginTop','width':%, 'display':'inline-block', 'float':'right'
###html.Table([html.Tr([html.Td(['x',html.Sup(2)]), html.Td(id='square')])])

#######################################################################################################################################################
##############################################################Tab Layout with Callbacks##################################################################################
#######################################################################################################################################################

class HaltCallback(Exception):
    pass

@program.server.errorhandler(HaltCallback)
def handle_error(error):
    print(error, file=sys.stderr)
    return ('', 204)

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

@program.callback(
    Output('tab-stuff','children'),
    [Input('tabbing','value')]
    )
def showcont(tab):
    if tab == 'tab-1':
        return
    elif tab == 'tab-2':
        return
    elif tab == 'tab-3':
        return

@program.callback(
    Output('graph-1','figure'),
    [Input('inter','n_intervals')]
    )
def update_graph1(n):
        
    broadband = tsll.broadband
    infrared = tsll.infrared
    
    end = timer()
    t = end - start
    T.append(t)
    B.append(broadband)
    I.append(infrared)

    data['Broadband'].append(broadband)
    data['Time'].append(t)
    
    return {
        'data':[{
            'type':'line',
            'x':data['Time'],
            'y':data['Broadband']
            }],
        'layout':{
            'xaxis':{
                'title':'Time (s)',
                'rangeslider':{
                    'visible':True
                    },
                'autorange': True
                },
            'yaxis':{
                'title':'Broadband (nm)',
                 'autorange':True    
                 },
            'plot_bgcolor':colorst['pbackground'],
            'paper_bgcolor':colorst['ebackground'],
            'font':colorst['text']
            }
        }




#######################################################################################################################################################
##############################################################Sensor functions##################################################################################
#######################################################################################################################################################

def senseout(start,tsll):
    end = 0
    broadband = tsll.broadband
    infrared = tsll.infrared
    
    #B.append(broadband)
    #I.append(infrared)
    
    #if(infrared/broadband <= 0.50 and infrared/broadband > 0):
     #   plux = ( (0.0304*(broadband/(2**10))) - ((0.062*(broadband/(2**10)))*((infrared/broadband)**1.4)))*(2**14)
    #elif(infrared/broadband <= 0.61 and infrared/broadband > 0.50):
     #   plux = ( (0.0224*(broadband/(2**10))) - (0.031*(infrared/(2**10))))*(2**14)
    #elif(infrared/broadband <= 0.80 and infrared/broadband > 0.61):
     #   plux = ( (0.0128*(broadband/(2**10))) - (0.0153*(infrared/(2**10))))*(2**14)
    #elif(infrared/broadband <= 1.3 and infrared/broadband > 0.80):
     #   plux = ( (0.00146*(broadband/(2**10))) - (0.00112*(infrared/(2**10))))*(2**14)
    #else:
     #   plux = 0
        
    #L.append(plux)
    
    #time program
    end = timer()
    t = end - start
    #T.append(t)
    return broadband,t
    
    #fm = ((numpy.max(L)-numpy.min(L))/(numpy.max(L)+numpy.min(L)))*100
    #ave = numpy.average(L)
    #for values in range(len(L)-1):
     #   xx = T[c+1] - T[c]
      #  total += xx*((L[c+1] + L[c])/2)
       # if values > ave:
        #    A1 += xx*(((L[c + 1] - ave)+(L[c] - ave))/2)
        #c += 1
            
    #A2 = total - A1
    #fi = (A1/(A1+A2))
    #FM.append(fm/100)
    #FI.append(fi)
    #ss += 1
    
    #if ss == 12:
     #   for lf in range(1,12):
      #      Pm += FM[lf-1] ** 3
       #     Pi += FI[lf-1] ** 3
            
        #Pltm = math.pow(Pm/12,1/3)
        #Plti = math.pow(Pi/12,1/3)
        #ss = 0
    
def check():

    #create the i2c bus
    i2c = busio.I2C(board.SCL, board.SDA)

    #create TSL2561 instance, passing in the I2C bus
    tsll = tsl.TSL2561(i2c)

    #print chip info:
    print("Chip ID = {}".format(tsll.chip_id))
    print("Enabled = {}".format(tsll.enabled))
    print("Gain = {}".format(tsll.gain))
    print("Intergration time = {}".format(tsll.integration_time))

    print("Configuring TSL2561....")

    #enable light sensor
    tsll.enable = True
    time.sleep(1)

    #set gain 0=1x 1=16x
    tsll.gain= 0

    #Set integration time (0 = 13.7ms, 1 = 101ms, 2 = 402ms, or 3 = manual)
    tsll.integration_time = 2

    print("Getting readings...")
    time.sleep(1)

    B = []
    I = []
    L = []
    #F = []
    T = []

    #first = 0
    #i = 0
    start = timer()
    
    #dist = 0
    #radi = 0
    
    #cd = lux*(dista**2)
    #flux = lux*4*math.pi*(radi**2)
    for i in range(1,100):
        [b,t] = senseout(start,tsll)
        B.append(b)
        T.append(t)
    
    t = 0
    #disable sensor
    tsll.enabled=False
    
    return B,T


#######################################################################################################################################################
##############################################################SQL functions##################################################################################
#######################################################################################################################################################

def save(broadband,infrared,plux,fm,fi,t):
    con = connection('Flickermeter.db')
    q = con.cursor()
    try:
        query = "INSERT INTO Data (LightID,Broadband,Infrared,Illuminance,Time) VALUES (?,?,?,?,?);"
        q.execute(query, (lit,broadband,infrared,plux,t))
        con.commit()
        close_con(con)
    except con.Error as e:
        print(e)
        close_con(con)

#######################################################################################################################################################
##############################################################Start Program and Threads##################################################################################
#######################################################################################################################################################

###x = threading.Thread(target=thread_function,args(1,))
###x.start()

if __name__=='__main__':
    #create the i2c bus
    i2c = busio.I2C(board.SCL, board.SDA)

    #create TSL2561 instance, passing in the I2C bus
    tsll = tsl.TSL2561(i2c)

    #print chip info:
    print("Chip ID = {}".format(tsll.chip_id))
    print("Enabled = {}".format(tsll.enabled))
    print("Gain = {}".format(tsll.gain))
    print("Intergration time = {}".format(tsll.integration_time))

    print("Configuring TSL2561....")

    #enable light sensor
    tsll.enable = True
    time.sleep(1)

    #set gain 0=1x 1=16x
    tsll.gain= 0

    #Set integration time (0 = 13.7ms, 1 = 101ms, 2 = 402ms, or 3 = manual)
    tsll.integration_time = 2

    print("Getting readings...")
    time.sleep(1)
    
    start = timer()
    
    data = {
        'Broadband': [],
        'Time': []
        '': []
        }
    
    #data['Broadband'] = deque(maxlen=50)
    #data['Time'] = deque(maxlen=50)
    
    program.run_server(debug=True, use_reloader=False)#, dev_tools_ui=True, dev_tools_props_check=False)#, use_reloader=False)
    
    