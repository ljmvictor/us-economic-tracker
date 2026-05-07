import os
from dotenv import load_dotenv
from fredapi import Fred
import yfinance as yf
import pandas as pd

# 1. Load the secure environment variables from the .env file
load_dotenv()
FRED_API_KEY = os.getenv("FRED_API_KEY")

# 2. Initialize the FRED client using your secure key
fred = Fred(api_key=FRED_API_KEY)

def fetch_and_save_data():
    print("Initializing Data Pipeline...")
    
    # NEW: Ensure the 'data' directory exists before we try to save files there
    os.makedirs('data', exist_ok=True)
    
    try:
        # 3. Fetch Macro Data: Federal Funds Rate (Ticker: FEDFUNDS)
        print("Fetching Federal Funds Rate from FRED...")
        fed_funds = fred.get_series('FEDFUNDS')
        
        # NEW: Convert the FRED Series into a structured DataFrame and save it
        df_fed = pd.DataFrame(fed_funds, columns=['Fed_Funds_Rate'])
        df_fed.index.name = 'Date'
        fed_csv_path = 'data/fed_funds_rate.csv'
        df_fed.to_csv(fed_csv_path)
        print(f"✅ Saved Fed Funds data to {fed_csv_path}")
        
        # 4. Fetch Market Data: S&P 500 (Ticker: ^GSPC) for the last 1 year
        print("Fetching S&P 500 data from Yahoo Finance...")
        sp500 = yf.download('^GSPC', period='1y')
        
        # NEW: Save the Yahoo Finance DataFrame directly to CSV
        sp500_csv_path = 'data/sp500_daily.csv'
        sp500.to_csv(sp500_csv_path)
        print(f"✅ Saved S&P 500 data to {sp500_csv_path}")
        
        print("\n🎉 PIPELINE COMPLETE! Data is securely stored and ready for the dashboard.")

    except Exception as e:
        print(f"\n❌ ERROR: Something went wrong pulling the data. Details: {e}")

if __name__ == "__main__":
    fetch_and_save_data()