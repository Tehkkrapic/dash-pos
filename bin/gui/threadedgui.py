#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import queue
import PIL.Image, PIL.ImageTk
import tkinter as tk
from guilistener import GuiListener
from screeninfo import get_monitors
from time import sleep
from client import Client
import pyqrcode
# '127.0.0.1',65449 input
# '127.0.0.1',65448 output

DASHCOLOR = "#1C75B8"
BGCOLOR = "#f5f6f7"

class GuiVend():
    def __init__(self, master, queue, startVend):
        self.master = master
        self.queue = queue
        self.startVend = startVend
        # Set up the GUI
        self.master.title('Vend')
        # ukljuciti u produkciji
        self.master.wm_attributes('-type', 'splash')
        self.master.attributes("-fullscreen", True)
        self.master.geometry("{0}x{1}+0+0".format(self.master.winfo_screenwidth(), 
                                 self.master.winfo_screenheight()))
        self.master.config(cursor = 'none')
	# ukljuciti za debug
        # self.master.geometry('400x400')
        self.master.config(background="white")
        self.master.overrideredirect(True)
        self.master.focus_set()
        
        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_columnconfigure(0, weight=1)

        self.master.grid_rowconfigure(1, weight=2)
        self.master.grid_columnconfigure(1, weight=2)

        self.master.grid_rowconfigure(2, weight=1)
        self.master.grid_columnconfigure(2, weight=1)

        
        """ Poziv prvog screen-a """
        self.syncScreen()

    def processIncoming(self):
        """
        Procesiranje poruka iz reda
        """
        while self.queue.qsize():
            try:
                msg = self.queue.get(0)
                # Check contents of message and do what it says
                if 'gui' in msg.keys():
                    message = msg['gui'].split('-')
                    print (message)
                    
                    if(message[0] == 'syncScreen'):
                        self.syncScreen()                
                    elif (message[0] == 'idleScreen'):
                        self.idleScreen()
                    elif (message[0] == 'selectBeverageScreen'):
                        self.selectBeverageScreen()                    
                    elif (message[0] == 'paymentScreen'):
                        self.paymentScreen(message[1], float(message[2]))                   
                    elif (message[0] == 'finalScreen'):
                        self.finalScreen()
                    elif (message[0] == 'waitingScreen'):
                        self.waitingScreen()

            except queue.Empty:
                pass
    
    def syncScreen(self):
        self.clear()
        topLabel = tk.Label(self.master, text = "Loading ...".upper(),
                          font =('Verdana', 32, 'bold','italic'),
                          foreground= DASHCOLOR,
                              anchor="center")
        topLabel.config(background=BGCOLOR)
        topLabel.pack(expand= True)
        return
 
    
    def idleScreen(self):
       self.clear()
       topLabel = tk.Label(self.master, text = "BUY WITH:",
                    font =('Verdana', 32, 'bold','italic'),
                    foreground= DASHCOLOR,
                    anchor="center")
       topLabel.config(background="white")
       topLabel.grid(row= 0,column= 0, columnspan= 3, padx= 30, pady= 50)
        
       buttonWidth = 300
       buttonHeight = 100
       img = PIL.Image.open("images/logo.png")
       img = img.resize((buttonWidth, buttonHeight), PIL.Image.ANTIALIAS)
       photoDashLogo =  PIL.ImageTk.PhotoImage(img)
       
       dashButton = tk.Button(self.master,image=photoDashLogo, command=self.startVend,
                       width=420, height=200, highlightbackground=DASHCOLOR,
                       activebackground="#e9edf5", highlightcolor=DASHCOLOR, 
                       highlightthickness=3, bd=0, relief= "raised")
        
       dashButton.config(background= "white")
       dashButton.image = photoDashLogo
       dashButton.grid(row= 1, column= 0, columnspan= 3, padx= 30, pady= 50)
       
       self.defaultFooter().grid(row= 2, column= 0, columnspan= 3, sticky="nsew")
       return
    
    def selectBeverageScreen(self):
         self.clear()
         message = "select your\n favourite\n beverage"
         label = tk.Label(self.master, text = message.upper(),
                          font =('Verdana', 32, 'bold','italic'),
                          foreground= DASHCOLOR,
                              anchor="center")
         label.config(background=BGCOLOR)
         label.pack(expand = 1)
         return
   
    def paymentScreen(self, address, amount): 
        self.clear() 
        topLabel = tk.Label(self.master, text = "SEND\n" + str(amount) +" DASH",
                          font =('Verdana', 30, 'bold','italic'),
                          foreground= DASHCOLOR,
                              anchor="center")
        topLabel.config(background=BGCOLOR)
        topLabel.pack(padx = 20, pady = 20)


        code = pyqrcode.create('dash:'+address+'?amount='+str(amount)+'&label=DLT&IS=1')
        codeXBM = code.xbm(scale=8) 
        codeBMP = tk.BitmapImage(data=codeXBM)
        codeBMP.config(background=BGCOLOR)
        
        qrCode = tk.Label(self.master,image=codeBMP, relief="flat")
        qrCode.image = codeBMP
        qrCode.pack(padx = 20, pady = 20)

        addressLabel = tk.Label(self.master, text = "Scan QR code for\n payment".upper(),
                          font =('Verdana', 22, 'bold','italic'),
                          foreground= DASHCOLOR,
                              anchor="center")
        addressLabel.config(background=BGCOLOR)
        addressLabel.pack(padx = 20, pady = 20)
        return
    
    def waitingScreen(self):
        self.clear()
        topLabel = tk.Label(self.master, text = "LOOKING FOR YOUR \n TRANSACTION...",
                          font =('Verdana', 28, 'bold','italic'),
                          foreground= DASHCOLOR,
                              anchor="center")
        topLabel.config(background=BGCOLOR)
        topLabel.pack(expand= True)
        return

    def finalScreen(self):
        self.clear()
        topLabel = tk.Label(self.master, text = "THANK YOU!",
                          font =('Verdana', 32, 'bold','italic'),
                          foreground= DASHCOLOR,
                              anchor="center")
        topLabel.config(background=BGCOLOR)
        topLabel.pack(expand= True)
        return

    def defaultFooter(self):        
        frame = tk.Frame(self.master)
        frame.config(background= BGCOLOR)
        frame.grid_rowconfigure(0, weight=1)
        for i in range(3):
            frame.grid_columnconfigure(i, weight=1)
        
        logoWidth = 80
        logoHeight = 80
       
        img = PIL.Image.open("images/auto_logo.png")
        img = img.resize((logoWidth + 20, logoHeight), PIL.Image.ANTIALIAS)
        photoAutoLogo =  PIL.ImageTk.PhotoImage(img)
       
        autoLabel = tk.Label(frame, image = photoAutoLogo)
        autoLabel.image = photoAutoLogo
        autoLabel.config(background= BGCOLOR)
        autoLabel.grid(row= 0, column= 0, padx= 30, pady= 0)
       
        img = PIL.Image.open("images/riteh_logo.gif")
        img = img.resize((100, 100), PIL.Image.ANTIALIAS)
        photoRitehLogo =  PIL.ImageTk.PhotoImage(img)
       
        ritehLabel = tk.Label(frame, image = photoRitehLogo)
        ritehLabel.image = photoRitehLogo
        ritehLabel.config(background= BGCOLOR)
        ritehLabel.grid(row= 0, column= 1, padx= 30, pady= 0)
       
        img = PIL.Image.open("images/qibixx_logo.png")
        img = img.resize((logoWidth, logoHeight), PIL.Image.ANTIALIAS)
        photoQibixxLogo =  PIL.ImageTk.PhotoImage(img)
        
        qibixxLabel = tk.Label(frame, image = photoQibixxLogo)
        qibixxLabel.image = photoQibixxLogo
        qibixxLabel.config(background= BGCOLOR)
        qibixxLabel.grid(row= 0, column= 2, padx= 30, pady= 0)
        
        return frame
    
    def clear(self):
        for widget in self.master.winfo_children():
            widget.destroy()
        #self.grid_forget()
        return


class ThreadedGUI:
    """
    Launch the main part of the GUI and the worker thread. periodicCall and
    endApplication could reside in the GUI, but putting them here
    means that you have all the thread controls in a single place.
    """
    def __init__(self, master):
        """
        Start the GUI and the asynchronous threads. We are in the main
        (original) thread of the application, which will later be used by
        the GUI. We spawn a new thread for the worker.
        """
        self.master = master

        # Waiting for connection to dash thread
        self.c = self.connect()

        # Create the queue
        self.queue = queue.Queue()

        # Set up the GUI part
        self.gui = GuiVend(master, self.queue, self.startVend)

        # Set up the thread to do asynchronous I/O
        # More can be made if necessary
        self.running = 1
        #conecct to listening
        self.connection = GuiListener(port = 65449, dataQueue = self.queue)
        self.connection.start()
        #nije ni potrebno ako se stavi scree1 u konstruktor GUIVend
        #self.connection.onThread(self.connection.initScreen)
        
        # Start the periodic call in the GUI to check if the queue contains
        # anything
        self.periodicCall()

    def periodicCall(self):
        """
        Check every 100 ms if there is something new in the queue.
        """
        self.gui.processIncoming()
        if not self.running:
            import sys
            sys.exit(1)
        self.master.after(100, self.periodicCall)

    def startVend(self):
        print("starting vending process")
        self.c.sendMessage('startVend')

    def connect(self):
        while True:
            try:
                c = Client('127.0.0.1',65448)
                return c
            except:
                pass
            print('Connecting...')
            sleep(1)

client = ThreadedGUI(tk.Tk())
client.master.mainloop()
