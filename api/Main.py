#######################################################################################################################################################
##############################################################Imports##################################################################################
#######################################################################################################################################################
import sys
import dash
from dash.dependencies import Output, Input, State
import dash_core_components as dcc
import dash_html_components as html
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
import Adafruit_ADS1x15

#######################################################################################################################################################
##############################################################Initialize Program##################################################################################
#######################################################################################################################################################

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
                    ''',
                         style ={
                            'textFont': '18',
                            'color': colorst['text']
                            }
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
                    interval=150,
                    n_intervals=0
                    ),
                html.Label(id = 'prop')
                ]
            #end dropdown sub division
            )
        ]
    #end main division
    )


##############################################possible extra features
###dcc.Markdown('''**bold text** and *italics* [links](https://something.com) 'code' snip can write lists, quotes and more''')
###dcc.ConfirmDialog(id='confirm',message='warning, you sure you want to continue')
###dcc.Store(id='my-store', data='my-data':'data') must be used with callbacks
###dcc.location(id = 'url', refresh = False) href= "http://127.0.0.1:8050/page-2?a=test#quiz" pathname ="/page2" search ="?a=test" hash="#quiz"

###html.P('paragraph component')
###class is className
###style= 'color','fontSize','marginBottom','marginTop','width':%, 'display':'inline-block', 'float':'right'
###html.Table([html.Tr([html.Td(['x',html.Sup(2)]), html.Td(id='square')])])

#######################################################################################################################################################
##############################################################Tab Layout with Callbacks##################################################################################
#######################################################################################################################################################

class HaltCallback(Exception):
    pass

#stop server
@program.server.errorhandler(HaltCallback)
def handle_error(error):
    print(error, file=sys.stderr)
    return ('', 204)

#save button callback
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

#dropdown control
@program.callback(
    Output('prop','children'),
    [Input('property','value'),
    Input('fli','value'),
    Input('cdi','value')]
    )
def update_label(value,dist,rad):
    A1 = 0
    A2 = 0
    Pm = 0
    Pi = 0
    total = 0
    broadband = tsll.broadband
    infrared = tsll.infrared
    
    visible_light = broadband - infrared
    
    end3 = timer()
    t3 = end3 - start
    
    if(infrared/broadband <= 0.50 and infrared/broadband > 0):
        plux = ( (0.0304*(broadband/(2**10))) - ((0.062*(broadband/(2**10)))*((infrared/broadband)**1.4)))*(2**14)
    elif(infrared/broadband <= 0.61 and infrared/broadband > 0.50):
        plux = ( (0.0224*(broadband/(2**10))) - (0.031*(infrared/(2**10))))*(2**14)
    elif(infrared/broadband <= 0.80 and infrared/broadband > 0.61):
        plux = ( (0.0128*(broadband/(2**10))) - (0.0153*(infrared/(2**10))))*(2**14)
    elif(infrared/broadband <= 1.3 and infrared/broadband > 0.80):
        plux = ( (0.00146*(broadband/(2**10))) - (0.00112*(infrared/(2**10))))*(2**14)
    else:
        plux = 0
        
    T.append(t3)
    
    
    slux = adc.read_adc(0, gain=GAIN)
    L.append(slux)
    fm = ((np.max(L)-np.min(L))/(np.max(L)+np.min(L)))*100
    ave = np.average(L)
    if len(L)>1:
        for values in range(len(L)-1):
            xx = T[values+1] - T[values]
            checkers = (L[values + 1]+L[values])/2
            total += xx*(checkers)
            if checkers > ave:
                A1 += xx*((checkers)-ave)
                
        A2 = total - A1
        fi = (A1/(A1+A2))
        FM.append(fm)
        FI.append(fi)
        
        for lf in range(len(FM)):
            Pm += FM[lf] ** 3
            Pi += FI[lf] ** 3
            
        Pltm = math.pow(Pm/len(FM),1/3)
        Plti = math.pow(Pi/len(FI),1/3)
    
    cd = plux*(0.5**2)
    
    ster = 2*math.pi*(1-math.cos((35*math.pi)/(180)))
    
    flux = cd*ster
    
    #if len(L) > 1: 
     #   save(broadband,infrared,visible_light,plux,fm,fi,Pltm,Plti,flux, cd,t3)
    
    if value == 'nm':
        return '{} nm'.format(broadband)
    elif value == 'inf':
        return '{} nm'.format(infrared)
    elif value == 'VL':
        return '{} nm'.format(visible_light)
    elif value == 'lx':
        return '{} lx'.format(plux)
    elif value == 'flicm':
        return '{} %'.format(fm)
    elif value == 'flici':
        return '{} '.format(fi)
    elif value == 'Lflic':
        return '{} '.format(Pltm)
    elif value == 'lm':
        return '{} '.format(flux)
    elif value == 'cd':
        return '{} '.format(cd)
    

#tab control
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

#update broadband graph
@program.callback(
    Output('graph-1','figure'),
    [Input('inter','n_intervals')]
    )
def update_graph1(n):
        
    broadband = tsll.broadband
    
    end = timer()
    t = end - start

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

#update Illuminance graph
@program.callback(
    Output('graph-2','figure'),
    [Input('inter2','n_intervals')]
    )
def update_graph2(n):
        
    broadband = tsll.broadband
    infrared = tsll.infrared
    
    end2 = timer()
    t2 = end2 - start
    
    if(infrared/broadband <= 0.50 and infrared/broadband > 0):
        plux = ( (0.0304*(broadband/(2**10))) - ((0.062*(broadband/(2**10)))*((infrared/broadband)**1.4)))*(2**14)
    elif(infrared/broadband <= 0.61 and infrared/broadband > 0.50):
        plux = ( (0.0224*(broadband/(2**10))) - (0.031*(infrared/(2**10))))*(2**14)
    elif(infrared/broadband <= 0.80 and infrared/broadband > 0.61):
        plux = ( (0.0128*(broadband/(2**10))) - (0.0153*(infrared/(2**10))))*(2**14)
    elif(infrared/broadband <= 1.3 and infrared/broadband > 0.80):
        plux = ( (0.00146*(broadband/(2**10))) - (0.00112*(infrared/(2**10))))*(2**14)
    else:
        plux = 0

    data['Illuminance'].append(plux)
    data['Time2'].append(t2)
    
    return {
        'data':[{
            'type':'line',
            'x':data['Time2'],
            'y':data['Illuminance']
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
                'title':'Illuminance (lx)',
                'autorange':True    
                 },
            'plot_bgcolor':colorst['pbackground'],
            'paper_bgcolor':colorst['ebackground'],
            'font':colorst['text']
            }
        }

#update Flicker graph
@program.callback(
    Output('graph-3','figure'),
    [Input('inter3','n_intervals')]
    )
def update_graph3(n):
    A1 = 0
    A2 = 0
    Pm = 0
    Pi = 0
    total = 0
    broadband = tsll.broadband
    infrared = tsll.infrared
    
    visible_light = broadband - infrared
    
    end3 = timer()
    t3 = end3 - start
    
    if(infrared/broadband <= 0.50 and infrared/broadband > 0):
        plux = ( (0.0304*(broadband/(2**10))) - ((0.062*(broadband/(2**10)))*((infrared/broadband)**1.4)))*(2**14)
    elif(infrared/broadband <= 0.61 and infrared/broadband > 0.50):
        plux = ( (0.0224*(broadband/(2**10))) - (0.031*(infrared/(2**10))))*(2**14)
    elif(infrared/broadband <= 0.80 and infrared/broadband > 0.61):
        plux = ( (0.0128*(broadband/(2**10))) - (0.0153*(infrared/(2**10))))*(2**14)
    elif(infrared/broadband <= 1.3 and infrared/broadband > 0.80):
        plux = ( (0.00146*(broadband/(2**10))) - (0.00112*(infrared/(2**10))))*(2**14)
    else:
        plux = 0
        
    T.append(t3)
    
    
    slux = adc.read_adc(0, gain=GAIN)
    L.append(slux)
    fm = ((np.max(L)-np.min(L))/(np.max(L)+np.min(L)))*100
    ave = np.average(L)
    if len(L)>1:
        for values in range(len(L)-1):
            xx = T[values+1] - T[values]
            checkers = (L[values + 1]+L[values])/2
            total += xx*(checkers)
            if checkers > ave:
                A1 += xx*((checkers)-ave)
                
        A2 = total - A1
        fi = (A1/(A1+A2))
        FM.append(fm)
        FI.append(fi)
        
        for lf in range(len(FM)):
            Pm += FM[lf] ** 3
            Pi += FI[lf] ** 3
            
        Pltm = math.pow(Pm/len(FM),1/3)
        Plti = math.pow(Pi/len(FI),1/3)
    
    cd = plux*(0.5**2)
    
    ster = 2*math.pi*(1-math.cos((35*math.pi)/(180)))
    
    flux = cd*ster
    
    if len(L) > 1:
        f = open("Data.txt","a")
        f.write("LED_8.5W_806lm_95lm/W_Yellow_PHILIPS_68ma_UnderLoad,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d \n"% (broadband,infrared,visible_light,plux,fm,fi,Pltm,Plti,flux, cd,t3))
        
        #save(broadband,infrared,visible_light,plux,fm,fi,Pltm,Plti,flux, cd,t3)
    
    
    #plux = adc.read_adc(0, gain=GAIN)
    
    #end4 = timer()
    #t4 = end4 - start
    
    #L2.append(plux)
    #fm = ((np.max(L2)-np.min(L2))/(np.max(L2)+np.min(L2)))*100
    
    data['Flicker'].append(fm)
    data['Time3'].append(t3)
    
    return {
        'data':[{
            'type':'line',
            'x':data['Time3'],
            'y':data['Flicker']
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
                'title':'Flicker Modulation (%)',
                'autorange':True    
                 },
            'plot_bgcolor':colorst['pbackground'],
            'paper_bgcolor':colorst['ebackground'],
            'font':colorst['text']
            }
        }

#######################################################################################################################################################
##############################################################SQL functions##################################################################################
#######################################################################################################################################################

def save(broadband,infrared,VisibleLight,plux,fm,fi,pm,pi,flux, inten,t):
    con = connection('Light_test.db')
    q = con.cursor()
    try:
        query = "INSERT INTO Lights (Light_Type, Broadband, Infrared, Visible_Light, Illuminance, Flicker_Modulation, Flicker_Index, Long_Modulation, Long_Index, Flux, Intensity, Time)) VALUES ('LED',?,?,?,?,?,?,?,?,?,?,?);"
        q.execute(query, (broadband,infrared,VisibleLight,plux,fm,fi,pm, pi,flux, inten,t))
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
if __name__ == '__main__':
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

    L = []
    L2 = []
    T = []
    FM = []
    FI = []
    
    fi = 0
    fm = 0
    adc = Adafruit_ADS1x15.ADS1115()
    GAIN = 8

    data = {
        'Broadband': [],
        'Time': [],
        'Time2': [],
        'Illuminance': [],
        'Flicker': [],
        'Time3': []
        }
    
    program.run_server(debug=True)