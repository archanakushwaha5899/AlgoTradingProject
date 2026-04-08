# Algo Trading Analytics System

## Project Overview

This project is an end-to-end trading analytics system that automates stock data processing, generates trading signals, tracks portfolio performance, and visualizes insights using Power BI.

---

## Key Features

Multi-stock analysis (10 stocks across sectors)
Automated trading signals using SMA (20 & 50)
Google Sheets integration for real-time logging
Duplicate-safe logging system
Portfolio tracking (Quantity + Profit/Loss)
Interactive Power BI dashboard

---

## Tech Stack

**Python**: Pandas, NumPy
**API**: Yahoo Finance (yfinance)
**Google Sheets API**: gspread, oauth2client
**Visualization**: Microsoft Power BI

---

## Project Structure

```
ALGO_TRADING_PROJECT/
│
├── data/
├── notebooks/
│   ├── 01_EDA.ipynb
│   ├── 02_trading_bot.ipynb
│
├── src/
│   ├── main.py
│   └── data_fetch.py
│
├── dashboard/
│   ├── algo_trading_dashboard.pbix
│   └── dashboard_preview.pdf
│
├── credentials.json  (not uploaded to GitHub)
├── requirements.txt
└── README.md
```

---

## How to Run the Project

### Install Dependencies

```
pip install -r requirements.txt
```

---

### Setup Google Sheets API

* Create a Google Cloud service account
* Download `credentials.json`
* Place it in the project root
* Share your Google Sheet with the service account email

---

### Run the Trading Bot

```
python src/main.py
```

---

## Dashboard Insights

The Power BI dashboard provides:

* Total Profit & Loss (PnL)
* Profit vs Loss distribution
* Stock-wise performance
* Buy vs Sell analysis
* Price trends over time
* Interactive filters (Stock, Date)

---

## Trading Strategy

* Uses **Simple Moving Average (SMA) crossover**
* BUY → when SMA 20 > SMA 50
* SELL → when SMA 20 < SMA 50

---

## Key Learnings

* Built an end-to-end data pipeline
* Automated financial data processing
* Implemented trading logic
* Designed interactive dashboards
* Applied real-world analytics concepts

---

## Future Improvements

* Real-time trading signals
* Streamlit dashboard
* Cloud deployment (AWS)
* Advanced indicators (RSI, MACD)

---


* GitHub: https://github.com/archanakushwaha5899
* LinkedIn: https://linkedin.com/in/archana-kushwaha-531153226

---
