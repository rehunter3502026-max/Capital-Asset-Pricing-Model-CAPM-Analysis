from google.colab import drive
drive.mount('/content/drive')

import pandas as pd
import seaborn as sns
import plotly.express as px
from copy import copy
from scipy import stats
import matplotlib.pyplot as plt
import numpy as np
import plotly.figure_factory as ff
import plotly.graph_objects as go

# Read the stock data file
stocks_df = pd.read_csv('/content/drive/My Drive/Colab Notebooks/Python & ML in Finance/Part 2. Financial Analysis in Python/stock.csv')
stocks_df
# Sort the data based on Date
stocks_df = stocks_df.sort_values(by = ['Date'])
stocks_df
def normalize(df):
  x = df.copy()
  for i in x.columns[1:]:
    x[i] = x[i]/x[i][0]
  return x

# Function to calculate the daily returns 
def daily_return(df):

  df_daily_return = df.copy()
  
  # Loop through each stock
  for i in df.columns[1:]:
    
    # Loop through each row belonging to the stock
    for j in range(1, len(df)):
      
      # Calculate the percentage of change from the previous day
      df_daily_return[i][j] = ((df[i][j]- df[i][j-1])/df[i][j-1]) * 100
    
    # set the value of first row to zero, as previous value is not available
    df_daily_return[i][0] = 0
  return df_daily_return

stocks_daily_return = daily_return(stocks_df)
stocks_daily_return

stocks_daily_return['AAPL']
stocks_daily_return['sp500']

# plotting a scatter plot between the selected stock and the S&P500 (Market)
stocks_daily_return.plot(kind = 'scatter', x = 'sp500', y = 'AAPL')

beta, alpha = np.polyfit(stocks_daily_return['sp500'], stocks_daily_return['AAPL'], 1)
print('Beta for {} stock is = {} and alpha is = {}'.format('AAPL', beta, alpha))  

stocks_daily_return.plot(kind = 'scatter', x = 'sp500', y = 'AAPL')

plt.plot(stocks_daily_return['sp500'], beta * stocks_daily_return['sp500'] + alpha, '-', color = 'r')

stocks_daily_return['sp500'].mean()

rm = stocks_daily_return['sp500'].mean() * 252
rm
rf = 0 
ER_AAPL = rf + ( beta * (rm-rf) ) 
ER_AAPL

beta = {}
alpha = {}

# Loop on every stock daily return
for i in stocks_daily_return.columns:

  # Ignoring the date and S&P500 Columns 
  if i != 'Date' and i != 'sp500':
    # plot a scatter plot between each individual stock and the S&P500 (Market)
    stocks_daily_return.plot(kind = 'scatter', x = 'sp500', y = i)
    
    # Fit a polynomial between each stock and the S&P500 (Poly with order = 1 is a straight line)
    b, a = np.polyfit(stocks_daily_return['sp500'], stocks_daily_return[i], 1)
    
    plt.plot(stocks_daily_return['sp500'], b * stocks_daily_return['sp500'] + a, '-', color = 'r')
    
    beta[i] = b
    
    alpha[i] = a
    
    plt.show()


beta
alpha
keys = list(beta.keys())
keys
ER = {}

rf = 0 # assume risk free rate is zero in this case
rm = stocks_daily_return['sp500'].mean() * 252 # this is the expected return of the market 
rm
for i in keys:
  # Calculate return for every security using CAPM  
  ER[i] = rf + ( beta[i] * (rm-rf) ) 

or i in keys:
  print('Expected Return Based on CAPM for {} is {}%'.format(i, ER[i]))

portfolio_weights = 1/8 * np.ones(8) 
portfolio_weights

ER_portfolio = sum(list(ER.values()) * portfolio_weights)
ER_portfolio
print('Expected Return Based on CAPM for the portfolio is {}%\n'.format(ER_portfolio))


