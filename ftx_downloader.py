#Written by me in April 2021, was still learning python, code isn't great.
#FTX is currently down, if the API ever comes back you can use this.
import time
from client import FtxClient
import hmac
import pandas as pd
import json
import csv
from iso8601 import parse_date as parse_datetime
from requests import Request, Session, Response
secret = ''
key = ''

ftxapi = FtxClient(key, secret)
fetch_time = 604800
orders = ftxapi.get_order_history('BTC-PERP')
contracts = float(0)
change = float(0) 
def full_trade_history(market, starttime, endtime):
    start_time = float(starttime)
    end_time = float(endtime)
    iterations = int((end_time-start_time)/fetch_time)
    trades = []
    for i in range(0,iterations):
        ser_trades = []
        st = start_time + (i*fetch_time)
        et = st + fetch_time
        curorder = ftxapi.get_fills(start_time=st, end_time=et)
        for i in curorder:
            trades.append(i)
            ser_trades.append(i)
        if len(ser_trades)>210:
            print(len(ser_trades))
            #trades = get_frequent_trades(st, et)
            #break
    return trades

def get_frequent_trades(start, end):
    ft = 3600
    iterations = int(end-start/ft)
    trades=[]
    for i in range (0,iterations):
        ser_trades = []
        st = start + (i*ft)
        et = st + ft
        curorder = ftxapi.get_fills(market=None,start_time=start, end_time=end)
        for i in curorder:
            trades.append(i)
    return trades

def print_trades():
    for i in orders:
        if str(i['avgFillPrice']) != "None":
            if str(i['side']) == 'buy':
                change = float(i['size'])
            elif str(i['side']) == 'sell':
                change = float(i['size']) *-1

            contracts = contracts + change
            print(str(i['size']) + " " +str(i['side']) + " Order filled @ " + str(i['avgFillPrice']) + " Open Position Size: " + str(contracts))
#dates in unix format use ur own start and finish dates. 
all_FTX_TRADES = pd.DataFrame(full_trade_history("nil", 1565222400, 1621119864))
all_FTX_TRADES.to_csv("FTX_fills.CSV")
