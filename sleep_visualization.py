import matplotlib 
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style

from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

LARGE_FONT= ("Verdana", 20)
MID_FONT= ("Verdana", 16)
style.use("ggplot")

inputFile = "" #input filename
filenameText = ""
dateText = ""
timeText = ""
chacking1 = False
chacking2 = False
chacking3 = False
nbOfData = []
sensor1 = []
sensor2 = []
sensor3 = []
sensor4 = []
sensor5 = []
sensor6 = []
sensor7 = []
sensor8 = []
sensor9 = []

def setInputFile(x):
    global inputFile
    inputFile = str(x)

def getInputFile():
    return inputFile

def setFilenameText(x):
    global filenameText
    filenameText = str(x)

def getFilenameText():
    return str(filenameText)

def setDateText(x):
    global dateText
    dateText = str(x)

def getDateText():
    return str(dateText)

def setTimeText(x):
    global timeText
    timeText = str(x)

def getTimeText():
    return str(timeText)

class OSEapp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        tk.Tk.wm_title(self,"Sleep Visualization") #program's title
    
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        
        for F in (HomePage, VisualPage1, VisualPage2, VisualPage3 ):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(HomePage) #Starter Page

    #show selected page
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()
        
#Home Page
class HomePage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        #Labe and Buttons
        label = tk.Label(self, text="Home", font=LARGE_FONT)
        label.grid(column=0,row=0,pady=10,padx=10)

        filenameLabel = tk.Label(self, text="File: ", font=MID_FONT)
        filenameLabel.grid(column=0,row=1)
        brownButton = ttk.Button(self, text="Browse...", command=self.fileDialog)
        brownButton.grid(column=2,row=1,pady=10,padx=6)
        enterButton = ttk.Button(self, text="Enter", command=lambda: controller.show_frame(VisualPage1))
        enterButton.grid(column=3,row=1,pady=10)

        exitButton = ttk.Button(self, text="Exit", command=lambda: exit(0))
        exitButton.grid(padx=10,pady=1,row=3)

    #read input file
    def fileDialog(self):
        fileName = filedialog.askopenfilename(initialdir = "",title = "Select file",filetypes=((" txt",".txt"),("All files", "*.*")))
        filenameDialog = tk.Label(self, text="")
        filenameDialog.grid(column=1,row=1,padx=6)
        filenameDialog.configure(text = fileName)
        setInputFile(fileName)

        pullEEGData = open(inputFile).read()
        listOfEEGData = pullEEGData.split('\n')
        for eachLine in listOfEEGData:
            if len(eachLine) > 1:
                x, a, b, c, d, e, f, g, h, i, k = eachLine.split(' ')
                nbOfData.append(int(x))
                sensor1.append(int(a))
                sensor2.append(int(b))
                sensor3.append(int(c))
                sensor4.append(int(d))
                sensor5.append(int(e))
                sensor6.append(int(f))
                sensor7.append(int(g))
                sensor8.append(int(h))
                sensor9.append(int(i))
        
        name = inputFile.split("/")
        inputFileName = name[(len(name)-1)]
        fn = inputFileName.split("-")
        global filenameText
        setFilenameText(str(fn[0]))
        global dateText
        setDateText(str(fn[3])+"/"+str(fn[2])+"/"+str(fn[1]))
        hr = fn[4].split("_")
        hrr = hr[2].split(".")
        global timeText
        setTimeText(hr[1]+":"+hrr[0])
        global chacking1
        chacking1 = True
        global chacking2
        chacking2 = True
        global chacking3
        chacking3 = True

#Page that show graphs of EEG Sensor, RIP Sensor and ECG Sensor.
class VisualPage1(tk.Frame):
    
    global filenameText
    global dateText
    global timeText

    filenameText = getFilenameText()
    dateText = getFilenameText
    timeText = getTimeText()
    a = getInputFile()

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        #Labels and buttons
        labelTitle = tk.Label(self, text="EEG Sensor, RIP Sensor and ECG Sensor", font=LARGE_FONT)
        labelTitle.pack(pady=10,padx=10)

        button1 = ttk.Button(self, text="EEG Sensor, RIP Sensor and ECG Sensor", command=lambda: controller.show_frame(VisualPage1))
        button1.pack(pady=3)

        button2 = ttk.Button(self, text="EMG Sensor and ACC Sensor", command=lambda: controller.show_frame(VisualPage2))
        button2.pack(pady=3)

        button3 = ttk.Button(self, text="BVP Sensor and SpO2 Sensor", command=lambda: controller.show_frame(VisualPage3))
        button3.pack(pady=3)

        backButton = ttk.Button(self, text="Back to home", command=lambda: controller.show_frame(HomePage))
        backButton.pack(pady=1)

        self.reload()

    def reload(self):
        global chacking1
        self.after(10000,self.reload)
        if( inputFile != ""):
            if(chacking1):
                chacking1 = False
                self.drawGraphs123()

    #draw graph of EEG Sensor, RIP Sensor and ECG Sensor.       
    def drawGraphs123(self):

        #Label of file information
        filenameText = getFilenameText()
        dateText = getDateText()
        timeText = getTimeText()

        labelFileInfo = tk.Label(self, text="Serial number: "+str(filenameText)+'\t'+"Date: "+str(dateText)+", "+str(timeText) , font=LARGE_FONT)
        labelFileInfo.pack(side="top", fill="both", expand=True,pady=3,padx=10)

        #Draw EEG sensor graph
        g = plt.figure()
        eg = g.add_subplot(311)
        eg.plot(nbOfData, sensor1,linewidth=0.7)
        eg.set_title("EEG sensor",fontsize = 10)
        # eg.set_xlabel("time(s)",fontsize = 6)  

        #Draw RIP sensor graph
        eg = g.add_subplot(312)
        eg.plot(nbOfData, sensor2,linewidth=0.7, color = '#a4b4fb' )
        eg.set_title("RIP sensor",fontsize = 10)
        # eg.set_xlabel("time(ms)",fontsize = 6)  

        #Draw ECG sensor graph
        eg = g.add_subplot(313)
        eg.plot(nbOfData, sensor3,linewidth=0.7, color= '#74cbeb')
        eg.set_title("ECG sensor",fontsize = 10)
        # eg.set_xlabel("time(ms)",fontsize = 6) 

        g.subplots_adjust(wspace=0.5,hspace=0.5)

        canvas = FigureCanvasTkAgg(g, self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.update()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        exitButton = ttk.Button(self, text="Exit", command=lambda: exit(0))
        exitButton.pack(pady=1)

#Page that show graphs of EMG Sensor and ACC Sensor.
class VisualPage2(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        #Label and buttons.
        labelTitle = tk.Label(self, text="EMG Sensor and ACC Sensor", font=LARGE_FONT)
        labelTitle.pack(pady=10,padx=10)

        button1 = ttk.Button(self, text="EEG Sensor, RIP Sensor and ECG Sensor", command=lambda: controller.show_frame(VisualPage1))
        button1.pack(pady=3)

        button2 = ttk.Button(self, text="EMG Sensor and ACC Sensor", command=lambda: controller.show_frame(VisualPage2))
        button2.pack(pady=3)

        button3 = ttk.Button(self, text="BVP Sensor and SpO2 Sensor", command=lambda: controller.show_frame(VisualPage3))
        button3.pack(pady=3)

        backButton = ttk.Button(self, text="Back to home", command=lambda: controller.show_frame(HomePage))
        backButton.pack(pady=1)

        self.reload()

    def reload(self):
        global chacking2
        self.after(10000,self.reload)
        if( inputFile != ""):
            if(chacking2):
                chacking2 = False
                self.drawGraphs456()

    #Draw graph of EMG Sensor and ACC Sensors.
    def drawGraphs456(self):

        #Label of file information
        filenameText = getFilenameText()
        dateText = getDateText()
        timeText = getTimeText()

        labelFileInfo = tk.Label(self, text="Serial number: "+str(filenameText)+'\t'+"Date: "+str(dateText)+", "+str(timeText) , font=LARGE_FONT)
        labelFileInfo.pack(side="top", fill="both", expand=True,pady=3,padx=10)
        
        f = plt.figure()

        #Draw EMG sensor graph
        ag = f.add_subplot(311)
        ag.clear()
        ag.plot(nbOfData, sensor4,linewidth=0.5 )
        ag.set_title("EMG sonsor",fontsize = 10)
        # ag.set_xlabel("time(s)",fontsize = 6)  

        #Draw ACC X axis sensor graph
        ag = f.add_subplot(312)
        ag.clear()
        ag.plot(nbOfData, sensor5,linewidth=0.5, color = '#a4b4fb' )
        ag.set_title("ACC X axis",fontsize = 10)
        # ag.set_xlabel("time(ms)",fontsize = 6)  

        #Draw ACC Y axis sensor graph
        ag = f.add_subplot(313)
        ag.clear()
        ag.plot(nbOfData, sensor6,linewidth=0.5, color= '#74cbeb' )
        ag.set_title("ACC Y axis",fontsize = 10)
        # ag.set_xlabel("time(ms)",fontsize = 6) 
        
        f.subplots_adjust(hspace=0.5)

        canvas = FigureCanvasTkAgg(f, self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.update()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        exitButton = ttk.Button(self, text="Exit", command=lambda: exit(0))
        exitButton.pack(pady=1)

#Page that show graphs of BVP Sensor and SpO2 Sensor
class VisualPage3(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        #Label and buttons
        labelTitle = tk.Label(self, text="BVP Sensor and SpO2 Sensor", font=LARGE_FONT)
        labelTitle.pack(pady=10,padx=10)

        button1 = ttk.Button(self, text="EEG Sensor, RIP Sensor and ECG Sensor", command=lambda: controller.show_frame(VisualPage1))
        button1.pack(pady=3)

        button2 = ttk.Button(self, text="EMG Sensor and ACC Sensor", command=lambda: controller.show_frame(VisualPage2))
        button2.pack(pady=3)

        button3 = ttk.Button(self, text="BVP Sensor and SpO2 Sensor", command=lambda: controller.show_frame(VisualPage3))
        button3.pack(pady=3)

        backButton = ttk.Button(self, text="Back to home", command=lambda: controller.show_frame(HomePage))
        backButton.pack(pady=1)

        self.reload()

    def reload(self):
        global chacking3
        self.after(10000,self.reload)
        if( inputFile != ""):
            if(chacking3):
                chacking3 = False
                self.drawGraphs789()

    #Draw graph of BVP Sensor and SpO2 Sensor
    def drawGraphs789(self):

        #Label of file information
        filenameText = getFilenameText()
        dateText = getDateText()
        timeText = getTimeText()

        labelFileInfo = tk.Label(self, text="Serial number: "+str(filenameText)+'\t'+"Date: "+str(dateText)+", "+str(timeText) , font=LARGE_FONT)
        labelFileInfo.pack(side="top", fill="both", expand=True,pady=3,padx=10)

        h = plt.figure()

        #Draw BVP sensor graph
        ag = h.add_subplot(311)
        ag.clear()
        ag.plot(nbOfData, sensor7,linewidth=0.5 )
        ag.set_title("BVP sensor",fontsize = 10)
        # ag.set_xlabel("time(s)",fontsize = 6)  

        #Draw SpO2 (Rad source) graph
        ag = h.add_subplot(312)
        ag.clear()
        ag.plot(nbOfData, sensor8,linewidth=0.5, color = '#a4b4fb' )
        ag.set_title("SpO2 (Rad source)",fontsize = 10)
        # ag.set_xlabel("time(ms)",fontsize = 6)  

        #Draw SpO2 (Infrared source) graph
        ag = h.add_subplot(313)
        ag.clear()
        ag.plot(nbOfData, sensor9,linewidth=0.5, color= '#74cbeb' )
        ag.set_title("SpO2 (Infrared source)",fontsize = 10)
        # ag.set_xlabel("time(ms)",fontsize = 6) 

        h.subplots_adjust(hspace=0.5)

        canvas = FigureCanvasTkAgg(h, self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.update()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        exitButton = ttk.Button(self, text="Exit", command=lambda: exit(0))
        exitButton.pack(pady=1)

if __name__== "__main__":
    app = OSEapp()
    height_value = app.winfo_screenheight()
    width_value = app.winfo_screenwidth()
    app.geometry("%dx%d+0+0" % (width_value,height_value)) #fullscreen size
    app.mainloop()

