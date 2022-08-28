import numpy as np
import pandas as pd
from talib.abstract import *
from client import Client
from datetime import datetime
import time

class Strategy(Client):  
    def get_time(self):
        result = time.localtime()
        return result.tm_year,result.tm_mon,result.tm_mday,result.tm_hour,result.tm_min,result.tm_sec
    def get_k_line(self,num,time,pair):
        result = np.array(self.get_public_k_line(pair,num,time))
        result = result.transpose()
        data = {'open':result[:][1], 'high':result[:][2],'low':result[:][3],'close':result[:][4]}
        df = pd.DataFrame(data)
        return df
    def get_current_price(self,pair):
        return float(self.get_public_all_tickers(pair)['sell'])
    
    def trade_record(self,coin_type,trade_type,price,volume):
        t = time.localtime()
        result = time.strftime("%Y/%m/%d, %H:%M:%S", t)
        path = 'trade_record.txt'
        f = open(path, 'a')
        f.write(result)
        f.write(' '+str(coin_type)+' '+str(trade_type)+' '+str(price)+' '+str(volume)+'\n')
        f.close()
        
    def get_ma(self,ma,time,pair):
        df = self.get_k_line(ma,time,pair)
        real = MA(df, timeperiod=ma, matype=0)
        return float(real[ma-1])

    def strategy_buy(self,current_price,target_price,ratio,pair):
        print('buy current_price = '+str(current_price)+' , target_price = '+str(round(target_price*ratio,2)))
        if(current_price > target_price*ratio):
            self.set_private_create_order(pair,'buy',0.0005,target_price)
            self.trade_record(pair,'buy',current_price,0.0005)
            print('buy')
            return True
        return False

    def strategy_sell(self,current_price,target_price,ratio,pair):
        print('sell current_price = '+str(current_price)+' , target_price = '+str(round(target_price*ratio,2))) 
        if(current_price < target_price*ratio) :
            #self.set_private_create_order(pair,'sell',0.0005,current_price*1.01)
            self.trade_record(pair,'sell',current_price,0.0005)
            print('sell')
            return False
        return True
      
        
