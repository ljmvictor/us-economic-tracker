import os
from dotenv import load_dotenv
from fredapi import Fred
import yfinance as yf
import pandas as pd

load_dotenv()
FRED_API_KEY = os.getenv("FRED_API_KEY")
fred = Fred(api_key=FRED_API_KEY)

def fetch_and_save_data():
    print("Initializing Full Historical Data Pipeline...")
    os.makedirs('data', exist_ok=True)
    
    try:
        # 1. Macro Indicators from FRED
        print("\n🏦 Fetching Macro Data from FRED...")
        macro_metrics = {
            'FEDFUNDS': 'fed_funds_rate.csv', # Federal Funds Rate
            'CPIAUCSL': 'cpi.csv',            # Consumer Price Index for All Urban Consumers: All Items
            'UNRATE': 'unemployment.csv',     # Unemployment Rate
            'GDP': 'gdp.csv'                  # Gross Domestic Product
        }
        
        for ticker, filename in macro_metrics.items():
            series = fred.get_series(ticker)
            df = pd.DataFrame(series, columns=['Value'])
            df.index.name = 'Date'
            df.to_csv(f'data/{filename}')
            print(f"✅ Saved {ticker} to {filename}")
            
        # 2. Market Indices from Yahoo Finance (All-Time History)
        print("\n📈 Fetching Market Data from Yahoo Finance...")
        market_indices = {
            '^GSPC': 'sp500.csv', # S&P 500
            '^IXIC': 'nasdaq.csv', # Nasdaq Composite
            '^DJI': 'djia.csv' # Dow Jones Industrial Average
        }
        
        for ticker, filename in market_indices.items():
            # 'period="max"' pulls all available historical data
            raw_data = yf.download(ticker, period='max')
            df = pd.DataFrame(raw_data['Close'])
            df.columns = ['Close'] # Ensure clean column naming
            df.index.name = 'Date'
            df.to_csv(f'data/{filename}')
            print(f"✅ Saved {ticker} to {filename}")
            
        print("\n🎉 HISTORICAL PIPELINE COMPLETE! All datasets updated.")

    except Exception as e:
        print(f"\n❌ ERROR: {e}")

if __name__ == "__main__":
    fetch_and_save_data()