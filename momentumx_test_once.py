import os
from pybit.unified_trading import HTTP
import time
import requests

# Umrechnung USDT-Betrag zu BTC bei Marktpreis (für ca. 10 €)
USDT_AMOUNT = 10

# Umgebungsvariablen abrufen
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
TG_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TG_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Bybit-Session erstellen
session = HTTP(api_key=API_KEY, api_secret=API_SECRET)

# Telegram-Funktion
def send_telegram(message):
    url = f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage"
    data = {"chat_id": TG_CHAT_ID, "text": message}
    requests.post(url, data=data)

try:
    # Preis abrufen
    ticker = session.get_ticker(category="linear", symbol="BTCUSDT")
    btc_price = float(ticker['result']['list'][0]['lastPrice'])
    qty = round(USDT_AMOUNT / btc_price, 6)

    send_telegram("MomentumX: Starte LIVE-Kauf (10 €)...")

    # Kauf (Market)
    buy = session.place_order(
        category="linear",
        symbol="BTCUSDT",
        side="Buy",
        order_type="Market",
        qty=qty,
        time_in_force="FillOrKill"
    )
    send_telegram(f"🟢 Live-Buy erfolgreich: {buy}")

    time.sleep(5)

    # Verkauf (Market)
    sell = session.place_order(
        category="linear",
        symbol="BTCUSDT",
        side="Sell",
        order_type="Market",
        qty=qty,
        time_in_force="FillOrKill"
    )
    send_telegram(f"🔴 Live-Sell erfolgreich: {sell}")

    send_telegram("✅ MomentumX LIVE-TEST abgeschlossen.")
except Exception as e:
    send_telegram(f"❌ Fehler: {e}")