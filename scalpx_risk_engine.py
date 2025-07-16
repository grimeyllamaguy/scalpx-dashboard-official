# scalpx_risk_engine.py

def calculate_position_size(account_balance: float, risk_percent: float, entry_price: float, stop_loss_price: float):
    """
    Calculates quantity of shares/contracts to buy.
    account_balance: total trading capital
    risk_percent: fraction of capital willing to risk (e.g., 0.02 for 2%)
    entry_price: price at entry
    stop_loss_price: price at stop loss
    """
    risk_amount = account_balance * risk_percent
    risk_per_share = abs(entry_price - stop_loss_price)
    if risk_per_share == 0:
        print("⚠️ Risk per share is zero, cannot calculate position size.")
        return 0
    qty = risk_amount / risk_per_share
    return max(1, int(qty))  # At least 1 share

def calculate_stop_loss(entry_price: float, stop_loss_percent: float = 0.02):
    """
    Calculates stop loss price given entry and percent.
    Default stop loss is 2% below entry.
    """
    return entry_price * (1 - stop_loss_percent)
