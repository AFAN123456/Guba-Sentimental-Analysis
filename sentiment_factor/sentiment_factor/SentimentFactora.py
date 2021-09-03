import pandas as pd
import numpy as np

class SentimentFactor:
    def __init__(self, length):
        self.st = pd.read_csv('sentiment_count.csv')
        self.sz = pd.read_csv('szzh2020.csv')
        
        self.length = length
        self.positions = self.get_positions()



    def get_positions (self): # length = [1,2,3,4,5,6]
        day_list = sorted(pd.to_datetime(self.sz.date))[2:136]
        window_len = self.length
        pos = [] # l = 1
        st = self.st
        st['Date'] = pd.to_datetime(st.Date)
        for i in range(len(day_list)):
            date  = day_list[i]
            ind = st[st.Date == date].index[0]
            window = st.iloc[ind-window_len:ind]
            rate = window.sum()[2]/window.sum()[0]
            if rate < 1.2:
                pos.append(-1)
            elif rate >1.3:
                pos.append(1)
            else:
                pos.append(0)
        return pos

    def get_sentiment_factor (self):
        day_list = sorted(pd.to_datetime(self.sz.date))[2:136]
        position = pd.DataFrame()
        position['date'] = day_list
        position['position'] = self.positions
        position = position.set_index('date')
        return position

            

        
          



    
