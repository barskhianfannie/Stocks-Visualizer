import tkinter as tk
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import re
from pip._vendor import requests
import tkinter
from PIL import ImageTk, Image  

import sys

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QStatusBar
from PyQt5.QtWidgets import QToolBar




class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.open = []
        self.close = []
        self.open_avg = 0
        self.close_avg = 0
        self.date =  20
        self.display_open = tk.Label(root, text="")
        self.graph = Image.open("/Users/fanniebarskhian/Documents/Python/plot1.png")
        self.keys = []
        self.date_range = []
        self.requests = []
        self.stockName = ""
        self.create_widgets()
        self.frame = tk.Frame(root, width=1000, height=1000)
        self.frame.pack()
        


    def create_widgets(self):
         # Create label
        l = tk.Label(root, text = "Weekly Trends Information")
        l.pack()
        self.show = tk.Button(self)
        self.show["text"] = "Show Stocks"
        self.show["command"] = self.url_generator
        self.show.pack()

        self.quit = tk.Button(self, text="EXIT", fg="red",
                              command=self.master.destroy)
        self.quit.pack()
       
       

    def display_info(self):
        open = tk.Label(self, text= "")
        open.configure(text = "Open Average:" + str(self.open_avg))
        open.pack()
        close = tk.Label(self, text= "")
        close.configure(text = "Close Average:" + str(self.close_avg))
        close.pack()

    def plot_vals(self):
        plt.plot(self.date_range, self.open, label = "Opening Cost")
        plt.plot(self.date_range, self.close, label = "Closing Cost")
        plt.title("Trend Chart")
        plt.xlabel("Day of Month")
        plt.ylabel("Cost (Dollars)")
        plt.legend()
        plt.savefig("plot1.png")
        #plt.show()
        self.graph = ImageTk.PhotoImage(Image.open(("/Users/fanniebarskhian/Documents/Python/plot1.png")))
        panel = tk.Label(root, image = self.graph)
        panel.pack(side = "bottom")
        app.mainloop()

    def parse_values(self):
        for req in self.requests:
            day = requests.get(req)
            json_data = json.loads(day.text)
        
            for key in json_data.keys():
                if key == "open":
                    self.open.append(json_data[key])
                if key == "close":
                    self.close.append(json_data[key])
        self.calc_averages()

    def calc_averages(self):
        self.open_avg = sum(self.open) / len(self.open)
        self.close_avg = sum(self.close) / len(self.close)
        self.display_info()
        self.plot_vals()

    def url_generator(self):
        for i in range(0,4):
            curr = self.date - i
            self.date_range.append(curr)
            url = "https://api.polygon.io/v1/open-close/AAPL/2021-05-" + str(curr) + "?unadjusted=true&apiKey=GtSkOAQo74fLGqCtEPwNCQRXowyaBnhp"
            self.requests.append(url)
            
        self.parse_values()

root = tk.Tk()
app = Application(master=root)
app.mainloop()