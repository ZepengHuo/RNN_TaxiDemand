#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  1 13:14:44 2018

@author: Apoorb
"""

import os
import pandas as pd
from datetime import datetime
from datetime import date, timedelta # to get 1st Sunday of an year
import matplotlib.pyplot as plt # this is used for the plot the graph 

def parse(x):
	return datetime.strptime(x, '%Y %m %d %H')
print('Current working directory ',os.getcwd())
os.chdir("/Users/Apoorb/Documents/GitHub/RNN_TaxiDemand")
print('Current working directory ',os.getcwd())

# load data
df = pd.read_csv('TTB.csv',  usecols = ["totaltrips","TIME1"])

#df["dt"]=pd.to_datetime(dict(year=df.year, month=df.month, day=df.day,hour=df.time))
#df=df.drop(['year', 'month', 'day', 'time'],axis=1)

df["dt"]=pd.to_datetime(df.TIME1)
df=df.set_index('dt')
df=df.drop(columns="TIME1")
df=df[df.index.year==2016]
df=df.rename(columns={"totaltrips":"NumTrips"})

# Get 1st Sunday of an year
d = date(2016, 1, 1)                    # January 1st
if d.weekday()==1:
    d = date(2016, 1, 1)  
else :
    d += timedelta(days = 7 - d.weekday())  # First Monday
    
d2=date(2016,12,31)
if d2.weekday()==0:
    d2 = date(2016, 12, 31)  
else :
    d2-= timedelta(days=d2.weekday())  # Last Monday
    
d2.weekday()
#Get data for  entire weeks. 
df=df[(df.index>=str(d)) & (df.index<=str(d2))]

df1=df
# Fill missing dates
idx = pd.date_range(str(d),str(d2),freq='H')
df=df.reindex(idx,fill_value=0)
df[df.NumTrips==0]

df.NumTrips.resample('D').sum().plot(title='Number of Trips Over Day for Sum') 
plt.tight_layout()
plt.show()   
df['NumTrips'].resample('M').mean().plot(kind='bar')



for i in range(0,169):
    buf="NumTrip_"+str(i)
    df[buf]=df.NumTrips.shift(i)

df=df.drop(["NumTrips"],axis=1)
Ydf=df['NumTrip_0'].resample('W', how='sum')

Ydf=Ydf[(Ydf.index>=str(d)) & (Ydf.index<str(d2))]

Ydf=Ydf.rename("Y")
Ydf=Ydf.shift(1,freq='D')
Ydf=pd.DataFrame(Ydf)

Ydf1=Ydf.merge(df,'left',left_index=True, right_index=True)
Ydf1.sort_index()
Ydf1.to_csv("RNN_data.csv")


#################################
start_date = date(2016, 1, 1)                    # January 1st
end_date=date(2016,12,31)
d = start_date
delta = timedelta(days=1)
j=0
while d <= end_date:
    #print(d.strftime("%Y-%m-%d"))
    if(d.weekday()==0):
        j=j+1
    d += delta