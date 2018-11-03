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
os.chdir("/Users/Apoorb/Syncplicity Folders/Data Science Competition/Data")
print('Current working directory ',os.getcwd())

# load data
df = pd.read_csv('2016TaxiMedianHourly.csv',  usecols = ["NumTrips",'year', 'month', 'day', 'time'])

df["dt"]=pd.to_datetime(dict(year=df.year, month=df.month, day=df.day,hour=df.time))
df=df.drop(['year', 'month', 'day', 'time'],axis=1)
df=df.set_index('dt')

df=df[df.index.year==2016]


df.NumTrips.resample('D').sum().plot(title='Number of Trips Over Day for Sum') 
plt.tight_layout()
plt.show()   
df['NumTrips'].resample('M').mean().plot(kind='bar')


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

# Fill missing dates
idx = pd.date_range(str(d),str(d2),freq='H')
df=df.reindex(idx,fill_value=0)
df[df.NumTrips==0]

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