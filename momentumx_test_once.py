
import os
import time
import requests
from pybit.unified_trading import HTTP

API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Telegram-Funktion
def send_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": TELEGRAM_CHAT_ID, "text": message})

# Bybit-Sitzung
session = HTTP(api_key=API_KEY, api_secret=API_SECRET)

send_telegram("🧪 MomentumX LIVE-TEST beginnt")

try:
    # Kurs abrufen
    price_data = session.get_tickers(category="spot", symbol="BTCUSDT")
    btc_price = float(price_data["result"]["list"][0]["lastPrice"])

    # Menge berechnen für 10 USDT
    usdt_amount = 10
    btc_qty = round(usdt_amount / btc_price, 6)

    # Order senden
    response = session.place_order(
        category="spot",
        symbol="BTCUSDT",
        side="Buy",
        order_type="Market",
        qty=btc_qty
    )

    send_telegram(f"📥 BUY ORDER erfolgreich:\n{response}")
except Exception as e:
    send_telegram(f"❌ FEHLER bei BUY ORDER:\n{e}")

send_telegram("✅ MomentumX LIVE-TEST abgeschlossen")
