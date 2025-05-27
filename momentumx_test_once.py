
import os
import time
import hmac
import hashlib
import requests
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("API_KEY")
api_secret = os.getenv("API_SECRET")

def create_signature(params, secret):
    sorted_params = sorted(params.items())
    query_string = "&".join([f"{key}={value}" for key, value in sorted_params])
    return hmac.new(bytes(secret, "utf-8"), query_string.encode("utf-8"), hashlib.sha256).hexdigest()

def send_test_order():
    url = "https://api.bybit.com/v5/order/create"
    timestamp = str(int(time.time() * 1000))

    params = {
        "category": "spot",
        "symbol": "BTCUSDT",
        "side": "Buy",
        "order_type": "Market",
        "qty": "0.0005",
        "timestamp": timestamp,
        "api_key": api_key,
    }

    sign = create_signature(params, api_secret)
    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    params["sign"] = sign
    response = requests.post(url, data=params, headers=headers)
    return response.json()

if __name__ == "__main__":
    print("🧪 MomentumX LIVE-TEST beginnt")
    result = send_test_order()
    print("📥 BUY ORDER →", result)
    print("✅ MomentumX LIVE-TEST abgeschlossen")
