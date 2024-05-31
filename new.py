import yfinance as yf
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Nifty 50 ticker symbols
nifty50_tickers = [
    'ADANIPORTS.NS', 'ASIANPAINT.NS', 'AXISBANK.NS', 'BAJAJ-AUTO.NS', 'BAJFINANCE.NS',
    'BAJAJFINSV.NS', 'BHARTIARTL.NS', 'BPCL.NS', 'BRITANNIA.NS', 'CIPLA.NS'
]

# Fetch historical data for top 10 Nifty 50 stocks
data = {ticker: yf.download(ticker, period='6mo') for ticker in nifty50_tickers}

# Create a DataFrame for closing prices, opening prices, and percentage changes
close_prices = pd.DataFrame({ticker: data[ticker]['Close'] for ticker in nifty50_tickers})
open_prices = pd.DataFrame({ticker: data[ticker]['Open'] for ticker in nifty50_tickers})
pct_change = close_prices.pct_change().dropna() * 100

# Calculate correlation matrix of closing prices
corr_matrix = close_prices.corr()

# Create a DataFrame to hold the annotation labels
labels = pd.DataFrame(index=close_prices.columns, columns=close_prices.columns)

# Populate the labels with detailed information
for i in close_prices.columns:
    for j in close_prices.columns:
        labels[i][j] = f'{corr_matrix[i][j]:.2f}\nOpen: {open_prices[i].iloc[-1]:.2f}\nClose: {close_prices[i].iloc[-1]:.2f}\nChange: {pct_change[i].iloc[-1]:.2f}%'

# Plot heatmap in table format
plt.figure(figsize=(24, 18))  # Further increase the figure size for better readability
sns.heatmap(corr_matrix, annot=labels, fmt='', cmap='coolwarm', linewidths=0.5, annot_kws={"size": 12})  # Increase font size
plt.title('Detailed Correlation Heatmap of Top 10 Nifty 50 Stocks', fontsize=24)
plt.xlabel('Stocks', fontsize=18)
plt.ylabel('Stocks', fontsize=18)
plt.xticks(rotation=45, ha='right', fontsize=16)  # Rotate x-axis labels for better visibility
plt.yticks(rotation=360, ha='right', fontsize=16)
plt.show()
