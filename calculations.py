import pandas as pd

class Calculations(object):
    def __init__(self):
        super().__init__()
        #variables
        self.open = []
        self.close = []
        self.dates = []

    def trigger_data(self, stockName, stockYear): 
        sheet_name = stockName + "421"
        sheet = pd.read_excel("stocks.xlsx", sheet_name = sheet_name)
        self.open = sheet.open.values
        self.close = sheet.close.values
        self.dates = sheet.date.values
        print("DATA EXTRACTION PROCESSED")

    def get_open(self):
        return self.open

    def get_close(self):
        return self.close

    def get_dates(self):
        print(self.dates)
        return self.dates




if __name__ == '__main__':
    c = Calculations()
    c.get_data()
    p = c.get_dates()
    print(p)