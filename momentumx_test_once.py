import os
from pybit.unified_trading import HTTP
import time
import requests

# Umgebungsvariablen laden
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Telegram-Sende-Funktion
def send_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    try:
        requests.post(url, data=data)
    except Exception as e:
        print(f"Telegram-Fehler: {e}")

# Session initialisieren
try:
    session = HTTP(api_key=API_KEY, api_secret=API_SECRET)
except Exception as e:
    send_telegram(f"❌ Verbindung zu Bybit fehlgeschlagen: {e}")
    exit()

send_telegram("🧪 MomentumX LIVE-TEST beginnt")

try:
    # Kauforder mit 10 USDT quoteOrderQty
    response = session.place_order(
        category="spot",
        symbol="BTCUSDT",
        side="Buy",
        order_type="Market",
        quoteOrderQty="10"
    )
    send_telegram(f"📥 BUY ORDER erfolgreich:\n{response}")
except Exception as e:
    send_telegram(f"❌ FEHLER bei BUY ORDER:\n{e}")

send_telegram("✅ MomentumX LIVE-TEST abgeschlossen")
