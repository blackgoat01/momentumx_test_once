
import os
import time
import requests
import hmac
import hashlib
import json

SYMBOL = "BTCUSDT"
USDT_EINSATZ = 10
BASE_URL = "https://api.bybit.com"

API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def create_signature(payload):
    return hmac.new(API_SECRET.encode(), payload.encode(), hashlib.sha256).hexdigest()

def send_telegram(msg):
    try:
        requests.post(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
                      data={"chat_id": TELEGRAM_CHAT_ID, "text": msg})
    except Exception as e:
        print("Telegram Fehler:", e)

def get_price():
    url = f"{BASE_URL}/v5/market/tickers"
    params = {"category": "spot", "symbol": SYMBOL}
    r = requests.get(url, params=params)
    return float(r.json()["result"]["list"][0]["lastPrice"])

def place_order(side, qty, price):
    timestamp = str(int(time.time() * 1000))
    body = {
        "category": "spot",
        "symbol": SYMBOL,
        "side": side,
        "orderType": "Limit",
        "qty": str(qty),
        "price": str(price),
        "timeInForce": "GTC"
    }
    payload = timestamp + API_KEY + "5000" + json.dumps(body)
    sign = create_signature(payload)
    headers = {
        "X-BAPI-API-KEY": API_KEY,
        "X-BAPI-TIMESTAMP": timestamp,
        "X-BAPI-SIGN": sign,
        "Content-Type": "application/json"
    }
    url = f"{BASE_URL}/v5/order/create"
    r = requests.post(url, headers=headers, data=json.dumps(body))
    send_telegram(f"📨 TEST-ORDER {side}: {qty} BTC @ {price} USDT → {r.text}")

def run_single_trade():
    try:
        price = get_price()
        qty = round(USDT_EINSATZ / price, 6)

        send_telegram("🧪 MomentumX: TEST beginnt")
        # KAUF
        place_order("Buy", qty, round(price, 2))
        time.sleep(10)  # kurze Pause, simuliert Wartezeit
        # VERKAUF
        place_order("Sell", qty, round(price * 1.001, 2))  # minimal höherer Preis
        send_telegram("✅ MomentumX TEST abgeschlossen")
    except Exception as e:
        send_telegram(f"❌ Fehler beim Test: {e}")

if __name__ == "__main__":
    run_single_trade()
