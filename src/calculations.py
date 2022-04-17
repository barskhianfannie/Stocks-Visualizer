import pandas as pd

class Calculations(object):
    def __init__(self):
        super().__init__()
        #variables
        self.open = []
        self.close = []
        self.dates = []
        self.high =[]
        self.low = []
        self.volume = []
        self.adjclose = []

    def trigger_data(self, sheetName): 
        sheetName = sheetName
        sheet = pd.read_excel("stocks.xlsx", sheet_name = sheetName)
        self.open = sheet.open.values
        self.close = sheet.close.values
        self.dates = sheet.date.values
        self.high = sheet.high.values
        self.low = sheet.low.values
        self.volume= sheet.volume.values
        self.adjclose = sheet.adjclose.values

    def get_open(self):
        return self.open

    def get_close(self):
        return self.close

    def get_dates(self):
        return self.dates

    def get_low(self):
        return self.low

    def get_high(self):
        return self.high

    def get_volume(self):
        return self.volume

    def get_adj(self):
        return self.adjclose


if __name__ == '__main__':
    c = Calculations()
    c.get_data()
    p = c.get_dates()
    print(p)