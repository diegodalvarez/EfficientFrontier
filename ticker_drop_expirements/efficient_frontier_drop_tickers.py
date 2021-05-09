import os
import datetime as dt
import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt

from efficient_frontier import *

#get the tickers
def get_tickers(url):
    
    table = pd.read_html(url)
    df = table[0]
    spx_tickers = df['Symbol'].tolist()
    spx_tickers.remove('BRK.B')
    spx_tickers.remove("BF.B")
    
    return spx_tickers

#cut the tickers
def cut_tickers(spx_tickers, cut_size):

    cut_size = int(len(spx_tickers) / cut_size)
    random_nums = sorted(np.random.randint(len(spx_tickers), size = cut_size), reverse = True)
    
    for i in range(len(random_nums)):
        
        print("pop value:", random_nums[i] - 1)
        print("column count:", len(spx_tickers))
        spx_tickers.pop(random_nums[i])
        
    print("tickers:", len(spx_tickers))

    return spx_tickers


#run the efficient frontier
def run_ef(spx_tickers, start, end, simulations):
    
    #make a list for the dataframes
    results = []
    
    print("simulations:", simulations)

    #the number of simulations is how many times we want to cut the tickers
    for i in range(simulations):
        
        print("simulation", i+1, "of", simulations)
        
        #first we want to cut the tickers
        spx_tickers = cut_tickers(spx_tickers, 4)
        
        #then we want to get the historical prices for those tickers
        prices = yf.download(spx_tickers, start, end)['Adj Close']
        
        #then we want to pass through the number of securities that we want
        num_portfolios = 10000
        
        #we also want to put in the risk free rate
        rf = 0.0
        
        #then we want to instantitate the efficient frontier variable
        ef = Efficient_Frontier(prices, spx_tickers)
        
        #then we want to get the results
        results_frame = ef.simulate_random_portfolios("mean_returns", "covariance", num_portfolios, rf)
        
        results.append(results_frame)
        
    return results


spx_tickers = get_tickers('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
#spx_tickers = ["AAPL", "MSFT", "AMZN", "GOOG", "FB", "TSLA", "BABA", "TSM", "V", "JPM", "JNJ", "WMT", "UNH", "MA", "NVDA", "HD", "BAC", "DIS", "PG", "PYPL", "CMCSA", "XOM", "VZ"]

start = dt.datetime(2010,1,1)
end = dt.datetime.today()

tickers = spx_tickers
scatter_plots = run_ef(tickers, start, end, 16)

total_plots = len(scatter_plots)

cols = 4
rows = 4

fig, axs = plt.subplots(rows,cols, figsize = (15, 15))
plotting_spots = []

for i in range(rows):
    
    for j in range(cols):
        
        tuple_spot = (i, j)
        plotting_spots.append(tuple_spot)
        
for j in range(total_plots):

    df = scatter_plots[j]
    plotting_spot = plotting_spots[j]
    ticker_count = len(df.columns) - 3
    
    axs[plotting_spot[0], plotting_spot[1]].scatter(df['stdev'], df['ret'])
    axs[plotting_spot[0], plotting_spot[1]].set_title(ticker_count)
    plt.tight_layout()
    
#fig.xlabel("Returns")
#fig.ylabel("Standard Deviation")

ts = str(dt.datetime.now().timestamp())
cwd = os.getcwd()

path = os.path.join(cwd, ts)
os.mkdir(path)

print("simulations done")
    
for i in range(len(scatter_plots)):
    
    df = scatter_plots[i]
    tickers = str(len(df.columns) - 3)
    
    print("writing", tickers, "tickers csv file")
    final_path = os.path.join(path, tickers + ".csv")
    df.to_csv(final_path)

print("saving plot")
fig_path = os.path.join(path, "plot")
plt.savefig(fig_path + ".png")   




