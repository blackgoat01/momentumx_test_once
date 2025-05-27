
import time
import hmac
import hashlib
import requests
import os

API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")

def sign(params):
    query_string = "&".join([f"{key}={value}" for key, value in sorted(params.items())])
    signature = hmac.new(bytes(API_SECRET, "utf-8"), query_string.encode("utf-8"), hashlib.sha256).hexdigest()
    return signature

def place_order(symbol, side, qty, price):
    url = "https://api.bybit.com/v5/order/create"
    timestamp = str(int(time.time() * 1000))
    params = {
        "apiKey": API_KEY,
        "symbol": symbol,
        "side": side,
        "orderType": "LIMIT",
        "qty": str(qty),
        "price": str(price),
        "timeInForce": "GTC",
        "timestamp": timestamp
    }
    params["sign"] = sign(params)
    response = requests.post(url, data=params)
    print(response.text)

if __name__ == "__main__":
    print("MomentumX: Starte Test-Buy...")
    place_order("BTCUSDT", "Buy", 0.001, 11000)
    time.sleep(10)
    print("MomentumX: Starte Test-Sell...")
    place_order("BTCUSDT", "Sell", 0.001, 11100)
    print("MomentumX: Test abgeschlossen.")
