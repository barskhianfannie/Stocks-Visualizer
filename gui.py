import sys
sys.path.append('/Users/fanniebarskhian/Documents/Python/calculations.py')
from calculations import Calculations


from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap
from PyQt5 import QtGui
from PyQt5.QtCore import QDate, Qt
from datetime import datetime
import tkinter as tk
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json
from urllib.request import urlopen, Request
import pyqtgraph as pg
import re
from pip._vendor import requests
from PIL import ImageTk, Image  

class TimeAxisItem(pg.AxisItem):
    def tickStrings(self, values, scale, spacing):
        return [datetime.fromtimestamp(value) for value in values]

class Window(QMainWindow):
    """Main Window."""
    #This is the Constructor
    def __init__(self, parent=None, date=20):
        """Initializer."""
        super().__init__(parent)
        #variables
        self.date =  date
        self.keys = []
        self.label = QLabel(self)
        # Setting the Window Up 
        self._setWindow(False)  
        self.subwindow = QtGui.QMdiSubWindow()
        self.subwindow.setGeometry(300,10,700,700)
        self.graphWidget = pg.PlotWidget()
        self.subwindow.setWidget(self.graphWidget)
        self.subwindow.show()

    

    def _setWindow(self, new_window):
        self.setWindowTitle('Stocks Visualizer')
        self.setFixedWidth(1000)
        self.setFixedHeight(1000)
        self.set_buttons()

    def appl_wrapper(self):
        print("IN APPL WRAPPER")
        self.appl_url_generator("AAPL")

    def gm_wrapper(self):
        print("IN GM WRAPPER")
        self.appl_url_generator("GM")

    def set_buttons(self):
        self.button = QPushButton('Apple Stock', self)
        self.button.setGeometry(60,60,100,100)
        self.button.clicked.connect(self.get_data)
        self.button.clicked.connect(self.show_gm_graph)  

        self.button = QPushButton('GM Stock', self)
        self.button.setGeometry(160,60,100,100)
        self.button.clicked.connect(self.gm_wrapper)
        self.button.clicked.connect(self.show_gm_graph) 



    def show_appl_graph(self):
            self.label.setPixmap(QPixmap("/Users/fanniebarskhian/Documents/Python/plotappl.png"))
            self.label.setScaledContents(True)
            self.label.setGeometry(500,400,400,500)

    def show_gm_graph(self):
            self.label.setPixmap(QPixmap("/Users/fanniebarskhian/Documents/Python/plotgm.png"))
            self.label.setScaledContents(True)
            self.label.setGeometry(300,10,700,700)

    def _createMenu(self):
        self.menu = self.menuBar().addMenu("&Stocks Menu")
        self.menu.addAction('&Apple', self.show_appl_graph)
        self.menu.addAction('&GM', self.show_gm_graph)
    
    def add_image(self):
        self._setWindow(True)


    def _createToolBar(self):
        tools = QToolBar()
        self.addToolBar(tools)
        tools.addAction('Apple', self.show_appl_graph)
        tools.addAction('GM', self.show_gm_graph)
        tools.addAction('Both', self.gm_url_generator)



    def plot_gm_vals(self, dates, open, close):
        plt.figure(1)
        plt.plot(dates, open, label = "Opening Cost")
        plt.plot(dates, close, label = "Closing Cost")
        plt.title("AAPL Open / Close Trend Chart")
        plt.xlabel("Year - Month")
        plt.ylabel("Cost (Dollars)")
        plt.legend()
        plt.savefig("plotgm.png")
        self.subwindow = QtGui.QMdiSubWindow()
        self.subwindow.setGeometry(300,10,700,700)
        self.graphWidget = pg.PlotWidget()
        self.subwindow.setWidget(self.graphWidget)
        self.graphWidget.plot(x=dates, y=open)
        self.subwindow.show()

    def get_data(self):
        data = Calculations()
        data.trigger_data("AAPL", "21")
        appl_open = data.get_open()
        appl_dates = data.get_dates()
        appl_close = data.get_close()
        self.plot_gm_vals(appl_dates, appl_open, appl_close)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec_())