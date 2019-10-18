import dash
from dash.dependencies import *
import dash_core_components as dcc
import dash_html_components as html
from timeit import default_timer as timer
import plotly.graph_objs as go
import time
import board
import busio
import adafruit_tsl2561 as tsl
import numpy as np
import pandas as pd
import math
import sqlite3

global sens
sens = pd.DataFrame(columns=['time','temp'])

#app layout
def layoutb():
    layout = html.Div(html.H1('Flickermeter'),
                      #html.Div(dcc.interval(id='refresh', interval=500)),
                      #dcc.Input(id='input',value='Enter something', type='text'),
                      html.Div(id='output')
                      )
#sensor graph
def gplot(sens):
    plot = dcc.Graph(id = 'preload',
                     figure={
                         'data': [go.plot(name='output',
                                          x=sens['time'],
                                          y=sens['temp'])],
                         'layout': go.layout(
                             title='Broadband (nm)'
                             )
                         },
                     style={
                         'width':'80%','float':'right'
                         }
                     )
    return plot

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

#main function
#def main():
    #global flag
    #flag = 1
    #check()

def check():
    #global flag
    global B
    global T

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
    F = []
    T = []

    first = 0
    i = 0
    start = timer()
    BnD(tsll,start,i,first)
    
    t = 0
    #disable sensor
    tsll.enabled=False

#Broadband plot data
def getBT(B,T):
    b = []
    t3 = []
    i = 0
    j = 0
    if len(B) >= 5 and len(B) < 50:
        for i in range(5,len(B)-1):
            b.append(B[i])
            t3.append(T[i])
    elif len(B) >= 50:
        for j in range(len(B)-51,len(B)-1):
            b.append(B[j])
            t3.append(T[j])
    return t3,b
            
#Broadband plot labels
def Blabels(axes):
    axes.title.set_text("Broadband measurement")
    axes.set_xlabel("Time (s)")
    axes.set_ylabel("Wavelength (nm)")
    program.refreshPlot("p")

#Broadband save database
def saveb(broadband,infrared,t):
    #global lit
    con = connection('Flickermeter.db')
    q = con.cursor()
    try:
        query = "INSERT INTO Data (LightID,Broadband,Infrared,Time) VALUES (?,?,?,?);"
        q.execute(query, (lit,broadband,infrared,t))
        con.commit()
        close_con(con)
    except con.Error as e:
        print(e)
        close_con(con)

#Broadband plot function
def BnD(tsll,start,i,first):
    #global flag
    global B
    global T
    #global saver
    while True:#flag == 1:
        #get raw (luminosity) readings individually
        broadband = tsll.broadband
        infrared = tsll.infrared
        B.append(broadband)
        #time program
        end = timer()
        t = end - start
        i += 1
        T.append(t)

        if i == 10:
            sens.loc[len(sens)] = [T,B]
            break
        #if saver == 1:
            #saveb(broadband,infrared,t)
        
        #if i >= 8:
            #print("enter")
            #i = 0
            #if first == 0:
                #[tempx, tempy] = getBT(B,T)
                #ax2 = program.updatePlot("p", list(tempx),list(tempy))
                #Blabels(ax2)
                #program.setLabel("Lnn","Infrared (nm):")
                #program.setLabel("Lv",round(infrared))
                #program.setLabel("Bn","Broadband (nm):")
                #program.setLabel("Bv",round(broadband))
                #program.setLabel("Tn","Time (s):")
                #program.setLabel("Tv",round(t))
                #first = 1
            #else:
                #[tempx,tempy] = getBT(B,T)
                #ax2 = program.updatePlot("p", *getBT(B,T),keepLabels = True)
                #program.setLabel("Lv",round(infrared))
                #program.setLabel("Bv",round(broadband))
                #program.setLabel("Tv",round(t))

program = dash.Dash(__name__)
program.layout = layoutb

@program.callback(
    Output(component_id='output', component_property='children')
    )
def update_value(input_data):
    return gplot(sens)#,
    #event = [Event(component_id='refresh',component_property='interval')])


if __name__ == '__main__':
    program.run_server(debug=True)
    check()



    
