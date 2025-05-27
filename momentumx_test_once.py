import os
from pybit.unified_trading import HTTP
import time
import requests

# ENV Variablen aus Render
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

def get_price(symbol):
    response = session.get_ticker_price(category="spot", symbol=symbol)
    return float(response["result"]["price"])

def test_trade(symbol="BTCUSDT", amount_usdt=10):
    send_telegram("🧪 MomentumX: TEST beginnt")
    
    try:
        price = get_price(symbol)
        qty = round(amount_usdt / price, 6)

        buy = session.place_order(
            category="spot",
            symbol=symbol,
            side="Buy",
            order_type="Market",
            qty=qty
        )
        send_telegram(f"📩 LIVE-ORDER Buy {qty} {symbol} @ {price} USDT → {buy}")

        time.sleep(3)

        sell = session.place_order(
            category="spot",
            symbol=symbol,
            side="Sell",
            order_type="Market",
            qty=qty
        )
        send_telegram(f"📤 LIVE-ORDER Sell {qty} {symbol} @ {price} USDT → {sell}")

    except Exception as e:
        send_telegram(f"❌ Fehler: {str(e)}")

    send_telegram("✅ MomentumX TEST abgeschlossen")

# Start
test_trade()
