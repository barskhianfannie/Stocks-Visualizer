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

stocksDict = {
  "Apple (AAPL)": "AAPL",
  "Tesla (TSLA)": "TSLA",
  "General Motors (GM)": "GM"
}

monthDict = {
  "May": "521",
  "April": "421",
  "March": "321",
  "February" : "221",
  "January" : "121"
}

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
        self.label1 = QLabel(self)
        # Setting the Window Up 
        self._setWindow(False)  
        self.setForm()
        

        # adding items to the combo box
        
    def setForm(self):
        # creating a group box
        self.formGroupBox = QGroupBox("Stocks Entry Form")
        self.stockComboBox = QComboBox(self)
        self.stockLabel = QLabel("Choose Stock : " ,self)
        self.stockLabel.setGeometry(50, 10, 400, 15)
        self.stockComboBox.setGeometry(200, 10, 400, 15)
        self.stockComboBox.addItems(["Apple (AAPL)", "Tesla (TSLA)", "General Motors (GM)"])
        self.monthComboBox = QComboBox(self)
        self.monthComboBox.addItems(["May","April", "March", "February", "January"])
        self.monthLabel = QLabel("Choose Month : " ,self)
        self.monthLabel.setGeometry(50, 40, 400, 15)
        self.monthComboBox.setGeometry(200, 40, 400, 15)

    def _setWindow(self, new_window):
        self.setWindowTitle('Stocks Visualizer')
        self.setFixedWidth(1000)
        self.setFixedHeight(500)
        self.set_buttons()


    def set_buttons(self):
        self.button = QPushButton('Visualize', self)
        self.button.setGeometry(700, 20, 100, 50)
        self.button.clicked.connect(self.get_data)
        self.button.clicked.connect(self.show_highlow_graph)  


    def show_highlow_graph(self):
            self.label.setPixmap(QPixmap("/Users/fanniebarskhian/Documents/Python/plothighlow.png"))
            self.label.setScaledContents(True)
            self.label.setGeometry(10,100, 400, 400)
            self.label1.setPixmap(QPixmap("/Users/fanniebarskhian/Documents/Python/plotvolume.png"))
            self.label1.setScaledContents(True)
            self.label1.setGeometry(450,100, 400, 400)

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



    def plot_gm_vals(self, dates, open, close, high, low):
        plt.figure(1)
        plt.plot(dates, high, label = monthDict[self.monthComboBox.currentText()] + " Daily High")
        plt.title("Daily High Trend Chart")
        plt.xlabel("Day Of Month")
        plt.ylabel("Cost (Dollars)")
        plt.legend()
        plt.savefig("plothighlow.png")
        plt.figure(2)
        plt.plot(dates, high, label = monthDict[self.monthComboBox.currentText()] + " Daily Volume")
        plt.title("Daily Volume Trend Chart")
        plt.xlabel("Day Of Month")
        plt.ylabel("Amount)")
        plt.legend()
        plt.savefig("plotvolume.png")
        self.subwindow = QtGui.QMdiSubWindow()
        self.subwindow.setGeometry(300,10,700,700)
        self.graphWidget = pg.PlotWidget()
        #Add gray backround
        self.graphWidget.setBackground((255,255,255))
        self.graphWidget.setTitle(stocksDict[self.stockComboBox.currentText()] + " Open Close Trend Line", color = (0,0,0), size = "30pt")
        self.graphWidget.setLabel('left', 'Dollars ($)', color = (255,255,255))
        self.graphWidget.setLabel('bottom', 'Day of Month', color = (255,255,255))
        self.graphWidget.addLegend((0,100))
        self.graphWidget.showGrid(x=True, y=True)
        self.subwindow.setWidget(self.graphWidget)
        pen = pg.mkPen(color = (0,0,255),width = 4)
        pen1 = pg.mkPen(color = (255,165,0),width = 4)
        self.graphWidget.setXRange(0, 31, padding=0)
        self.graphWidget.plot(x=dates, y=open, name = "Opening Costs", pen = pen,symbol = '+',symbolSize = 3)
        self.graphWidget.plot(x=dates, y=close, name = "Closing Costs", pen = pen1,symbol = '+',symbolSize = 3)
        self.subwindow.show()

    def get_data(self):
        sheetname = stocksDict[self.stockComboBox.currentText()] + monthDict[self.monthComboBox.currentText()]
        data = Calculations()
        data.trigger_data(sheetname)
        open = data.get_open()
        dates = data.get_dates()
        close = data.get_close()
        high = data.get_high()
        low = data.get_low()
        self.plot_gm_vals(dates, open, close, high, low)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec_())