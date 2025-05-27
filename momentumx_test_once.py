import os
from pybit.unified_trading import HTTP
import time
import requests

# ENV Variablen
api_key = os.getenv("API_KEY")
api_secret = os.getenv("API_SECRET")
telegram_token = os.getenv("TELEGRAM_BOT_TOKEN")
telegram_chat_id = os.getenv("TELEGRAM_CHAT_ID")

session = HTTP(api_key=api_key, api_secret=api_secret)

def send_telegram(msg):
    requests.get(f"https://api.telegram.org/bot{telegram_token}/sendMessage", params={
        "chat_id": telegram_chat_id,
        "text": msg
    })

def test_usdt_order(symbol="BTCUSDT", usdt_amount=10):
    send_telegram("🧪 MomentumX: TEST beginnt")

    try:
        # Buy mit festem USDT-Betrag
        buy = session.place_order(
            category="spot",
            symbol=symbol,
            side="Buy",
            order_type="Market",
            order_amt=usdt_amount
        )
        send_telegram(f"📩 LIVE-ORDER Buy {usdt_amount} USDT → {buy}")

        time.sleep(5)

        # Letzter Preis holen
        price = float(session.get_tickers(category="spot", symbol=symbol)["result"]["list"][0]["lastPrice"])
        qty = round(usdt_amount / price, 6)

        # Sell nach Menge (nicht USDT)
        sell = session.place_order(
            category="spot",
            symbol=symbol,
            side="Sell",
            order_type="Market",
            qty=qty
        )
        send_telegram(f"📤 LIVE-ORDER Sell {qty} {symbol} → {sell}")

    except Exception as e:
        send_telegram(f"❌ Fehler: {str(e)}")

    send_telegram("✅ MomentumX TEST abgeschlossen")

# Start
test_usdt_order()
