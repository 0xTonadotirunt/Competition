
import pandas as pd
import pyarrow
import pyarrow.parquet


sg_df = pd.read_parquet('data/city=Singapore', engine='pyarrow')


import plotly.graph_objects as go

import numpy as np

import datetime
# functions to change dtypes
def to_category(df, *args):
    for col_name in args:
        df[col_name] = df[col_name].astype("category")
    
def to_float32(df, *args):
    for col_name in args:
        df[col_name] = df[col_name].astype("float32")
        
def to_uint16(df, *args):
    for col_name in args:
        df[col_name] = df[col_name].astype("uint16")
  
def to_int32(df, *args):
    for col_name in args:
      df[col_name] = df[col_name].astype("int32")

def format_datetime(df, col_name):
    # get datetime obj for all timestamps
    dt = sg_df[col_name].apply(datetime.datetime.fromtimestamp)
    
    df["time"] = dt.apply(lambda x: x.time())
    df["day_of_week"] = dt.apply(lambda x: x.weekday())
    df["month"] = dt.apply(lambda x: x.month)
    df["year"] = dt.apply(lambda x: x.year)
    
df_formatted = sg_df.copy()

format_datetime(df_formatted, "pingtimestamp")
to_category(df_formatted, ["trj_id", "driving_mode", "osname"])
to_float32(df_formatted, ["rawlat", "rawlng", "speed", "accuracy"])
to_uint16(df_formatted, ["bearing", "day_of_week", "month", "year"])
to_int32(df_formatted, "pingtimestamp")

#truncate data set
df_formatted = df_formatted.sort_values(by=['pingtimestamp'])
df_formatted2 = df_formatted.reset_index()
trunc_df = df_formatted2.truncate(before=0, after=100000, axis=0, copy=True)

trunc_df
df_formatted.head()

lat = trunc_df[["rawlat"]]
lat.head()
long = trunc_df[["rawlng"]]
long.head()
time = trunc_df[["pingtimestamp"]]
time.head()
accuracy = trunc_df[["accuracy"]]

min_lng = min(trunc_df["rawlng"])
max_lng = max(trunc_df["rawlng"])

min_lat = min(trunc_df["rawlat"])
max_lat = max(trunc_df["rawlat"])

