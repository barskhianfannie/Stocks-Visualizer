import sys
sys.path.append('/Users/fanniebarskhian/Documents/Python/calculations.py')
from calculations import Calculations


from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap
from PyQt5 import QtGui
from PyQt5.QtCore import QDate, Qt, QSortFilterProxyModel
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
        # self.setForm()
 
    def setForm(self):
        # creating a group box
        self.formGroupBox = QGroupBox("Stocks Entry Form")
        self.stockComboBox = QComboBox(self)
        self.stockComboBox.setEditable(True)
        self.stockComboBox.showPopup()

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
        self.setStyleSheet("background:rgb(r:105,g:105,b:105)")
        self.setFixedWidth(2000)
        self.setFixedHeight(1000)
        #Top Graph
        self.topGraph = pg.PlotWidget(self)
        self.topGraph.setGeometry(40, 140, 450, 400)
        self.topGraph.setObjectName("highlow")
        #Bottom Graph
        self.bottomGraph = pg.PlotWidget(self)
        self.bottomGraph.setGeometry(40, 550, 450, 400)
        self.bottomGraph.setObjectName("volume")
        #Central Graph 
        self.centralGraph = pg.PlotWidget(self)
        self.centralGraph.setGeometry(540, 140, 750, 700)
        self.centralGraph.setObjectName("openclose")
        #Central Graph Design
        self.centralGraph.setBackground((192,192,192))
        self.centralGraph.setTitle(" Daily Open / Close Trend Line", color = (0,0,0), size = "15pt")
        self.centralGraph.setLabel('left', 'Dollars ($)', color = (255,255,255))
        self.centralGraph.setLabel('bottom', 'Day of Month', color = (255,255,255))
        self.centralGraph.addLegend((0,20))
        self.centralGraph.showGrid(x=True, y=True)
        self.centralGraph.setXRange(1, 31, padding=0)
        #Top Half Graph Design
        self.topGraph.setBackground((192,192,192))
        self.topGraph.setTitle(" Daily High / Low Trend Line", color = (0,0,0), size = "15pt")
        self.topGraph.setLabel('left', 'Dollars ($)', color = (255,255,255))
        self.topGraph.setLabel('bottom', 'Day of Month', color = (255,255,255))
        self.topGraph.addLegend((0,20))
        self.topGraph.showGrid(x=True, y=True)
        self.topGraph.setXRange(1, 31, padding=0)
        #Bottom Half Visual Design
        self.bottomGraph.setBackground((192,192,192))
        self.bottomGraph.setTitle(" Daily Volume Trend Line", color = (0,0,0), size = "15pt")
        self.bottomGraph.setLabel('left', 'Volume', color = (255,255,255))
        self.bottomGraph.setLabel('bottom', 'Day of Month', color = (255,255,255))
        self.bottomGraph.addLegend((0,20))
        self.bottomGraph.showGrid(x=True, y=True)
        self.bottomGraph.setXRange(1, 31, padding=0)
        self.setForm()
        self.set_buttons()
        #Table Stats
        self.tableWidget = QTableWidget(6, 2, self)
        self.tableWidget.setGeometry(1350, 140, 518, 700)
        statHeader = QTableWidgetItem('Statistic')
        statHeader.setBackground(QtGui.QColor(128, 128, 128))
        self.tableWidget.setHorizontalHeaderItem(0,statHeader)
        self.tableWidget.setObjectName("tableWidget")
        valueHeader = QTableWidgetItem('Value')
        valueHeader.setBackground(QtGui.QColor(128, 128, 128))
        self.tableWidget.setHorizontalHeaderItem(1,valueHeader)
        self.tableWidget.setObjectName("tableWidget")
        stat0 = QtGui.QTableWidgetItem("Open Average")
        stat1 = QtGui.QTableWidgetItem("Close Average")
        stat2 = QtGui.QTableWidgetItem("High Average")
        stat3 = QtGui.QTableWidgetItem("Low Average")
        stat4 = QtGui.QTableWidgetItem("Volume Average")
        stat5 = QtGui.QTableWidgetItem("Adj Close Average")
        self.tableWidget.setColumnWidth(0,259)
        self.tableWidget.setColumnWidth(1,259)
        self.tableWidget.setItem(0,0, stat0)
        self.tableWidget.setItem(1,0, stat1)
        self.tableWidget.setItem(2,0, stat2)
        self.tableWidget.setItem(3,0, stat3)
        self.tableWidget.setItem(4,0, stat4)
        self.tableWidget.setItem(5,0, stat5)
        #Ad Location
        ad = QLabel(self)
        ad.setGeometry(540, 880, 1300, 100)
        ad.setText("YOUR AD HERE")
        ad.setStyleSheet("background:white")
        # self.set_buttons()


    def set_buttons(self):
        self.button = QPushButton('Visualize', self)
        self.button.setGeometry(700, 20, 100, 50)
        self.button.clicked.connect(self.get_data)

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


    def plot_gm_vals(self, dates, open, close, high, low, volume):
        print("Graphing")
        pen = pg.mkPen(color = (255,0,0),width = 2)
        pen1 = pg.mkPen(color = (0,0,0),width = 2)
        self.bottomGraph.clear()
        self.bottomGraph.plot(x=dates, y=volume, name = "Daily Volume", pen = pen)
        self.topGraph.clear()
        self.topGraph.plot(x=dates, y=high, name = "Daily High", pen = pen)
        self.topGraph.plot(x=dates, y=low, name = "Daily Low", pen = pen1)
        self.centralGraph.clear()
        pen2 = pg.mkPen(color = (255,0,0),width = 3)
        pen3 = pg.mkPen(color = (0,0,0),width = 3)
        self.centralGraph.plot(x=dates, y=open, name = "Daily Open", pen = pen2)
        self.centralGraph.plot(x=dates, y=close, name = "Daily Close", pen = pen3)
        self.centralGraph.setData(dates, open)
        self.centralGraph.setData(dates, close)

    def calculate_averages(self, open, close, high, low, volume, adjclose):
        openAvg = "$  " + str(float("{:.2f}".format((sum(open) / len(open))))) 
        closeAvg = "$  " + str(float("{:.2f}".format((sum(close) / len(close))))) 
        highAvg = "$  " + str(float("{:.2f}".format((sum(high) / len(high)))))
        lowAvg = "$  " + str(float("{:.2f}".format((sum(low) / len(low))))) 
        volAvg = str(float("{:.2f}".format((sum(volume) / len(volume))))) + " stocks"
        adjAvg = "$  " + str(float("{:.2f}".format((sum(adjclose) / len(adjclose))))) 
        stat0 = QtGui.QTableWidgetItem(openAvg)
        stat1 = QtGui.QTableWidgetItem(closeAvg)
        stat2 = QtGui.QTableWidgetItem(highAvg)
        stat3 = QtGui.QTableWidgetItem(lowAvg)
        stat4 = QtGui.QTableWidgetItem(volAvg)
        stat5 = QtGui.QTableWidgetItem(adjAvg)
        self.tableWidget.setItem(0,1, stat0)
        self.tableWidget.setItem(1,1, stat1)
        self.tableWidget.setItem(2,1, stat2)
        self.tableWidget.setItem(3,1, stat3)
        self.tableWidget.setItem(4,1, stat4)
        self.tableWidget.setItem(5,1, stat5)


    def get_data(self):
        sheetname = stocksDict[self.stockComboBox.currentText()] + monthDict[self.monthComboBox.currentText()]
        data = Calculations()
        data.trigger_data(sheetname)
        open = data.get_open()
        dates = data.get_dates()
        close = data.get_close()
        high = data.get_high()
        low = data.get_low()
        volume = data.get_volume()
        adjclose = data.get_adj()
        self.calculate_averages(open, close, high, low, volume, adjclose)
        self.plot_gm_vals(dates, open, close, high, low, volume)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec_())