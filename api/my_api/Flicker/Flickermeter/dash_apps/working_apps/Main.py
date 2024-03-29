#######################################################################################################################################################
##############################################################Imports##################################################################################
#######################################################################################################################################################
from django_plotly_dash import DjangoDash
from dash.dependencies import Output, Input
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
import board
import busio
import adafruit_tsl2561 as tsl
from timeit import default_timer as timer
import time
import math
#import pandas as pd
import sqlite3
import Adafruit_ADS1x15
from django.utils import timezone

#######################################################################################################################################################
##############################################################Initialize Program##################################################################################
#######################################################################################################################################################
external_stylesheets = ['bWLwgP.css']
program = DjangoDash('Main',external_stylesheets = external_stylesheets)

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

#Database connection
def connection(db):
    db = '/home/pi/projek/api/my_api/Flicker/db.sqlite3'
    con = None
    try:
        con = sqlite3.connect(db)
    except con.Error as e:
        print(e)
    
    return con

#close connection
def close_con(con):
    con.close()

#######################################################################################################################################################
##############################################################Program Layout##################################################################################
#######################################################################################################################################################

def popup1():
    return 
    

program.layout = html.Div(
    #head division
    children=[
        html.Div(
            style={'backgroundColor': colorst['background'],
                   'font-size':'24px'
                   },
            #sub division with tabs
            children=[
                html.Div(
                    #start sub flux division
                    style={
                        'backgroundColor': colorst['background'],
                        'font-size':'24px',
                        'display':'inline-block',
                        'padding-left':'5%'
                        },
                    children=[
                        html.Label('  Enter distance from light source to device:  '),
                        html.Br(),
                        dcc.Input(
                            id = 'fli',
                            style = {
                                'font-size':'24px',
                                'padding-right':'10px'
                                },
                            placeholder='In meter',
                            type='text'
                            ),
                        ]
                    #end sub flux division
                    ),
                
                html.Div(
                    #start dropdown sub division
                    style={
                        'backgroundColor': colorst['background'],
                        'font-size':'24px',
                        'display':'inline-block',
                        'width':'25%',
                        'padding-left':'10%',
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
                        html.Label(id = 'prop', style={
                            'font-size':'24px',
                            'display':'inline-block',
                            })
                        ]
                    #end dropdown sub division
                    ),
                html.Button('Save',id='sabutton', n_clicks = 0, style={
                    'background-color': 'rgb(159, 213, 200)', 
                    'border': 'none',
                    'text-align':'center',
                    'text-decoration': 'none',
                    'display': 'inline-block',
                    'font-size': '24px',
                    'padding-left':'10px'
                    }),
                html.Button('Stop Saving',id='sasbutton', n_clicks = 0, style={
                    'background-color': 'rgb(159, 213, 200)', 
                    'border': 'none',
                    'text-align':'center',
                    'text-decoration': 'none',
                    'display': 'inline-block',
                    'font-size': '24px',
                    'padding-left':'10px'
                    }),
                html.Div(
                    children=[
                        html.Div([
                            html.Div(
                                children=[
                                    html.Button('Confirm',id='confirmbutton', n_clicks = 0, style={
                                        'background-color': 'rgb(159, 213, 200)',
                                        'border': 'none',
                                        'text-align':'left',
                                        'text-decoration': 'none',
                                        'display': 'inline-block',
                                        'font-size': '24px',
                                        'padding-left':'10px'
                                        }),
                                    html.Br(),
                                    html.Label('  Confirm Username and enter light ID and light type:  '),
                                    html.Br(),
                                    dcc.Input(
                                        id = 'userna',
                                        style = {
                                            'font-size':'24px',
                                            'padding-right':'10px'
                                            },
                                        placeholder='Username',
                                        debounce=True,
                                        type='text'
                                        ),
                                    html.Br(),
                                    dcc.Input(
                                        id = 'lighterid',
                                        style = {
                                            'font-size':'24px',
                                            'padding-right':'10px'
                                            },
                                        placeholder='Light ID ex. Light1',
                                        debounce=True,
                                        type='text'
                                        ),
                                    html.Br(),
                                    dcc.Input(
                                        id = 'lightertype',
                                        style = {
                                            'font-size':'24px',
                                            'padding-right':'10px'
                                            },
                                        placeholder='Light type ex. Flourescent',
                                        debounce = True,
                                        type='text'
                                        ),
                                    html.Br(),
                                    html.Button('Close',id='closebutton', n_clicks = 0, style={
                                        'background-color': 'rgb(159, 213, 200)',
                                        'border': 'none',
                                        'text-align':'left',
                                        'text-decoration': 'none',
                                        'display': 'inline-block',
                                        'font-size': '24px',
                                        'padding-left':'10px'
                                        }),
                                    html.Br(),
                                    html.Div(
                                        id = 'lack',
                                        style = {
                                            'text-align':'center',
                                            'font-size':'24px'
                                            },
                                        )
                                    ],
                                style = {
                                    'margin': '40px',
                                    'height':'400px',
                                    'padding':'40px',
                                    'background-color':'white',
                                    'text-align':'center',
                                    }
                                )
                            ]),
                        ],
                    id= 'popup1',
                    style = {
                        'display':'none',
                        'font-size':'24px',
                        'position': 'fixed',
                        'z-index': '1002',
                        'left':'0',
                        'top':'0',
                        'width':'100%',
                        'height':'100%',
                        'background-color': colorst['background']
                        }
                    ),
                dcc.Tabs(
                    id='tabbing',
                    value='tab-1',
                    children=[
                        dcc.Tab(
                            label='Broadband',
                            value='tab-1',
                            children =[
                                html.Div(
                                    id ='blom1',
                                    style= {
                                        'display': 'inline-block',
                                        },
                                    children = [
                                        html.Button('Start', id='sbutton1', style={
                                            'background-color': 'rgb(159, 213, 200)', 
                                            'border': 'none',
                                            'text-align':'center',
                                            'text-decoration': 'none',
                                            'font-size': '24px',
                                            'padding-right':'20px'
                                            
                                            }),
                                        html.Button('Reset', id='pbutton1', n_clicks = 0 , style={
                                            'background-color': 'rgb(159, 213, 200)', 
                                            'border': 'none',
                                            'text-align':'center',
                                            'text-decoration': 'none',
                                            'font-size': '24px',
                                            
                                            }),
                                        ]
                                    ),
                                html.Br(),
                                html.H2(
                                    children= 'Broadband measurent (nm)',
                                    style ={
                                        'textAlign': 'center',
                                        'color': colorst['text'],
                                        'font-size': '28px',
                                        }
                                    ),
                                dcc.Graph(
                                    id = 'graph-1'
                                    ),
                                dcc.Interval(
                                    id='inter',
                                    interval=1000,
                                    n_intervals=0
                                    )
                                ]
                            ),
                        html.Div(id='graphing1'),
                        dcc.Tab(
                            label='Illuminance',
                            value='tab-2',
                            children =[
                                html.Div(
                                    id ='blom2',
                                    style= {
                                        'display': 'inline-block',
                                        },
                                    children = [
                                        html.Button('Start', id='sbutton2', style={
                                            'background-color': 'rgb(159, 213, 200)', 
                                            'border': 'none',
                                            'text-align':'center',
                                            'text-decoration': 'none',
                                            'font-size': '24px',
                                            'padding-right':'20px'
                                            
                                            }),
                                        html.Button('Reset', id='pbutton2', n_clicks = 0 , style={
                                            'background-color': 'rgb(159, 213, 200)', 
                                            'border': 'none',
                                            'text-align':'center',
                                            'text-decoration': 'none',
                                            'font-size': '24px',
                                            
                                            }),
                                        ]
                                    ),
                                html.Br(),
                                html.H2(
                                    children= 'Illuminance measurent (lx)',
                                    style ={
                                        'textAlign': 'center',
                                        'color': colorst['text'],
                                        'font-size': '28px',
                                        }
                                    ),
                                dcc.Graph(
                                    id = 'graph-2'
                                    ),
                                dcc.Interval(
                                    id='inter2',
                                    interval=1000,
                                    n_intervals=0
                                    )
                                ]
                            ),
                        html.Div(id='graphing2'),
                        dcc.Tab(
                            label='Flicker',
                            value='tab-3',
                            children =[
                                html.Div(
                                    id ='blom3',
                                    style= {
                                        'display': 'inline-block',
                                        },
                                    children = [
                                        html.Button('Start', id='sbutton3', style={
                                            'background-color': 'rgb(159, 213, 200)', 
                                            'border': 'none',
                                            'text-align':'center',
                                            'text-decoration': 'none',
                                            'font-size': '24px',
                                            'padding-right':'20px'
                                            
                                            }),
                                        html.Button('Reset', id='pbutton3', n_clicks = 0 , style={
                                            'background-color': 'rgb(159, 213, 200)', 
                                            'border': 'none',
                                            'text-align':'center',
                                            'text-decoration': 'none',
                                            'font-size': '24px',
                                            
                                            }),
                                        ]
                                    ),
                                html.Br(),
                                html.H2(
                                    children= 'Flicker measurent (%)',
                                    style ={
                                        'textAlign': 'center',
                                        'color': colorst['text'],
                                        'font-size': '28px',
                                        }
                                    ),
                                dcc.Graph(
                                    id = 'graph-3'
                                    ),
                                dcc.Interval(
                                    id='inter3',
                                    interval=1000,
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
        dcc.Interval(
            id = 'inter5',
            interval = 500,
            n_intervals = 0
            ),
        html.Div(id='Datastore',
                 style = {'display':'none'},
                 children = [
                     dcc.Interval(
                         id = 'inter4',
                         interval = 500,
                         n_intervals = 0
                         ),
            
            ]),
        ]
    #end main division
    )

#######################################################################################################################################################
##############################################################Tab Layout with Callbacks##################################################################################
#######################################################################################################################################################


# def datacon(dist,tslll,adcc):
#     A1 = 0
#     A2 = 0
#     Pm = 0
#     Pi = 0
#     fi = 0
#     Pltm = 0
#     total = 0
#     broadband = tslll.broadband
#     infrared = tslll.infrared
#     
#     visible_light = broadband - infrared
#     
#     end3 = timer()
#     t3 = end3 - start
#     
#     if(infrared/broadband <= 0.50 and infrared/broadband > 0):
#         plux = ( (0.0304*(broadband/(2**10))) - ((0.062*(broadband/(2**10)))*((infrared/broadband)**1.4)))*(2**14)
#     elif(infrared/broadband <= 0.61 and infrared/broadband > 0.50):
#         plux = ( (0.0224*(broadband/(2**10))) - (0.031*(infrared/(2**10))))*(2**14)
#     elif(infrared/broadband <= 0.80 and infrared/broadband > 0.61):
#         plux = ( (0.0128*(broadband/(2**10))) - (0.0153*(infrared/(2**10))))*(2**14)
#     elif(infrared/broadband <= 1.3 and infrared/broadband > 0.80):
#         plux = ( (0.00146*(broadband/(2**10))) - (0.00112*(infrared/(2**10))))*(2**14)
#     else:
#         plux = 0
#         
#     timeD['T'].append(t3)
#     T = timeD['T']
#     slux = adcc.read_adc(0, gain=GAIN)
#     timeD['L'].append(slux)
#     L = timeD['L']
#     fm = ((np.max(L)-np.min(L))/(np.max(L)+np.min(L)))*100
#     ave = np.average(L)
#     if len(L)>1:
#         for values in range(len(L)-1):
#             xx = T[values+1] - T[values]
#             checkers = (L[values + 1]+L[values])/2
#             total += xx*(checkers)
#             if checkers > ave:
#                 A1 += xx*((checkers)-ave)
#                 
#         A2 = total - A1
#         fi = (A1/(A1+A2))
#         timeD['FM'].append(fm)
#         FM = timeD['FM']
#         timeD['FI'].append(fi)
#         FI = timeD['FI']
#         
#         for lf in range(len(FM)):
#             Pm += FM[lf] ** 3
#             Pi += FI[lf] ** 3
#             
#         Pltm = math.pow(Pm/len(FM),1/3)
#         #Plti = math.pow(Pi/len(FI),1/3)
#     
#     if dist is not None:
#         try:
#             cd = plux*(float(dist)**2)
#             ster = 2*math.pi*(1-math.cos((35*math.pi)/(180)))
#     
#             flux = cd*ster
#         except:
#             cd = 0
#             ster = 2*math.pi*(1-math.cos((35*math.pi)/(180)))
#     
#             flux = cd*ster
#     else:
#         cd = 0
#         ster = 2*math.pi*(1-math.cos((35*math.pi)/(180)))
# 
#         flux = cd*ster
#     return infrared,broadband,visible_light,t3,plux,flux,fm,fi,cd,Pltm

@program.callback(
    Output('popup1','style'),
    [Input('sabutton','n_clicks'),
     Input('inter5','n_intervals')]
    )
def savingly(nn, n):
    if nn is not None:
        if (nn % 2) == 1:
            return {'display':'block'}
        else:
            return {'display':'none'}

@program.callback(
    Output('sabutton','n_clicks'),
    [Input('closebutton','n_clicks')]
    )
def closesav(nc):
    if nc:
        return 0


@program.callback(
    Output('closebutton','n_clicks'),
    [Input('lack','children'),
     Input('inter4','n_intervals'),
     Input('lighterid','value'),
     Input('fli','value')
     ]
    )
def savingly33(dat,n,litd,dist):
    if dat == 'Saving started':
        timeD['start4'].append(timer())
        end = timer()
        ti = end - timeD['start4'][0]
        A1 = 0
        A2 = 0
        Pm = 0
        Pi = 0
        fi = 0
        Pltm = 0
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
            
        timeD['T'].append(t3)
        T = timeD['T']
        slux = adc.read_adc(0, gain=GAIN)
        timeD['L'].append(slux)
        L = timeD['L']
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
                timeD['FM2'].append(fm)
                FM = timeD['FM2']
                timeD['FI2'].append(fi)
                FI = timeD['FI2']
                
                for lf in range(len(FM)):
                    Pm += FM[lf] ** 3
                    Pi += FI[lf] ** 3
                    
                Pltm = math.pow(Pm/len(FM),1/3)
                #Plti = math.pow(Pi/len(FI),1/3)
            
            if dist is not None:
                try:
                    cd = plux*(float(dist)**2)
                    ster = 2*math.pi*(1-math.cos((35*math.pi)/(180)))
            
                    flux = cd*ster
                except:
                    cd = 0
                    ster = 2*math.pi*(1-math.cos((35*math.pi)/(180)))
            
                    flux = cd*ster
            else:
                cd = 0
                ster = 2*math.pi*(1-math.cos((35*math.pi)/(180)))

                flux = cd*ster
        try:
            db = '/home/pi/projek/api/my_api/Flicker/db.sqlite3'
            con = connection(db)
            q = con.cursor()
            query2 = "INSERT INTO Flickermeter_data (Broadband, Infrared, VisibleLight, Illuminance, FlickerModulation, FlickerIndex, LongFlickerModulation, LongFlickerIndex, Luminance, Flux, Time, LightID_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
            q.execute(query2, (broadband,infrared,visible_light,plux,fm,fi,Pltm,0,flux,cd,ti,litd))
            con.commit()
            close_con(con)
            return 0
        except con.Error as e:
            print(e)
            close_con(con)
            return 0
        
    
@program.callback(
    Output('lack','children'),
    [Input('confirmbutton','n_clicks'),
     Input('userna','value'),
     Input('lighterid','value'),
     Input('lightertype','value'),
     Input('sasbutton','n_clicks')
     ]
    )
def savingly2(nn1,userss,lid,lty,nn2):
    if nn2:
        return 'Saving Stopped'
        
    if nn1:
        print('entered')
        db = '/home/pi/projek/api/my_api/Flicker/db.sqlite3'
        con = connection(db)
        q = con.cursor()
        try:
            query = "SELECT id FROM auth_user WHERE username = ?"
            q.execute(query, (userss,))
            useri = q.fetchone()
            if useri is not None:
                userii = useri[0]
                close_con(con)
                try:
                    db = '/home/pi/projek/api/my_api/Flicker/db.sqlite3'
                    con = connection(db)
                    q = con.cursor()
                    query3 = "SELECT LightID FROM Flickermeter_lighti WHERE UserID_id = ?"
                    q.execute(query3, (lid,))
                    lidd = q.fetchone()
                    if lidd is not None:
                        close_con(con)
                        return 'Light ID already exists'
                    else:
                        close_con(con)
                        try:                            
                            db = '/home/pi/projek/api/my_api/Flicker/db.sqlite3'
                            con = connection(db)
                            q = con.cursor()
                            if lid is not None and lty is not None:
                                timen = timezone.now()
                                query2 = "INSERT INTO Flickermeter_lighti (LightID, LightType, date_created, UserID_id) VALUES (?, ?, ?, ?)"
                                q.execute(query2, (lid,lty,timen,userii))
                                con.commit()
                                close_con(con)
                                return 'Saving started'
                            else:
                                print('Light ID or light type not entered')
                                return 'Light ID or light type not entered'
                        except con.Error as e:
                            print(e)
                            close_con(con)
                            return e
                except con.Error as e:
                    print(e)
                    close_con(con)
                    return e
            else:
                print('username not entered')
                return 'Username not entered'
        except con.Error as e:
            print(e)
            close_con(con)
            return e


#dropdown control
@program.callback(
    Output('prop','children'),
    [Input('property','value'),
     Input('fli','value')
    ]
    )
def update_label(value, dist):
    A1 = 0
    A2 = 0
    Pm = 0
    Pi = 0
    fi = 0
    Pltm = 0
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
        
    timeD['T2'].append(t3)
    T = timeD['T2']
    slux = adc.read_adc(0, gain=GAIN)
    timeD['L2'].append(slux)
    L = timeD['L2']
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
        timeD['FM2'].append(fm)
        FM = timeD['FM2']
        timeD['FI2'].append(fi)
        FI = timeD['FI2']
        
        for lf in range(len(FM)):
            Pm += FM[lf] ** 3
            Pi += FI[lf] ** 3
            
        Pltm = math.pow(Pm/len(FM),1/3)
        #Plti = math.pow(Pi/len(FI),1/3)
    
    if dist is not None:
        try:
            cd = plux*(float(dist)**2)
            ster = 2*math.pi*(1-math.cos((35*math.pi)/(180)))
    
            flux = cd*ster
        except:
            cd = 0
            ster = 2*math.pi*(1-math.cos((35*math.pi)/(180)))
    
            flux = cd*ster
    else:
        cd = 0
        ster = 2*math.pi*(1-math.cos((35*math.pi)/(180)))

        flux = cd*ster
    
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
    [Input('inter','n_intervals'),
     Input('sbutton1','n_clicks')
     ]
    )
def update_graph1(n,nn1):    
    if nn1 is None or nn1 == 0:
        broadband = tsll.broadband
        timeD['Time2'].clear()
        timeD['Time2'].append(0)
        timeD['n3'].clear()
        timeD['n3'].append(0)
        timeD['start1'].clear()
        timeD['BnD'].clear()
        timeD['BnD'].append(broadband)
        return {
            'data':[{
                'type':'scatter',
                'x':timeD['Time2'],
                'y':timeD['BnD']
                }],
            'layout':{
                'xaxis':{
                    'title':'Time (s)',
                    'rangeslider':{
                        'visible':True
                        },
                    'autorange': True,
                    },
                'yaxis':{
                    'title':'Broadband (nm)',
                    'autorange':True,    
                     },
                'plot_bgcolor':colorst['pbackground'],
                'paper_bgcolor':colorst['ebackground'],
                'font':colorst['text'],
                'font-size':'24px'
                }
            }
    
    if nn1 is not None and nn1 >= 1:
        broadband = tsll.broadband
        if timeD['n3'][0] == 0:
            timeD['start1'].append(timer())
            timeD['n3'][0] = 1
            timeD['Time2'].clear()
            timeD['BnD'].clear()
        elif timeD['n3'][0] == 1:
            end = timer()
            timeD['Time2'].append(end-timeD['start1'][0])
            timeD['BnD'].append(broadband)
            
            if timeD['Time2'][-1] < 20:
                return {
                    'data':[{
                        'type':'line',
                        'x':timeD['Time2'],
                        'y':timeD['BnD']
                        }],
                    'layout':{
                        'xaxis':{
                            'title':'Time (s)',
                            'rangeslider':{
                                'visible':True
                                },
                            'autorange': True,
                            },
                        'yaxis':{
                            'title':'Broadband (nm)',
                            'autorange':True,    
                             },
                        'plot_bgcolor':colorst['pbackground'],
                        'paper_bgcolor':colorst['ebackground'],
                        'font':colorst['text'],
                        'font-size':'24px'
                        }
                    }
            elif timeD['Time2'][-1] >= 20:
                return {
                    'data':[{
                        'type':'line',
                        'x':timeD['Time2'][-19:-1],
                        'y':timeD['BnD'][-19:-1]
                        }],
                    'layout':{
                        'xaxis':{
                            'title':'Time (s)',
                            'rangeslider':{
                                'visible':True
                                },
                            'autorange': True,
                            },
                        'yaxis':{
                            'title':'Broadband (nm)',
                            'autorange':True,    
                             },
                        'plot_bgcolor':colorst['pbackground'],
                        'paper_bgcolor':colorst['ebackground'],
                        'font':colorst['text'],
                        'font-size':'24px'
                        }
                    }

@program.callback(
    Output('sbutton1','n_clicks'),
    [Input('pbutton1','n_clicks')
     ]
    )
def resetgraphs1(n):
    return 0

@program.callback(
    Output('sbutton2','n_clicks'),
    [Input('pbutton2','n_clicks')
     ]
    )
def resetgraphs2(n):
    return 0

@program.callback(
    Output('sbutton3','n_clicks'),
    [Input('pbutton3','n_clicks')
     ]
    )
def resetgraphs3(n):
    return 0

#update Illuminance graph
@program.callback(
    Output('graph-2','figure'),
    [Input('inter2','n_intervals'),
     Input('sbutton2','n_clicks')]
    )
def update_graph2(n,nn1):
    if nn1 is None or nn1 == 0:
        broadband = tsll.broadband
        infrared = tsll.infrared
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
            
        timeD['Time3'].clear()
        timeD['Time3'].append(0)
        timeD['n4'].clear()
        timeD['n4'].append(0)
        timeD['start2'].clear()
        timeD['LnD'].clear()
        timeD['LnD'].append(plux)
        return {
            'data':[{
                'type':'scatter',
                'x':timeD['Time3'],
                'y':timeD['LnD']
                }],
            'layout':{
                'xaxis':{
                    'title':'Time (s)',
                    'rangeslider':{
                        'visible':True
                        },
                    'autorange': True,
                    },
                'yaxis':{
                    'title':'Illuminance (lx)',
                    'autorange':True,    
                     },
                'plot_bgcolor':colorst['pbackground'],
                'paper_bgcolor':colorst['ebackground'],
                'font':colorst['text'],
                'font-size':'24px'
                }
            }
    
    if nn1 is not None and nn1 >= 1:
        broadband = tslll.broadband
        infrared = tslll.infrared
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
        if timeD['n4'][0] == 0:
            timeD['start2'].append(timer())
            timeD['n4'][0] = 1
            timeD['Time3'].clear()
            timeD['LnD'].clear()
        elif timeD['n4'][0] == 1:
            end = timer()
            timeD['Time3'].append(end-timeD['start2'][0])
            timeD['LnD'].append(plux)
            
            if timeD['Time3'][-1] < 20:
                return {
                    'data':[{
                        'type':'line',
                        'x':timeD['Time3'],
                        'y':timeD['LnD']
                        }],
                    'layout':{
                        'xaxis':{
                            'title':'Time (s)',
                            'rangeslider':{
                                'visible':True
                                },
                            'autorange': True,
                            },
                        'yaxis':{
                            'title':'Illuminance (lx)',
                            'autorange':True,    
                             },
                        'plot_bgcolor':colorst['pbackground'],
                        'paper_bgcolor':colorst['ebackground'],
                        'font':colorst['text'],
                        'font-size':'24px'
                        }
                    }
            elif timeD['Time3'][-1] >= 20:
                return {
                    'data':[{
                        'type':'line',
                        'x':timeD['Time3'][-19:-1],
                        'y':timeD['LnD'][-19:-1]
                        }],
                    'layout':{
                        'xaxis':{
                            'title':'Time (s)',
                            'rangeslider':{
                                'visible':True
                                },
                            'autorange': True,
                            },
                        'yaxis':{
                            'title':'Illuminance (lx)',
                            'autorange':True,    
                             },
                        'plot_bgcolor':colorst['pbackground'],
                        'paper_bgcolor':colorst['ebackground'],
                        'font':colorst['text'],
                        'font-size':'24px'
                        }
                    }

#update Flicker graph
@program.callback(
    Output('graph-3','figure'),
    [Input('inter3','n_intervals'),
     Input('sbutton3','n_clicks')
     ]
    )
def update_graph3(n,nn1):
    if nn1 is None or nn1 == 0:
        slux = adc.read_adc(0, gain=GAIN)
        timeD['L'].append(slux)
        L = timeD['L']
        fm = ((np.max(L)-np.min(L))/(np.max(L)+np.min(L)))*100
        timeD['Time4'].clear()
        timeD['Time4'].append(0)
        timeD['n5'].clear()
        timeD['n5'].append(0)
        timeD['start3'].clear()
        timeD['FnD'].clear()
        timeD['FnD'].append(fm)
        return {
            'data':[{
                'type':'scatter',
                'x':timeD['Time4'],
                'y':timeD['FnD']
                }],
            'layout':{
                'xaxis':{
                    'title':'Time (s)',
                    'rangeslider':{
                        'visible':True
                        },
                    'autorange': True,
                    },
                'yaxis':{
                    'title':'Flicker Modulation (%)',
                    'autorange':True,    
                     },
                'plot_bgcolor':colorst['pbackground'],
                'paper_bgcolor':colorst['ebackground'],
                'font':colorst['text'],
                'font-size':'24px'
                }
            }
    
    if nn1 is not None and nn1 >= 1:
        slux = adcc.read_adc(0, gain=GAIN)
        timeD['L'].append(slux)
        L = timeD['L']
        fm = ((np.max(L)-np.min(L))/(np.max(L)+np.min(L)))*100
        if timeD['n5'][0] == 0:
            timeD['start3'].append(timer())
            timeD['n5'][0] = 1
            timeD['Time4'].clear()
            timeD['FnD'].clear()
        elif timeD['n5'][0] == 1:
            end = timer()
            timeD['Time4'].append(end-timeD['start3'][0])
            timeD['FnD'].append(fm)
            
            if timeD['Time4'][-1] < 20:
                return {
                    'data':[{
                        'type':'line',
                        'x':timeD['Time4'],
                        'y':timeD['FnD']
                        }],
                    'layout':{
                        'xaxis':{
                            'title':'Time (s)',
                            'rangeslider':{
                                'visible':True
                                },
                            'autorange': True,
                            },
                        'yaxis':{
                            'title':'Flicker Modulation (%)',
                            'autorange':True,    
                             },
                        'plot_bgcolor':colorst['pbackground'],
                        'paper_bgcolor':colorst['ebackground'],
                        'font':colorst['text'],
                        'font-size':'24px'
                        }
                    }
            elif timeD['Time4'][-1] >= 20:
                return {
                    'data':[{
                        'type':'line',
                        'x':timeD['Time4'][-19:-1],
                        'y':timeD['FnD'][-19:-1]
                        }],
                    'layout':{
                        'xaxis':{
                            'title':'Time (s)',
                            'rangeslider':{
                                'visible':True
                                },
                            'autorange': True,
                            },
                        'yaxis':{
                            'title':'Flicker Modulation (%)',
                            'autorange':True,    
                             },
                        'plot_bgcolor':colorst['pbackground'],
                        'paper_bgcolor':colorst['ebackground'],
                        'font':colorst['text'],
                        'font-size':'24px'
                        }
                    }

#######################################################################################################################################################
##############################################################Start Program and Threads##################################################################################
#######################################################################################################################################################

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

adc = Adafruit_ADS1x15.ADS1115()
GAIN = 8


data = {
    'Infrared': [],
    'Broadband': [],
    'VisibleLight':[],
    'Time': [],
    'Illuminance': [],
    'Flux':[],
    'FlickerModulation': [],
    'FlickerIndex':[],
    'Intensity': [],
    'LongTermFlicker':[],
    }

timeD = {
    'Time2': [],
    'BnD': [],
    'Time3': [],
    'LnD': [],
    'Time4': [],
    'FnD': [],
    'n3': [0],
    'n4': [0],
    'n5': [0],
    'start1': [],
    'start2': [],
    'start3': [],
    'start4':[],
    'L' : [],
    'T' : [],
    'FM' : [],
    'FI' : [],
    'L2' : [],
    'T2' : [],
    'FM2' : [],
    'FI2' : [],
    }

