from flask import Flask, render_template, send_file
import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import datetime


app = Flask(__name__)

# Function to fetch NIFTY50 stocks data
def fetch_nifty50_data():
    tickers = [
        'RELIANCE.NS', 'TCS.NS', 'INFY.NS', 'HDFCBANK.NS', 'HINDUNILVR.NS', 
        'ICICIBANK.NS', 'KOTAKBANK.NS', 'LT.NS', 'ITC.NS', 'SBIN.NS', 
        'BHARTIARTL.NS', 'AXISBANK.NS', 'BAJFINANCE.NS', 'HCLTECH.NS', 
        'MARUTI.NS', 'ASIANPAINT.NS', 'ONGC.NS', 'TITAN.NS', 'ADANIGREEN.NS',
        'POWERGRID.NS', 'ULTRACEMCO.NS', 'NESTLEIND.NS', 'WIPRO.NS',
        'NTPC.NS', 'SUNPHARMA.NS', 'HDFC.NS', 'COALINDIA.NS', 'TATAMOTORS.NS',
        'GRASIM.NS', 'ADANIPORTS.NS', 'BAJAJ-AUTO.NS', 'TATASTEEL.NS', 
        'TECHM.NS', 'HEROMOTOCO.NS', 'JSWSTEEL.NS', 'DIVISLAB.NS', 'M&M.NS',
        'BRITANNIA.NS', 'BPCL.NS', 'INDUSINDBK.NS', 'EICHERMOT.NS', 
        'SHREECEM.NS', 'CIPLA.NS', 'DRREDDY.NS', 'UPL.NS', 'APOLLOHOSP.NS',
        'SBILIFE.NS', 'HINDALCO.NS'
    ]
    return fetch_stock_data(tickers)

# Function to fetch NIFTY100 stocks data
def fetch_nifty100_data():
    tickers = [
        'RELIANCE.NS', 'TCS.NS', 'INFY.NS', 'HDFCBANK.NS', 'HINDUNILVR.NS', 
        'ICICIBANK.NS', 'KOTAKBANK.NS', 'LT.NS', 'ITC.NS', 'SBIN.NS', 
        'BHARTIARTL.NS', 'AXISBANK.NS', 'BAJFINANCE.NS', 'HCLTECH.NS', 
        'MARUTI.NS', 'ASIANPAINT.NS', 'ONGC.NS', 'TITAN.NS', 'ADANIGREEN.NS',
        'POWERGRID.NS', 'ULTRACEMCO.NS', 'NESTLEIND.NS', 'WIPRO.NS',
        'NTPC.NS', 'SUNPHARMA.NS', 'HDFC.NS', 'COALINDIA.NS', 'TATAMOTORS.NS',
        'GRASIM.NS', 'ADANIPORTS.NS', 'BAJAJ-AUTO.NS', 'TATASTEEL.NS', 
        'TECHM.NS', 'HEROMOTOCO.NS', 'JSWSTEEL.NS', 'DIVISLAB.NS', 'M&M.NS',
        'BRITANNIA.NS', 'BPCL.NS', 'INDUSINDBK.NS', 'EICHERMOT.NS', 
        'SHREECEM.NS', 'CIPLA.NS', 'DRREDDY.NS', 'UPL.NS', 'APOLLOHOSP.NS',
        'SBILIFE.NS', 'HINDALCO.NS', 'ABBOTINDIA.NS', 'ADANIENT.NS', 'AMBUJACEM.NS', 
        'AUROPHARMA.NS', 'BAJAJFINSV.NS', 'BANDHANBNK.NS', 'BANKBARODA.NS', 
        'BERGEPAINT.NS', 'BOSCHLTD.NS', 'CADILAHC.NS', 'CHOLAFIN.NS', 
        'DABUR.NS', 'DLF.NS', 'GAIL.NS', 'GLAXO.NS', 'GODREJCP.NS', 
        'HAVELLS.NS', 'ICICIPRULI.NS', 'IGL.NS', 'INDIGO.NS', 'JINDALSTEL.NS', 
        'LUPIN.NS', 'MCDOWELL-N.NS', 'MRF.NS', 'MUTHOOTFIN.NS', 'PEL.NS', 
        'PETRONET.NS', 'PIDILITIND.NS', 'PNB.NS', 'SAIL.NS', 'TORNTPHARM.NS', 
        'TVSMOTOR.NS', 'VEDL.NS', 'YESBANK.NS', 'ZEEL.NS'
    ]
    return fetch_stock_data(tickers)


# General function to fetch stock data
def fetch_stock_data(tickers):
    data = {}
    for ticker in tickers:
        stock = yf.Ticker(ticker)
        hist = stock.history(period="5d")
        
        if not hist.empty:
            latest_data = hist.iloc[-1]
            prev_data = hist.iloc[-2]
            change_percentage = ((latest_data['Close'] - latest_data['Open']) / latest_data['Open']) * 100
            data[ticker] = {
                'Date': latest_data.name.strftime("%Y-%m-%d"),
                'Open': latest_data['Open'],
                'High': latest_data['High'],
                'Low': latest_data['Low'],
                'Close': latest_data['Close'],
                'Volume': latest_data['Volume'],
                'History': hist['Close'].tolist(),
                'Trend': 'up' if latest_data['Close'] > prev_data['Close'] else 'down',
                'Prediction': predict_next_close(hist['Close'].tolist()),
                'Change': round(change_percentage, 2) 
            }
    
    sorted_data = dict(sorted(data.items(), key=lambda item: item[1]['Close'], reverse=True)[:50])
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
    plt.title('Heat Map of NIFTY Stocks')
    heatmap_path = os.path.join('static', 'heatmap.png')
    plt.savefig(heatmap_path)
    plt.close()
    return heatmap_path

@app.route('/')
def index():
    data = fetch_nifty50_data()
    heatmap_path = generate_heat_map(data)
    profitable_stocks = {k: v for k, v in data.items() if v['Trend'] == 'up'}
    non_profitable_stocks = {k: v for k, v in data.items() if v['Trend'] == 'down'}
    return render_template('index.html', profitable_stocks=profitable_stocks, non_profitable_stocks=non_profitable_stocks, heatmap_path=heatmap_path)

@app.route('/nifty50')
def nifty50():
    data = fetch_nifty50_data()
    heatmap_path = generate_heat_map(data)
    profitable_stocks = {k: v for k, v in data.items() if v['Trend'] == 'up'}
    non_profitable_stocks = {k: v for k, v in data.items() if v['Trend'] == 'down'}
    return render_template('nifty50.html', nifty50_data=data, profitable_stocks=profitable_stocks, non_profitable_stocks=non_profitable_stocks, heatmap_path=heatmap_path)

@app.route('/nifty100')
def nifty100():
    data = fetch_nifty100_data()
    heatmap_path = generate_heat_map(data)
    profitable_stocks = {k: v for k, v in data.items() if v['Trend'] == 'up'}
    non_profitable_stocks = {k: v for k, v in data.items() if v['Trend'] == 'down'}
    return render_template('nifty100.html', nifty100_data=data, profitable_stocks=profitable_stocks, non_profitable_stocks=non_profitable_stocks, heatmap_path=heatmap_path)

@app.route('/stock/<ticker>')
def stock_details(ticker):
    # Fetch historical data for the selected stock
    end_date = datetime.date.today()
    start_date = end_date - datetime.timedelta(days=30 * 1)  # 5 years
    stock_data = yf.download(ticker, start=start_date, end=end_date)

    # Process the historical data as needed
    # For example, calculate profit and loss over the last 5 years

    # Render the new page with the stock details
    return render_template('stock_details.html', ticker=ticker, stock_data=stock_data)


if __name__ == '__main__':
    app.run(debug=True)
