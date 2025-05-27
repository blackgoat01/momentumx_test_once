import os
from pybit.unified_trading import HTTP
import time
import requests

session = HTTP(
    api_key=os.getenv("API_KEY"),
    api_secret=os.getenv("API_SECRET")
)

symbol = "BTCUSDT"
usdt_einsatz = 10

def send_telegram(msg):
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {"chat_id": chat_id, "text": msg}
    requests.post(url, json=payload)

try:
    send_telegram("🧪 MomentumX: TEST beginnt")
    
    # Marktpreis-Kauf für 10 USDT
    buy = session.place_order(
        category="spot",
        symbol=symbol,
        side="Buy",
        order_type="Market",
        quoteOrderQty=usdt_einsatz
    )
    send_telegram(f"📩 TEST-BUY → {buy}")
    time.sleep(7)

    # Letzte Orderdaten holen, Menge auslesen
    fills = session.get_execution_list(category="spot", symbol=symbol, limit=1)
    qty = float(fills['result']['list'][0]['execQty']) if fills['result']['list'] else 0

    if qty > 0:
        sell = session.place_order(
            category="spot",
            symbol=symbol,
            side="Sell",
            order_type="Market",
            qty=round(qty, 6)
        )
        send_telegram(f"📤 TEST-SELL → {sell}")
    else:
        send_telegram("⚠️ Keine gültige Kaufmenge gefunden, Abbruch.")

except Exception as e:
    send_telegram(f"❌ Fehler: {str(e)}")

send_telegram("✅ MomentumX TEST abgeschlossen")
