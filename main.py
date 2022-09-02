# I want to sell put options but they are expensive
# so I want to find stocks that are over 1$ but less than my budget if
# bought 100x
# also maybe do some fun stuff with stock data

import pandas as pd
import pandas_datareader.data as web
import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style

style.use("ggplot")

start = dt.datetime(2000, 1, 1)
end = dt.datetime(2022, 1, 1)

df = web.DataReader("TSLA", "yahoo", start, end)

print(df.tail())