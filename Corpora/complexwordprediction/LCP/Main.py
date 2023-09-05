# -*- coding: utf-8 -*-
import tkinter as tk
from CorporaFrequency import CorporaFrequency
from RandomForestRegressor import RandomForestClasificator
#from Bert import BertClasificator
from CorporaFrequencyRNN import CorporaFrequencyRNN
import sys
from PIL import Image, ImageTk
import os
class Main(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.geometry("730x400")
        self.centerWindow()
        self.title("Complex Word Prediction System")
        self.resizable(width=0, height=0)
        
       
        # the container is where we'll stack a bunch of frames
        # on top of each other,  then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, CorporaFrequency,CorporaFrequencyRNN,RandomForestClasificator):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")
        # self.show_frame("CorporaFrequency")

    def show_frame(self, page_name):
        # Show a frame for the given page name
        frame = self.frames[page_name]
        frame.tkraise()

    def centerWindow(self):
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() / 2) - (width / 2)
        y = (self.winfo_screenheight() / 2) - (height / 2)
        self.geometry('%dx%d+%d+%d' % (width, height, x, y-50))


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Welcome to the System", height=2,font='Helvetica 18 bold')
        
        
        button1 = tk.Button(
            self,
            text="Feature Words",
            height=2,
            width=30, 
            fg="blue", activebackground='yellow',
            font='Helvetica 8 bold',cursor="circle",
            command=lambda: controller.show_frame("CorporaFrequency")
        )

        button2 = tk.Button(
            self,
            text="Bert & XLM-RoBERTa",
            height=2,
            width=30,
            fg="blue",
                font='Helvetica 8 bold',cursor="circle",
            command=lambda: controller.show_frame("CorporaFrequencyRNN")
        )

        button3 = tk.Button(
            self,
            text="Prediction Words",
            height=2,
            width=30,
            fg="blue",
                font='Helvetica 8 bold',cursor="circle",
            command=lambda: controller.show_frame("RandomForestClasificator")
        )

        #img = Image.open(os.path.abspath("images\machinelearning.png"))
        #img = img.resize((300, 250), Image.ANTIALIAS)
        #img = ImageTk.PhotoImage(img)
        #background = tk.Label(image = img, text = "Imagen S.O de fondo")
        #background.place(x = 10, y = 50)
        #background.config(bg = "white")
        #background.image = img

        
        img = Image.open(os.path.abspath("images\\networkneural.png"))
        img = img.resize((420, 260), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(img)
        panel = tk.Label(self, image=img)
        

        #panel_dos = tk.Label(self, image=img)
        panel.image = img
        #panel_dos.image = img
        label.place(x=375, y=20)
        panel.place(x=5,y=70)
        #panel_dos.place(x=450,y=50)
        button1.place(x=425,y=100)
        button2.place(x=425,y=180)
        button3.place(x=425,y=260)
        # panel.grid(row=2,column=0)
        # button1.grid(row=1, column=1)
        # button2.grid(row=2, column=1)
        # panel_dos.grid(row=2,column=2)


       


if __name__ == "__main__":    
    app = Main()   
    app.mainloop()
