# scalpx_trade_logger.py
import csv
import os
from datetime import datetime

LOG_FILE = "trade_log.csv"

def log_trade(ticker: str, entry_price: float, exit_price: float, qty: int, result: str):
    """
    Logs trade details to CSV file with timestamp.
    """
    file_exists = os.path.isfile(LOG_FILE)
    with open(LOG_FILE, mode='a', newline='') as f:
        writer = csv.writer(f)
        if not file_exists:
            # Write headers if file doesn't exist
            writer.writerow(["Timestamp", "Ticker", "Entry Price", "Exit Price", "Quantity", "Result"])
        writer.writerow([datetime.now().isoformat(), ticker, entry_price, exit_price, qty, result])
    print(f"📝 Trade logged: {ticker} | {result}")
