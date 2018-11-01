# -*- coding: utf-8 -*-
"""
Created on Thu Nov  1 11:09:51 2018

@author: A-Bibeka
"""

import pandas as pd
from sodapy import Socrata

# Unauthenticated client only works with public data sets. Note 'None'
# in place of application token, and no username or password:
client = Socrata("data.cityofchicago.org", None)

# Example authenticated client (needed for non-public datasets):
# client = Socrata(data.cityofchicago.org,
#                  MyAppToken,
#                  userame="user@example.com",
#                  password="AFakePassword")

# First 2000 results, returned as JSON from API / converted to Python list of
# dictionaries by sodapy.
#results = client.get("wrvz-psew", limit=2000, where="trip_start_timestamp between '2015-08-14T11:15:00.000' AND '2015-08-14T11:15:00.000' ")
results = client.get("wrvz-psew",limit=10**10, where="trip_start_timestamp between '2017-01-31T00:00:00.000' AND '2017-12-31T23:59:00.000' ")

# Convert to pandas DataFrame
results_df = pd.DataFrame.from_records(results)