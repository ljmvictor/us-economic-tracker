# us-economic-tracker

An automated, end-to-end data pipeline and visualization dashboard tracking the relationship between US macroeconomic indicators (FRED) and stock market performance (Yahoo Finance). 

## Architecture
* **Data Ingestion:** Python (`yfinance`, `fredapi`)
* **Automation:** GitHub Actions (Daily CI/CD pipeline)
* **Front-End:** Streamlit & Plotly
* **Deployment:** Streamlit Community Cloud

## Objectives
1. Provide a daily-updated, interactive view of how inflation, interest rates, and employment affect the S&P 500, Nasdaq, and DJIA.
2. Demonstrate a fully automated data engineering and analytics workflow.