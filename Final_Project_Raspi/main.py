import serial
import os
from client import Client
from strategy import Strategy
from time import sleep
#connect Uart to stm32
ser = serial.Serial ("/dev/ttyS0", 115200,timeout = 0.5)
#connect to max api
accessKey = 'CHb6F7pBxR8Q0txAT2tKO6smboHuJDxPJQEO7HB9';
secretKey = 'rDUtylrG7jeeMVxjX8uMtsq9KTfvTyk94Pkt7OqT';
strategy = Strategy(accessKey, secretKey); 

def send_cmd(cmd):
	buf = cmd + "\r"
	try:
		ser.write(buf.encode('utf-8'))
		return True
	except SerialException as e:
		print ("Error, ", e)
		return None
	
def get_data():
    received_data = ser.read(1)
    sleep(0.03)
    data_left = ser.inWaiting()
    received_data += ser.read(data_left)

    return received_data;
            



I_am_buy = 0
status = 1
pair = 'btcusdt'
while True:
    current_price = strategy.get_current_price(pair)
    target_price = strategy.get_ma(20,60,pair)
    buy_ratio = 1.02
    sell_ratio = 0.95

    current_price_str = ('%.2f'%current_price)
    if(I_am_buy == 0):
        I_am_buy = strategy.strategy_buy(current_price,target_price,buy_ratio,pair)
        target_price_str_buy = ('%.3f'%round(target_price*buy_ratio,3))
        send_cmd("current price = " + current_price_str+" target buy price = "+target_price_str_buy)
    if(I_am_buy == 1):
        I_am_buy = strategy.strategy_sell(current_price,target_price,sell_ratio,pair)
        target_price_str_sell = ('%.2f'%round(target_price*sell_ratio,2))
        send_cmd("current price = " + current_price_str+" target sell price = "+target_price_str_sell)
    data = get_data()
    if(data):
        os._exit(0)
    sleep(0.5)
    
