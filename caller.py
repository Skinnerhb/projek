from dash.dependencies import Output, Input, State
import sqlite3
from connect import connection, close_con
from Program import program

#@program.callback(
  #  Output('url','pathname'),
   # [Input('hideme2','value')]
   # )
#def resets(value):
    #if value == 'deselect':
        #return '/api/login'

@program.callback(
    [Output('show','children'),
     Output('hideme1','value'),
     Output('hideme2','value')
     ],
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
                return 'Logging in', 'confirmed','select'
            else:
                close_con(con)
                return 'Username or password incorrect', 'not', 'deselect'
        else:
            return 'No Username or Password given', 'not', 'deselect'


#save button callback
#@program.callback(
    #Output('save_con','children'),
    #[Input('Sbut','n_clicks')],
    #[State('LID','value')]
    #)
#def upout(n_clicks, value):
    #return 'clicks: {}, ID: "{}"'.format(
        #n_clicks,
        #value
       # )

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
    L.append(plux)
        
    fm = ((np.max(L)-np.min(L))/(np.max(L)+np.min(L)))*100
    ave = np.average(L)
    if len(L)>1:
        for values in range(len(L)-1):
            xx = T[values+1] - T[values]
            total += xx*((L[values+1] + L[values])/2)
            if L[values] > ave:
                A1 += xx*(((L[values + 1] - ave)+(L[values] - ave))/2)
                
        A2 = total - A1
        fi = (A1/(A1+A2))
        FM.append(fm/100)
        FI.append(fi)
        
        for lf in range(len(FM)):
            Pm += FM[lf] ** 3
            Pi += FI[lf] ** 3
            
        Pltm = math.pow(Pm/len(FM),1/3)
        Plti = math.pow(Pi/len(FI),1/3)
    
    if dist is not None and isinstance(float(dist),str) == False:
        flux = plux*(float(dist)**2)
    else:
        flux = 0
    
    
    if rad is not None and isinstance(float(rad),str) == False:
        cd = plux*4*math.pi*(float(rad)**2)
    else:
        cd = 0
    
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
        
    broadband = tsll.broadband
    infrared = tsll.infrared
    
    end4 = timer()
    t4 = end4 - start
    
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
    
    L2.append(plux)
    fm = ((np.max(L2)-np.min(L2))/(np.max(L2)+np.min(L2)))*100
    
    data['Flicker'].append(fm)
    data['Time3'].append(t4)
    
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