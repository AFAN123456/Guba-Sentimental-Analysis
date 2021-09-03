import pandas as pd
import numpy as np

class SentimentFactorb:
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
            #print(window)
            sum_array = window.sum()
            #print(sum_array)
            indx = np.argmax(sum_array)
            #print(indx)
            if indx == 0:
                pos.append(-1)
            elif indx == 1:
                pos.append(0)
            else:
                pos.append(1)
        return pos

    def get_sentiment_factor (self):
        day_list = sorted(pd.to_datetime(self.sz.date))[2:136]
        position = pd.DataFrame()
        position['date'] = day_list
        position['position'] = self.positions
        position = position.set_index('date')
        return position

            

        
          



    
