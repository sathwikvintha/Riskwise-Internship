from flask import Flask, render_template, send_file
import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

app = Flask(__name__)

# Function to fetch NIFTY50 stocks data
def fetch_nifty50_data():
    tickers = [
        'RELIANCE.NS', 'TCS.NS', 'INFY.NS', 'HDFCBANK.NS', 'HINDUNILVR.NS', 
        'ICICIBANK.NS', 'KOTAKBANK.NS', 'LT.NS', 'ITC.NS', 'SBIN.NS', 
        'BHARTIARTL.NS', 'AXISBANK.NS', 'BAJFINANCE.NS', 'HCLTECH.NS', 
        'MARUTI.NS', 'ASIANPAINT.NS', 'ONGC.NS', 'TITAN.NS', 'ADANIGREEN.NS',
        'POWERGRID.NS', 'ULTRACEMCO.NS', 'NESTLEIND.NS', 'WIPRO.NS'
    ]
    data = {}
    for ticker in tickers:
        stock = yf.Ticker(ticker)
        hist = stock.history(period="5d")
        if not hist.empty:
            latest_data = hist.iloc[-1]
            prev_data = hist.iloc[-2]
            data[ticker] = {
                'Date': latest_data.name.strftime("%Y-%m-%d"),
                'Open': latest_data['Open'],
                'High': latest_data['High'],
                'Low': latest_data['Low'],
                'Close': latest_data['Close'],
                'Volume': latest_data['Volume'],
                'History': hist['Close'].tolist(),
                'Trend': 'up' if latest_data['Close'] > prev_data['Close'] else 'down',
                'Prediction': predict_next_close(hist['Close'].tolist())
            }
    
    sorted_data = dict(sorted(data.items(), key=lambda item: item[1]['Close'], reverse=True)[:9])
    return sorted_data

# Function to predict the next closing price
def predict_next_close(history):
    if len(history) < 5:
        return None
    
    x = np.arange(1, 6)
    y = np.array(history[-5:])
    A = np.vstack([x, np.ones(len(x))]).T
    slope, intercept = np.linalg.lstsq(A, y, rcond=None)[0]
    
    return slope * 6 + intercept

# Function to generate a heat map
def generate_heat_map(data):
    heatmap_data = []
    tickers = []
    for ticker, details in data.items():
        change = (details['Close'] - details['Open']) / details['Open'] * 100
        heatmap_data.append([details['Volume'], change])
        tickers.append(ticker)
    
    heatmap_data = np.array(heatmap_data)
    
    plt.figure(figsize=(10, 8))
    sns.heatmap(heatmap_data, annot=True, fmt=".2f", xticklabels=['Volume', '% Change'], yticklabels=tickers, cmap='coolwarm')
    plt.title('Heat Map of NIFTY50 Stocks')
    heatmap_path = os.path.join('static', 'heatmap.png')
    plt.savefig(heatmap_path)
    plt.close()
    return heatmap_path

@app.route('/')
def index():
    data = fetch_nifty50_data()
    heatmap_path = generate_heat_map(data)
    return render_template('index.html', data=data, heatmap_path=heatmap_path)

if __name__ == '__main__':
    app.run(debug=True)
