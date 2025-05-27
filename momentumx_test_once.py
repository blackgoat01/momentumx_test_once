
import os
import requests
import time
from dotenv import load_dotenv

# Telegram Setup
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
def send_telegram(msg):
    requests.post(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage", data={
        "chat_id": TELEGRAM_CHAT_ID,
        "text": msg
    })

# API Setup
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")

import hmac
import hashlib
import time
import requests
import json

def get_signature(api_key, api_secret, req_time, sign_params=""):
    param_str = str(req_time) + api_key + sign_params
    hash = hmac.new(bytes(api_secret, "utf-8"), param_str.encode("utf-8"), hashlib.sha256)
    return hash.hexdigest()

def place_market_buy_order(symbol, usdt_amount):
    url = "https://api.bybit.com/v5/market/tickers?category=spot&symbol=" + symbol
    try:
        response = requests.get(url)
        response.raise_for_status()
        price = float(response.json()["result"]["list"][0]["lastPrice"])
        qty = round(usdt_amount / price, 6)
    except Exception as e:
        send_telegram(f"❌ Fehler beim Abrufen des Preises: {e}")
        return

    # Order erstellen
    endpoint = "https://api.bybit.com/v5/order/create"
    req_time = str(int(time.time() * 1000))
    body = {
        "category": "spot",
        "symbol": symbol,
        "side": "Buy",
        "order_type": "Market",
        "qty": str(qty)
    }
    body_str = json.dumps(body, separators=(",", ":"))
    sign = get_signature(API_KEY, API_SECRET, req_time, body_str)

    headers = {
        "X-BAPI-API-KEY": API_KEY,
        "X-BAPI-SIGN": sign,
        "X-BAPI-TIMESTAMP": req_time,
        "X-BAPI-RECV-WINDOW": "5000",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(endpoint, headers=headers, data=body_str)
        send_telegram(f"📥 BUY ORDER → {response.text}")
    except Exception as e:
        send_telegram(f"❌ Fehler beim Platzieren der Buy-Order: {e}")

def main():
    send_telegram("🧪 MomentumX LIVE-TEST beginnt")
    place_market_buy_order("BTCUSDT", 10)
    send_telegram("✅ MomentumX LIVE-TEST abgeschlossen")

if __name__ == "__main__":
    main()
    
