import fractions
from numpy.core.defchararray import index
from numpy.lib.function_base import append
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from fractions import Fraction

class backtest:
    def __init__(self, positions, index, cash = 1000000, rf = 0.03):
        self.index = index

        if index=='szzs':
            self.index_df = self.get_index_df('000001')
        if index=='szcz':
            self.index_df = self.get_index_df('399001')
        if index=='cybz':
            self.index_df = self.get_index_df('399006')
        if index=='hssb':
            self.index_df = self.get_index_df('000300')
        if index=='zzwb':
            self.index_df = self.get_index_df('000905')

        self.cash = cash
        self.rf = rf
        self.positions = positions
        self.price_return, self.test_price = self.get_prices()
        self.net_df, self.tot_df, self.amount_df, self.cum_amount_df = self.get_net_amount()
        self.dtd_pnl, self.cum_pnl = self.get_pnl()
        self.dtd_ret, self.cum_ret = self.get_return()
        self.sp_pd = self.get_sharpe_ratio_period()


    def get_index_df(self, index):
        # read szzs from file
        path = str(index)+'.csv'
        # print (path)
        #szzs_df = pd.read_csv((index)+'.csv', usecols=[0, 3], names=['date', 'close_price']).iloc[1:,:]
        szzs_df = pd.read_csv((index)+'.csv', usecols=[0, 6], names=['date', 'open_price']).iloc[1:,:]
        # print(szzs_df)
        szzs_df['date'] = pd.to_datetime(szzs_df['date'])
        szzs_df['open_price'] = szzs_df['open_price'].astype('float')
        szzs_df = szzs_df.set_index('date')
        szzs_df = szzs_df.sort_index(ascending=True)

        return szzs_df


    def get_prices(self):
        test_price = self.index_df.loc[self.positions.index,:]
        price_return = test_price.diff(1)

        return price_return, test_price

    # def get_pnl(self):
    #     dtd_pnl = pd.DataFrame(self.positions.shift(1)[['position']].values*self.price_return[['close_price']].values
    #     -self.test_price[['close_price']].values*0.003*abs(self.positions.shift(1)[['position']].values),  
    #                             index=self.price_return.index, columns=['dtd_pnl'])
    #     cum_pnl = dtd_pnl.cumsum()
    #     cum_pnl = cum_pnl.rename(columns={'dtd_pnl': 'cum_pnl'})

    #     return dtd_pnl, cum_pnl
    
    def get_net_amount(self):
        # if len(self.positions.position.unique()) == 1:
        #     print('Warnning: There is only '+ str(self.positions.position.unique()) + ' in positions.')
        p = list(self.positions.position)  
        op = list(self.test_price.open_price)
        # List of net cash in hand at the end of date t
        net_list = []
        # List of numbers of stock bought/sold at date t;
        # To buy or sell is decided by the position at date t
        amount_list = []
        # List of cummulated number of stock bought/sold at date t;
        cum_amount_list = []
        # List of cummulated profit and loss at date t
        #pnl_list = []
        # List of net value at hand
        tot_list = []
        # Initial cash in hand
        net = self.cash
        # Net value at hand
        tot = self.cash

        amount = 0
        cum_amount = 0
        #cum_pnl = 0
        k = 1
        m = 1
        # Situation of the first day
        if p[0] == 1:
            amount = int(net/(1.003*op[0]))
            cum_amount = amount
            net = net - amount*1.003*op[0]
            tot -= amount*0.003*op[0]
        elif p[0] == -1: # To Do: 
            amount = int(net/(1.006*op[0]))
            cum_amount = amount
            net = net - amount*1.006*op[0]
            tot -= amount*0.003*op[0]
            # Actually, net = net + 0.997*op[0]
        else:
            amount = 0
            cum_amount = amount
            net = net
            tot = tot

        amount_list.append(amount)
        cum_amount_list.append(cum_amount)
        net_list.append(net)
        #pnl_list.append(cum_pnl)
        tot_list.append(tot)

        # Situation after the first day
        for i in range(1,len(p)-1):
            if p[i] == 0:
                if p[i-1] == -1:
                    k+=1
                    tot = tot_list[-1] + cum_amount*(op[i-1]-op[i])
                elif p[i-1] == 0:
                    if k!=1:
                        k+=1
                        tot = tot_list[-1] + cum_amount*(op[i-1]-op[i])
                    elif m!=1:
                        m+=1                 
                        tot = tot_list[-1]+cum_amount*(op[i]-op[i-1])
                    elif k == 1 and m == 1:
                        tot = tot_list[-1]
                elif p[i-1] == 1:
                    m+=1
                    tot = tot_list[-1] + cum_amount*(op[i]-op[i-1])
                amount = 0
                cum_amount = cum_amount
                #cum_pnl = cum_pnl
                amount_list.append(amount)
                cum_amount_list.append(cum_amount)
                net_list.append(net)
                #pnl_list.append(cum_pnl)
                tot_list.append(tot)
                
            elif p[i] == 1:
                if p[i-1] == -1:
                    net = net + cum_amount*(op[i-k]*2.003-op[i]*1.003)
                    tot = tot_list[-1] + cum_amount*(op[i-1]-op[i])
                    #cum_pnl += cum_amount*(0.997*op[i-k]-1.003*op[i])
                    amount = int(net/(1.003*op[i]))
                    cum_amount = amount
                    net = net - amount*1.003*op[i]
                    tot -= cum_amount*0.003*op[i]
                elif p[i-1] == 1:
                    cum_amount = cum_amount
                    amount = 0
                    net = net - amount*1.003*op[i]
                    #cum_pnl = cum_pnl
                    m += 1
                    tot = tot_list[-1] + cum_amount*(op[i]-op[i-1])
                else:
                    if k == 1 and m != 1: # Means that the position before these 0 is 1, m!=1
                        amount = 0
                        cum_amount = cum_amount
                        net = net - amount*1.003*op[i]
                        #cum_pnl = cum_pnl
                        m+=1
                        tot = tot_list[-1] + cum_amount*(op[i]-op[i-1])
                    elif k==1 and m == 1: # Means that this is the first 1.
                        net = net
                        tot = tot_list[-1]
                        amount = int(net/(1.003*op[i]))
                        net -= amount*1.003*op[i]
                        cum_amount = amount
                        tot -= cum_amount*0.003*op[i]
                    elif k > 1:
                        net = net + cum_amount*(op[i-k]*2.003-op[i]*1.003)
                        tot = tot_list[-k] + cum_amount*(op[i-k]-1.003*op[i])
                        #cum_pnl += cum_amount*(0.997*op[i-k]-1.003*op[i]) 
                        amount = int(net/(1.003*op[i]))
                        cum_amount = amount
                        net = net - amount*1.003*op[i]
                        tot -= cum_amount*0.003*op[i]
                    # amount = int(net/(1.003*op[i]))
                    # cum_amount = amount
                    # net = net - amount*1.003*op[i]

                amount_list.append(amount)
                cum_amount_list.append(cum_amount)
                net_list.append(net)
                #pnl_list.append(cum_pnl)
                tot_list.append(tot)
                k = 1
            else: # p[i] = -1
                if p[i-1] == -1:
                    k += 1 
                    # d0 p = 1, k = 1; d1 p = -1, k = 1; d2 p = -1, k = 2; d3 p = -1, k = 3; d4 p = -1, k = 4; d5 p = 1, k = 1;
                    # d6 p = -1, k = 1; d7 p = -1, k = 2 ...
                    cum_amount = cum_amount
                    amount = 0
                    net = net - amount*1.006*op[i]
                    #cum_pnl = cum_pnl
                    tot = tot_list[-1] + cum_amount*(op[i-1]-op[i])
                elif p[i-1] == 1:
                    net = net + cum_amount*op[i]*0.997
                    #cum_pnl += cum_amount*(0.997*op[i]-1.003*op[i-m])
                    tot = tot_list[-1] + cum_amount*(op[i]-op[i-1])
                    amount = int(net/(1.006*op[i]))
                    cum_amount = amount
                    net = net - amount*1.006*op[i]
                    tot -= cum_amount*0.003*op[i]
                else:
                    if k == 1 and m!=1:
                        net = net + cum_amount*op[i]*0.997
                        # print(tot_list[-m])
                        # print(op[i-m])
                        # print(cum_amount)
                        tot = tot_list[-m] + cum_amount*(0.997*op[i]-op[i-m])
                        amount = int(net/(1.006*op[i]))
                        cum_amount = amount
                        net = net - amount*1.006*op[i]
                        #cum_pnl = cum_pnl
                        tot -= cum_amount*0.003*op[i]
                    elif k == 1 and m == 1:
                        net = net
                        tot = tot_list[-1]
                        amount = int(net/(1.006*op[i]))
                        cum_amount = amount
                        net = net - amount*1.006*op[i]
                        tot -= amount*0.003*op[i]
                    else:
                        tot = tot_list[-1] + cum_amount*(op[i-1]-op[i])
                        amount = 0
                        k+=1
                        #cum_pnl = cum_pnl
                        cum_amount = cum_amount
                        net = net - amount*1.006*op[i]
                m = 1
                amount_list.append(amount)
                cum_amount_list.append(cum_amount)
                net_list.append(net)
                #pnl_list.append(cum_pnl)
                tot_list.append(tot)


        if p[-1]==0:
            if p[-2]== 1 or (p[-2]==0 & m!=1): 
                # print(m)
                net = net + cum_amount*op[-1]*0.997
                #cum_pnl += cum_amount*(0.997*op[i]-1.003*op[i-m])
                tot = tot_list[-m] + cum_amount*(0.997*op[-1]-op[-1-m])
                # print(tot_list[-m])
                # print(op[-1-m])
            elif p[-2] == -1 or (p[-2]==0 & k != 1):
                net = net + cum_amount*(op[-1-k]*2.003-op[i]*1.003)
                #cum_pnl += cum_amount*(0.997*op[i-k]-1.003*op[i])
                tot = tot_list[-k] + cum_amount*(op[-1-k]-1.003*op[-1])
            else:
                net = net
                tot = tot_list[-1]
            # else:
            #     if k==1:
            #         net = net + cum_amount*op[i]*0.997
            #         cum_pnl += cum_amount*[0.997*op[i]-1.003*p[i-m]]
            #         amount = 0
            #         cum_amount = amount
            #     else:
            #         net = net + cum_amount*(op[i-k]*2.003-op[i]*1.003)
            #         cum_pnl += cum_amount*(0.997*op[i]-1.003*op[i-k])
            #         amount = 0
            #         cum_amount = amount

        elif p[-1] == 1:
            if (m == 1 and p[-2]!=1):
                net = net + cum_amount*(op[-1-k]*2.003-op[-1]*1.003)
                #cum_pnl += cum_amount*(0.997*op[i-k]-1.003*op[i])
                tot = tot_list[-k] + cum_amount*(op[-1-k]-1.003*op[-1])
            elif m!=1 or p[-2] == 1:
                net = net + cum_amount*op[-1]*0.997
                #cum_pnl += cum_amount*(0.997*op[i]-1.003*op[i-m])
                tot = tot_list[-m] + cum_amount*(0.997*op[-1]-op[-1-m])
        else:
            if (k == 1 and p[-2]!=-1):
                net = net + cum_amount*op[-1]*0.997
                #cum_pnl += cum_amount*(0.997*op[i]-1.003*op[i-m])
                tot = tot_list[-m] + cum_amount*(0.997*op[-1]-op[-1-m])
            elif k!=1 or p[-2] == -1:
                net = net + cum_amount*(op[-1-k]*2.003-op[-1]*1.003)
                #cum_pnl += cum_amount*(0.997*op[i-k]-1.003*op[i])
                tot = tot_list[-k] + cum_amount*(op[-1-k]-1.003*op[-1])
        amount = 0
        cum_amount = amount
        net = net
        amount_list.append(amount)
        cum_amount_list.append(cum_amount)
        net_list.append(net)
        # pnl_list.append(cum_pnl)
        tot_list.append(tot)
        
        net_df = pd.DataFrame(net_list, index=self.positions.index, columns=['net_t'])
        # pnl_df = pd.DataFrame(pnl_list, index=self.positions.index, columns=['cum_pnl'])
        tot_df = pd.DataFrame(tot_list, index=self.positions.index, columns=['tot_t'])
        amount_df = pd.DataFrame(amount_list, index=self.positions.index, columns=['amount_t'])
        cum_amount_df = pd.DataFrame(cum_amount_list, index=self.positions.index, columns=['cum_amount_t'])
        # print(cum_amount_df)

        return net_df, tot_df, amount_df, cum_amount_df

    def get_pnl(self):
        tot = self.tot_df
        # print(tot)
        dtd_pnl = tot.diff(1)
        dtd_pnl.columns=['dtd_pnl']
        d1 = list(tot.tot_t)[0]-self.cash
        dtd_pnl = dtd_pnl.fillna(d1)
        # print(dtd_pnl)
        cum_pnl = dtd_pnl.cumsum()
        cum_pnl = cum_pnl.rename(columns={'dtd_pnl': 'cum_pnl'})
        return dtd_pnl, cum_pnl
    
    
    def get_return(self):
        cum_pnl = self.cum_pnl
        dtd_pnl = self.dtd_pnl
        cash = self.cash
        tot = self.tot_df
        dtd_ret = pd.DataFrame(dtd_pnl.dtd_pnl.values/(tot.shift(1).tot_t.values), index=tot.index, columns=['dtd_ret'])
        d1 = list(cum_pnl.cum_pnl)[0]/cash
        dtd_ret = dtd_ret.fillna(d1)
        cum_ret = pd.DataFrame(cum_pnl.cum_pnl.values/cash, index=tot.index, columns=['cum_ret'])
        # print(cum_ret)
        return dtd_ret, cum_ret
                
    # To do（Return）
    def get_sharpe_ratio_period(self): # Non-risk rate
        # return self.dtd_pnl['dtd_pnl'].mean()/self.dtd_pnl['dtd_pnl'].std()
        # dtd_ret = self.dtd_ret
        cash = self.cash
        cum_ret = self.cum_ret
        tot = self.tot_df
        amount = self.amount_df[self.amount_df.amount_t!=0]
        if self.amount_df.amount_t[-1] == 0:
            tot = tot.loc[list(amount.index)+[pd.to_datetime('2020-7-27')]]
        else:
            tot = tot.loc[list(amount.index)]
        rf_adj = self.rf*(120/252)
        td_pnl = tot.diff()/tot.shift(1)
        d1 = (tot.tot_t[0]-cash)/cash
        td_pnl.fillna(d1)
        try:
            # print(dtd_ret['dtd_ret'].mean()-rf)
            # print(dtd_ret['dtd_ret'].std())
            sp_pd = (cum_ret['cum_ret'][-1]-rf_adj)/float(td_pnl['tot_t'].std())
        except ZeroDivisionError:
            sp_pd = 0

        return sp_pd

    def get_sharpe_ratio_1y(self):
        sp_pd = self.sp_pd
        return sp_pd * np.sqrt(252/120)

    def get_positions(self):
        return self.positions

    def get_index_data(self):
        return self.index_df

    def get_price_return(self):
        return self.price_return

    def get_dtd_pnl(self):
        return self.dtd_pnl

    def get_cum_pnl(self):
        return self.cum_pnl