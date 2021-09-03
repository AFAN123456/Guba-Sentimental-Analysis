from functools import update_wrapper
from numpy.core.fromnumeric import mean
from numpy.lib.function_base import median
import pandas as pd
import numpy as np
from pandas.io.stata import StataStrLWriter

class SentimentFactorD:
    # Length_1 is the train set size for position, lenth_2 is the size of train set for rate.
    # 
    def __init__(self, length_1, weighted = True, rolling = True, length_2 = 30):
        self.sz = pd.read_csv('szzh2020.csv')
        
        self.length_1 = length_1
        self.length_2 = length_2
        # print(self.length_2)
        self.weighted = weighted
        self.rolling = rolling
        # print(self.rolling)

        if self.weighted == True:
            self.st = pd.read_csv('sentiment_count_weighted.csv')
        else:
            self.st = pd.read_csv('/home/afan/emotion_analysis/sentiment_factor/sentiment_count.csv')

        if self.rolling == True:
            # print(self.length_2)
            self.day_list = self.get_trading_dates() # 2020-02-03 to 2020-7-27 (120 days) while rolling == True
            # print(self.day_list)
            self.low_list, self.up_list = self.get_thresholds()
        else:
            self.day_list = sorted(pd.to_datetime(self.sz.date))[2:136]
            # print(self.day_list)

        
        self.positions = self.get_positions()
        

    
    def get_trading_dates (self):
        sz = self.sz
        sz['date'] = pd.to_datetime(sz.date)
        start_date = '2020-02-01'
        end_date = '2020-07-27'
        con1=sz['date']>=start_date
        con2=sz['date']<=end_date
        szt = sz[con1&con2]
        day_list = sorted(szt.date)
        return day_list
    

    def get_thresholds (self):
        day_list = self.day_list
        window_size = self.length_2
        st = self.st
        st['Date'] = pd.to_datetime(st.Date)
        st['rate'] = st['1']/st['-1']
        low_list = []
        up_list = []
        for i in range(len(day_list)):     
            date = day_list[i]
            ind = st[st.Date == date].index[0]
            window = st.iloc[ind-window_size:ind]
            # To refine!!
            # selling takes more risk, so prefer to buy
            med = window.rate.median()
            sd = window.rate.std()
            low = med-sd
            up = med+sd
            low_list.append(low)
            up_list.append(up)
            # print(low_list)
        return low_list, up_list 
        

    def get_positions (self): # length = [1,2,3,4,5,6]
        day_list = self.day_list
        window_len = self.length_1
        pos = [] 
        st = self.st
        st['Date'] = pd.to_datetime(st.Date)
        if self.rolling == True:
            low_list = self.low_list
            up_list = self.up_list
            for i in range(len(day_list)):
                date  = day_list[i]
                ind = st[st.Date == date].index[0]
                window = st.iloc[ind-window_len:ind]
                rate = window.sum()[2]/window.sum()[0]
                # print(rate)
                low = low_list[i]
                up = up_list[i]
                if rate < low:
                    pos.append(-1)
                    #print('F')
                elif rate > up:
                    pos.append(1)
                    # print('T')
                else:
                    pos.append(0)
                    # print('0')
        else:
            low = 1.25
            up = 1.38
            for i in range(len(day_list)):
                # print(day_list)
                date  = day_list[i]
                # print(st)
                ind = st[st.Date == date].index[0]
                # print(ind)
                window = st.iloc[ind-window_len:ind]
                rate = window.sum()[2]/window.sum()[0]
                # rate = rate
                if rate < low:
                    pos.append(-1)
                elif rate > up:
                    pos.append(1)
                else:
                    pos.append(0)
        return pos

    def get_sentiment_factor (self):
        day_list = self.day_list
        position = pd.DataFrame()
        position['date'] = day_list
        position['position'] = self.positions
        position = position.set_index('date')
        return position

            

        
          



    
