#! /usr/bin/python3

from appJar import *
from matplotlib import style
from timeit import default_timer as timer
import time
import board
import busio
import adafruit_tsl2561 as tsl
import numpy
import math
import sqlite3

style.use('fivethirtyeight')

#create gui
program = gui("Flickermeter","Fullscreen")
program.setBg("lightblue")

flag = 0
distt = 0
radd = 0

#Illumanance plot data
def getLT(L,T):
    l = []
    t3 = []
    i = 0
    j = 0
    if len(L) >= 5 and len(L) < 50:
        for i in range(5,len(L)-1):
            l.append(L[i])
            t3.append(T[i])
    elif len(L) >= 50:
        for j in range(len(L)-51,len(L)-1):
            l.append(L[j])
            t3.append(T[j])
    return t3,l
            
#Illumanance plot labels
def Llabels(axes):
    axes.title.set_text("Illuminance measurement")
    axes.set_xlabel("Time (s)")
    axes.set_ylabel("Illuminance (Lux)")
    program.refreshPlot("p")

#Illuminance save database
def savel(broadband,infrared,plux,t):
    global lit
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

#Illumanance plot function
def LnD(L,T,tsll,start,i,first):
    global flag
    global saver
    while flag == 3:
        #get raw (luminosity) readings individually
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
            
        L.append(plux)
        
        #time program
        end = timer()
        t = end - start
        i += 1
        T.append(t)
        
        if saver == 1:
            savel(broadband,infrared,plux,t)
        
        if i >= 7:
            print("enter")
            if first == 0:
                program.setLabel("Lnn","Iluminance (lux):")
                program.setLabel("Lv",round(plux))
                program.setLabel("Bn","Broadband (nm):")
                program.setLabel("Bv",round(broadband))
                program.setLabel("Tn","Time (s):")
                program.setLabel("Tv",round(t))
                ax2 = program.updatePlot("p", *getLT(L,T))
                Llabels(ax2)
                first = 1
            else:
                ax2 = program.updatePlot("p",*getLT(L,T),keepLabels=True)
                program.setLabel("Lv",round(plux))
                program.setLabel("Bv",round(broadband))
                program.setLabel("Tv",round(t))
                
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
    global lit
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
def BnD(B,T,I,tsll,start,i,first):
    global flag
    global saver
    while flag == 1:
        #get raw (luminosity) readings individually
        broadband = tsll.broadband
        infrared = tsll.infrared
        B.append(broadband)
        #time program
        end = timer()
        t = end - start
        i += 1
        T.append(t)
        if saver == 1:
            saveb(broadband,infrared,t)
        
        if i >= 8:
            print("enter")
            i = 0
            if first == 0:
                [tempx, tempy] = getBT(B,T)
                ax2 = program.updatePlot("p", list(tempx),list(tempy))
                Blabels(ax2)
                program.setLabel("Lnn","Infrared (nm):")
                program.setLabel("Lv",round(infrared))
                program.setLabel("Bn","Broadband (nm):")
                program.setLabel("Bv",round(broadband))
                program.setLabel("Tn","Time (s):")
                program.setLabel("Tv",round(t))
                first = 1
            else:
                [tempx,tempy] = getBT(B,T)
                ax2 = program.updatePlot("p", *getBT(B,T),keepLabels = True)
                program.setLabel("Lv",round(infrared))
                program.setLabel("Bv",round(broadband))
                program.setLabel("Tv",round(t))

#Flicker plot data
def getFT(F,T):
    f = []
    t3 = []
    i = 0
    j = 0
    if len(F) >= 5 and len(F) < 50:
        for i in range(5,len(F)-1):
            f.append(F[i])
            t3.append(T[i])
    elif len(F) >= 50:
        for j in range(len(F)-51,len(F)-1):
            f.append(F[j])
            t3.append(T[j])
    return t3,f
            
#Flicker plot labels
def Flabels(axes):
    axes.title.set_text("Flicker measurement")
    axes.set_xlabel("Time (s)")
    axes.set_ylabel("Illuminance (lux)")
    program.refreshPlot,"p"

#Flicker save database
def savef(broadband,infrared,plux,fm,fi,Pltm,Plti,t):
    global lit
    con = connection('Flickermeter.db')
    q = con.cursor()
    try:
        query = "INSERT INTO Data (LightID,Broadband,Infrared,Illuminance,Short_Term_Flicker_Modulation,Short_Term_Flicker_Index,Long_Term_Flicker_Modulation,Long_Term_Flicker_Index,Time) VALUES (?,?,?,?,?,?,?,?,?);"
        q.execute(query, (lit,broadband,infrared,plux,fm,fi,Pltm,Plti,t))
        con.commit()
        close_con(con)
    except con.Error as e:
        print(e)
        close_con(con)

#Flicker plot function
def FnD(F,T,tsll,start,i,first):
    global flag
    global saver
    tv = 0
    tn = 0
    second = 0
    fm = 0
    fi = 0
    Pltm = 0
    Plti = 0
    while flag == 2:
        #get raw (luminosity) readings individually
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
            
        F.append(plux) 
        
        #time program
        end = timer()
        t = end - start
        if second == 0:
            tn = end - start
        else:
            tn = t - tv
        i += 1
        T.append(t)
        
        if saver == 1:
            savef(broadband,infrared,plux,fm,fi,Pltm,Plti,t)
        
        if i >= 7:
            print("enter")
            i = 0
            if first == 0:
                ax2 = program.updatePlot("p",*getFT(F,T))
                Flabels(ax2)
                program.setLabel("Lnn","Illumance (lux):")
                program.setLabel("Lv",round(plux))
                program.setLabel("Bn","Broadband (nm):")
                program.setLabel("Bv",round(broadband))
                program.setLabel("Tn","Time (s):")
                program.setLabel("Tv",round(t))
                first = 1
            else:
                ax2 = program.updatePlot("p", *getFT(F,T),keepLabels = True)
                program.setLabel("Lv",round(plux))
                program.setLabel("Bv",round(broadband))
                program.setLabel("Tv",round(t))
                
        if tn >= 20:
            c = 0
            total = 0
            A1 = 0
            A2 = 0
            fm = ((numpy.max(F)-numpy.min(F))/(numpy.max(F)+numpy.min(F)))*100
            ave = numpy.average(F)
            for values in range(len(F)-1):
                xx = T[c+1] - T[c]
                total += xx*((F[c+1] + F[c])/2)
                if values > ave:
                    A1 += xx*(((F[c + 1] - ave)+(F[c] - ave))/2)
                c += 1
                    
            A2 = total - A1
            fi = (A1/(A1+A2))*100
            if saver == 1:
                savef(broadband,infrared,plux,fm,fi,Pltm,Plti,t)
            program.setLabel("Fmn","Flicker Modulation%:")
            program.setLabel("Fmv",round(fm))
            program.setLabel("Fin","Flicker Index%:")
            program.setLabel("Fiv",round(fi))
            tn = 0
            tv = end - start
            T.clear()
            F.clear()
            second = 1

#Long term flicker plot function
def FLnD(F,T,tsll,start,i,first):
    FM = []
    FI = []
    Pm = 0
    Pi = 0
    Pltm = 0
    Plti = 0
    fm = 0
    fi = 0
    tn = 0
    second = 0
    tv = 0
    ss = 0
    global flag
    global lit
    global saver
    while flag == 4:
        #get raw (luminosity) readings individually
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
            
        F.append(plux)
        
        #time program
        end = timer()
        t = end - start
        if second == 0:
            tn = end - start
        else:
            tn = t - tv
        i += 1
        T.append(t)
        
        if saver == 1:
            savef(broadband,infrared,plux,fm,fi,Pltm,Plti,t)
        
        if i >= 100:
            print("enter")
            i = 0
            if first == 0:
                ax2 = program.updatePlot("p",*getFT(F,T))
                Flabels(ax2)
                program.setLabel("Lnn","Illumance (lux):")
                program.setLabel("Lv",round(plux))
                program.setLabel("Bn","Broadband (nm):")
                program.setLabel("Bv",round(broadband))
                program.setLabel("Tn","Time (s):")
                program.setLabel("Tv",round(t))
                first = 1
            else:
                ax2 = program.updatePlot("p", *getFT(F,T),keepLabels = True)
                program.setLabel("Lv",round(plux))
                program.setLabel("Bv",round(broadband))
                program.setLabel("Tv",round(t))
                
        if tn >= 20:
            c = 0
            total = 0
            A1 = 0
            A2 = 0
            fm = ((numpy.max(F)-numpy.min(F))/(numpy.max(F)+numpy.min(F)))*100
            ave = numpy.average(F)
            
            for values in range(len(F)-1):
                xx = T[c+1] - T[c]
                total += xx*((F[c+1] + F[c])/2)
                if values > ave:
                    A1 += xx*(((F[c + 1] - ave)+(F[c] - ave))/2)
                c += 1
            
            A2 = total - A1
            fi = (A1/(A1+A2))*100
            if saver == 1:
                savef(broadband,infrared,plux,fm,fi,Pltm,Plti,t)
            program.setLabel("Fmn","Flicker Modulation%:")
            program.setLabel("Fmv",round(fm))
            program.setLabel("Fin","Flicker Index%:")
            program.setLabel("Fiv",round(fi))
            FM.append(fm/100)
            FI.append(fi/100)
            tn = 0
            tv = end - start
            T.clear()
            F.clear()
            second = 1
            ss += 1
            
        if ss == 12:
            for lf in range(1,len(FM)):
                Pm += FM[lf-1] ** 3
                Pi += FI[lf-1] ** 3
                
            Pltm = math.pow(Pm/12,1/3)
            Plti = math.pow(Pi/12,1/3)
            if saver == 1:
                savef(broadband,infrared,plux,fm,fi,Pltm,Plti,t)
            program.setLabel("Fmn","Flicker Modulation:")
            program.setLabel("Fmv",round(Pltm))
            program.setLabel("Fin","Flicker Index:")
            program.setLabel("Fiv",round(Plti))
            break
            
#Flux function
def Flux(tsll):
    lux = tsll.lux
    global saver
    global distt
    global radd
    global lit
    
    dista = float(distt)
    radi = float(radd)
    
    cd = lux*(dista**2)
    flux = lux*4*math.pi*(radi**2)
    
    if saver == 1:
        try:
            con = connection('Flickermeter.db')
            q = con.cursor()
            query = "INSERT INTO Data (LightID,Flux,Luminous_Intensity,Distance,Radius) VALUES (?,?,?,?);"
            q.execute(query, (lit,flux,cd,dist,radi))
            con.commit()
            close_con(con)
        except con.Error as e:
            print(e)
            close_con(con)
    
    program.setLabel("Lnn","Illumance in lux (lx):")
    program.setLabel("Lv",round(lux))
    program.setLabel("Bn","Luminuous intensity in candela (cd):")
    program.setLabel("Bv",round(cd))
    program.setLabel("Tn","Luminuous flux in lumen (lm):")
    program.setLabel("Tv",round(flux))
        

#button function
def main(meas):
    global flag
    program.setLabel("Lnn"," ")
    program.setLabel("Lv"," ")
    program.setLabel("Bn"," ")
    program.setLabel("Bv"," ")
    program.setLabel("Tn"," ")
    program.setLabel("Tv"," ")
    program.setLabel("Fmn"," ")
    program.setLabel("Fmv"," ")
    program.setLabel("Fin"," ")
    program.setLabel("Fiv"," ")
    if meas == "Measure\nWavelength":
        print("Broadband (nm)")
        flag = 1
        program.showSubWindow("three")
    elif meas == "Measure\nFlicker":
        print("Flicker%")
        flag = 2
        program.showSubWindow("three")
    elif meas == "Measure\nIlluminance":
        print("Illuminance")
        flag = 3
        program.showSubWindow("three")
    elif meas == "Measure Long\nTerm Flicker":
        print("Plt")
        flag = 4
        program.showSubWindow("three")
    elif meas == "Measure\nFlux":
        print("Flux")
        flag = 5
        program.showSubWindow("three")
    elif meas == "Stop":
        print("Stopped")
        flag = 0
    elif meas == "Close":
        flag = 0
        program.stop()
    elif meas == "To Login":
        flag = 0
        program.hide()
        program.showSubWindow("one")
    elif meas == "Info":
        flag = 0
        program.showSubWindow("four")
        
    
def check():
    global flag

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
    
    if flag == 1:
        program.thread(BnD,B,T,I,tsll,start,i,first)
    elif flag == 2:
        program.thread(FnD,F,T,tsll,start,i,first)
    elif flag == 3:
        program.thread(LnD,L,T,tsll,start,i,first)
    elif flag == 4:
        program.thread(FLnD,F,T,tsll,start,i,first)
    elif flag == 5:
        program.thread(Flux,tsll)
    
    t = 0
    #disable sensor
    tsll.enabled=False

#pre set Labels
program.setStretch("column")
program.setSticky("nw")
program.addEmptyLabel("Lnn",row=1,column=0,colspan=1)
program.addEmptyLabel("Lv",row=2,column=0,colspan=1)
program.setLabelBg("Lnn","cyan")
program.setLabelBg("Lv","white")
program.setLabelFont("Lnn",size = 16, family = "Verdana")
program.setLabelFont("Lv",size = 16, family = "Verdana")

program.setSticky("nw")
program.addEmptyLabel("Bn",row=1,column=1,colspan=1)
program.addEmptyLabel("Bv",row=2,column=1,colspan=1)
program.setLabelBg("Bn","cyan")
program.setLabelBg("Bv","white")
program.setLabelFont("Bn",size = 16, family = "Verdana")
program.setLabelFont("Bv",size = 16, family = "Verdana")

program.setSticky("nw")
program.addEmptyLabel("Tn",row=1,column=2,colspan=1)
program.addEmptyLabel("Tv",row=2,column=2,colspan=1)
program.setLabelBg("Tn","cyan")
program.setLabelBg("Tv","white")
program.setLabelFont("Tn",size = 16, family = "Verdana")
program.setLabelFont("Tv",size = 16, family = "Verdana")

program.setSticky("nw")
program.addEmptyLabel("Fmn",row=1,column=3,colspan=1)
program.addEmptyLabel("Fmv",row=2,column=3,colspan=1)
program.setLabelBg("Fmn","cyan")
program.setLabelBg("Fmv","white")
program.setLabelFont("Fmn",size = 16, family = "Verdana")
program.setLabelFont("Fmv",size = 16, family = "Verdana")

program.setStretch("row")
program.setSticky("nw")
program.addEmptyLabel("Fin",row=1,column=4,colspan=1)
program.addEmptyLabel("Fiv",row=2,column=4,colspan=1)
program.setLabelBg("Fin","cyan")
program.setLabelBg("Fiv","white")
program.setLabelFont("Fin",size = 16, family = "Verdana")
program.setLabelFont("Fiv",size = 16, family = "Verdana")

program.setStretch("row")
program.setSticky("ne")
program.addButton("To Login",main,row=0,column=0,colspan=1)

program.setStretch("row")
program.setSticky("ne")
program.addButton("Info",main,row=0,column=4,colspan=1)

program.setStretch("row")
program.setSticky("nw")
program.addButton("Measure\nWavelength",main,row=3,column=4,colspan=1)

program.setStretch("row")
program.setSticky("w")
program.addButton("Measure\nFlicker",main,row=4,column=4,colspan=1)

program.setStretch("row")
program.setSticky("w")
program.addButton("Measure\nIlluminance",main,row=5,column=4,colspan=1)

program.setStretch("row")
program.setSticky("w")
program.addButton("Measure Long\nTerm Flicker",main,row=6,column=4,colspan=1)

program.setStretch("row")
program.setSticky("w")
program.addButton("Measure\nFlux",main,row=7,column=4,colspan=1)

program.setStretch("row")
program.setSticky("w")
program.addButton("Stop",main,row=8,column=4,colspan=1)

program.setStretch("row")
program.setSticky("w")
program.addButton("Close",main,row=9,column=4,colspan=1)
program.setButtonFont(size = 16, family = "Verdana")

program.setStretch("both")
program.setSticky("news")
program.addPlot("p",1,1,showNav = True,row=3,column=0,rowspan=7,colspan=4)

def connection(db):
    con = None
    try:
        con = sqlite3.connect(db)
    except con.Error as e:
        print(e)
    
    return con

def close_con(con):
    con.close()
     
def pressed(submit):
    if submit == "Cancel":
        program.stop()
    elif submit == "Log in":
        global usr
        usr = program.getEntry("Username")
        psw = program.getEntry("Password")
        program.clearEntry("Username")
        program.clearEntry("Password")
        con = connection('Flickermeter.db')
        q = con.cursor()
        try:
            q.execute("SELECT 1 FROM User WHERE Username = ? AND Password = ?", (usr, psw))
            if q.fetchone() is not None:
                program.hideSubWindow("one")
                close_con(con)
                program.show()
            else:
                program.warningBox(title = "Error", message = "Username or password incorrect",parent = "one")
        except con.Error as e:
            print(e)
            close_con(con)
    else:
        program.hideSubWindow("one")
        program.showSubWindow("two")
        
def press(submit):
    if submit == "Exit":
        program.hideSubWindow("flux")
    else:
        global distt
        global radd
        distt = program.getEntry("Distance")
        radd = program.getEntry("Radius")
        if len(distt) < 1:
            program.warningBox(title="Missing data",message="No distance given",parent="flux")
        elif len(radd) < 1:
            program.warningBox(title="Missing data",message="No distance given",parent="flux")
        else:
            program.hideSubWindow("flux")
            program.clearEntry("Distance")
            program.clearEntry("Radius")
            check()
        
def regis(reg):
    if reg == "Submit":
        global usr
        usr = program.getEntry("Enter Username")
        nam = program.getEntry("Enter Name")
        sur = program.getEntry("Enter Surname")
        psw1 = program.getEntry("Enter Password")
        psw2 = program.getEntry("Confirm Password")
        program.clearEntry("Enter Username")
        program.clearEntry("Enter Name")
        program.clearEntry("Enter Surname")
        program.clearEntry("Enter Password")
        program.clearEntry("Confirm Password")
        con = connection('Flickermeter.db')
        q = con.cursor()
        if psw1 != psw2:
            program.warningBox(title = "Error", message = "Passwords do not match",parent = "two")
        else:
            try:
                q.execute("INSERT INTO User (Username,Name,Surname,Password) VALUES (?,?,?,?);", (usr, nam, sur, psw1))
                con.commit()
                program.hideSubWindow("two")
                program.show()
                close_con(con)
            except con.Error as e:
                print(e)
                close_con(con)
    else:
        program.hideSubWindow("two")
        program.showSubWindow("one")

#Start Window
program.startSubWindow("one",title = "Login",modal = True)
program.addLabel("titles", "Welcome! please login to continue")
program.setLabelFont("titles",size = 16, family = "Verdana")
program.setLabelBg("titles", "cyan")
program.setLabelFg("titles","red")
program.setBg("blue")
program.addLabelEntry("Username")
program.setEntryMaxLength("Username",20)
program.addLabelSecretEntry("Password")
program.setEntryMaxLength("Password",20)
program.setLabelFont("Username",size = 16, family = "Verdana")
program.setLabelFont("Password",size = 16, family = "Verdana")
program.addButtons(["Log in", "Register","Cancel"], pressed)
program.stopSubWindow()

def enough(click):
    if click == "Back to Measuring":
        program.hideSubWindow("four")

#Info Window
program.startSubWindow("four",title = "Information",modal = True, blocking = True)
program.addLabel("titlesss", "This will be bunch of explanations once the code runs smoothly")
program.setLabelFont("titlesss",size = 16, family = "Verdana")
program.setLabelBg("titlesss", "cyan")
program.setLabelFg("titlesss","red")
program.setBg("blue")
program.addButton("Back to Measuring", enough)
program.stopSubWindow()

def lighted(submit):
    global lit
    global usr
    global saver
    global flag
    con = connection('Flickermeter.db')
    if submit == "Load":
        q = con.cursor()
        lists = []
        try:
            q.execute("SELECT * FROM Light_Info WHERE UserID=?;",(usr,))
            for row in q.fetchall():
                if len(row)>0 and len(row)<4:
                    lists.append(row[0])
            close_con(con)
        except con.Error as e:
            print(e)
            close_con(con)
            program.hideSubWindow("three")
                
        if len(lists)>2:
            program.changeOptionBox("Existing ID",["-Empty-",lists[0],lists[1],lists[2],"None"])
        elif len(lists)==2:
            lists.append("-Empty-")
            program.changeOptionBox("Existing ID",["-Empty-",lists[0],lists[1],lists[2],"None"])
        elif len(lists)==1:
            for i in range(2):
                lists.append("-Empty-")
            program.changeOptionBox("Existing ID",["-Empty-",lists[0],lists[1],lists[2],"None"])
        else:
            program.warningBox(title = "No Data", message = "No saved data /nor no memory allocated for more for data,try again",parent="three")
                        
    elif submit == "Ok":
        saver = 1
        tik = program.getOptionBox("Existing ID")
        if tik != None and tik != "None":
            lit = tik
            program.hideSubWindow("three")
            close_con(con)
            program.changeOptionBox("Existing ID",["-Empty-","-Empty-","-Empty-","-Empty-","None"])
            if flag==5:
                program.showSubWindow("flux")
            else:
                check()
        else:
            try:
                lit = program.getEntry("Light ID")
                nam = program.getEntry("Light Type")
                if len(lit) < 1:
                    program.warningBox(title = "ID Error", message = "No light ID given or selected",parent="three")
                elif len(nam) < 1:
                    program.warningBox(title = "Type Error", message = "No light type given",parent="three")
                else:
                    program.clearEntry("Light ID")
                    program.clearEntry("Light Type")
                    q = con.cursor()
                    q.execute("INSERT INTO Light_Info (LightID,Light_Type,UserID) VALUES (?,?,?);", (lit,nam,usr))
                    con.commit()
                    program.hideSubWindow("three")
                    close_con(con)
                    program.changeOptionBox("Existing ID",["-Empty-","-Empty-","-Empty-","-Empty-","None"])
                    if flag==5:
                        program.showSubWindow("flux")
                    else:
                        check()
            except con.Error as e:
                print(e)
                close_con(con)
                program.hideSubWindow("three")
    else:
        program.hideSubWindow("three")
        program.changeOptionBox("Existing ID",["Empty","-Empty-","-Empty-","-Empty-"])
        close_con(con)
        saver = 0
        if flag==5:
            program.showSubWindow("flux")
        else:
            check()


#LightID
program.startSubWindow("three",title = "Register Light ID",modal = True,blocking = True)
program.setStretch("row")
program.setSticky("news")
program.addLabel("Enter Light ID",row=0,column=0,colspan=3)
program.setLabelFont("Enter Light ID",size = 16, family = "Verdana")
program.setLabelBg("Enter Light ID", "cyan")
program.setLabelFg("Enter Light ID","red")
program.setBg("blue")
program.setStretch("row")
program.setSticky("news")
program.addEntry("Light ID",row=1,column=0,colspan=3)
program.setEntryMaxLength("Light ID",20)
program.setLabelFont("Light ID",size = 16, family = "Verdana")
program.setEntryDefault("Light ID","ex. Light1")
program.setStretch("row")
program.setSticky("news")
program.addLabel("Enter Light Type",row=2,column=0,colspan=3)
program.setLabelFont("Enter Light Type",size = 16, family = "Verdana")
program.setLabelBg("Enter Light Type", "cyan")
program.setLabelFg("Enter Light Type","red")
program.setBg("blue")
program.setStretch("row")
program.setSticky("news")
program.addEntry("Light Type",row=3,column=0,colspan=3)
program.setEntryMaxLength("Light Type",20)
program.setEntryDefault("Light Type","ex. Flourescent")
program.setLabelFont("Light Type",size = 16, family = "Verdana")
program.setStretch("row")
program.setSticky("news")
program.addOptionBox("Existing ID",["-Empty-","-Empty-","-Empty-","-Empty-","None"],row=4,column=0,colspan=2)
program.setStretch("row")
program.setSticky("news")
program.addButton("Load",lighted,row=4,column=2,colspan=1)
program.setStretch("row")
program.setSticky("news")
program.addButtons(["Ok","Pass"], lighted,row=5,column=0,colspan=3)
program.stopSubWindow()

#Register Window
program.startSubWindow("two",title = "Register",modal = True)
program.setBg("blue")
program.addLabelEntry("Enter Username")
program.setEntryMaxLength("Enter Username",20)
program.addLabelEntry("Enter Name")
program.setEntryMaxLength("Enter Name",20)
program.addLabelEntry("Enter Surname")
program.setEntryMaxLength("Enter Surname",25)
program.addLabelSecretEntry("Enter Password")
program.setEntryMaxLength("Enter Password",20)
program.addLabelSecretEntry("Confirm Password")
program.setEntryMaxLength("Confirm Password",20)
program.setLabelFont("Enter Username",size = 16, family = "Verdana")
program.setLabelFont("Enter Name",size = 16, family = "Verdana")
program.setLabelFont("Enter Surname",size = 16, family = "Verdana")
program.setLabelFont("Enter Password",size = 16, family = "Verdana")
program.setLabelFont("Confirm Password",size = 16, family = "Verdana")
program.addButtons(["Submit","Back"], regis)
program.stopSubWindow()

#Flux Windows
program.startSubWindow("flux",title = "Flux and Intensity",modal = True, blocking = True)
program.addLabel("titless", "Please input the following values and continue.")
program.setLabelBg("titless", "cyan")
program.setLabelFont("titless",size = 16, family = "Verdana")
program.setBg("lightblue")
program.addLabel("dist","Distance from light to sensor")
program.setLabelFont("dist",16)
program.setLabelBg("dist","cyan")
program.addLabelEntry("Distance")
program.setEntryDefault("Distance","Most likely between 0 and 3")
program.setEntryMaxLength("Distance",10)
program.addLabel("rad","Radius of light")
program.setLabelFont("rad",16)
program.setLabelBg("rad","cyan")
program.addLabelEntry("Radius")
program.setEntryDefault("Radius","Most likely below 1")
program.setEntryMaxLength("Radius",10)
program.addButtons(["Continue", "Exit"], press)
program.stopSubWindow()

program.go(startWindow = "one")