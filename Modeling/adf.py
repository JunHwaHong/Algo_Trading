from __future__ import print_function

# Import the Time Series library
import statsmodels.tsa.stattools as ts

# Import Datetime and the Pandas DataReader
from datetime import datetime
import pandas as pd
import FinanceDataReader as fdr

# Download the Amazon OHLCV data from 1/1/2000 to 1/1/2015
amzn = fdr.DataReader("AMZN", datetime(2000,1,1), datetime(2015,1,1))

# Output the results of the Augmented Dickey-Fuller test for Amazon
# with a lag order value of 1
print(ts.adfuller(amzn['Adj Close'], 1))