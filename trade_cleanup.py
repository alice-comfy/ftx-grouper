##Script to parse FTX fills into something more human understandable. 
##Note: I am not an accountant and this is likely not 100% accurate for tax purposes. 
import pandas as pd

#lambdas for fetching first / last values from df
first = lambda x : x.iloc[0] 
last = lambda x : x.iloc[-1]

df = pd.read_csv("trades.csv",index_col=0) #raw data your CSV's name goes here. Don't put index col if you didn't export using another script.
grouped = df.groupby(['orderId', 'side', 'market', 'type']).agg({"price": "mean", 'size': 'sum', 'fee' : 'sum', 'feeRate': 'mean',  'time' : first, 'feeCurrency': first})
grouped['sizeUSD'] = grouped['price'] * grouped ['size']
grouped.to_csv("cleaned.csv")
