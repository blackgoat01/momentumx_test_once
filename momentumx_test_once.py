
import os
import requests
import time

api_key = os.getenv("API_KEY")
api_secret = os.getenv("API_SECRET")
telegram_token = os.getenv("TELEGRAM_BOT_TOKEN")
telegram_chat_id = os.getenv("TELEGRAM_CHAT_ID")

def send_telegram(msg):
    url = f"https://api.telegram.org/bot{telegram_token}/sendMessage"
    data = {"chat_id": telegram_chat_id, "text": msg}
    requests.post(url, data=data)

def test_order():
    send_telegram("🧪 MomentumX: TEST beginnt")

    # Simulierter Test-Buy
    print("MomentumX: Starte Test-Buy...")
    result_buy = {
        "retCode": 10001,
        "retMsg": "TEST: Buy Order simuliert"
    }
    send_telegram(f"📩 TEST-ORDER Buy → {result_buy}")

    # Kurze Pause
    time.sleep(1)

    # Simulierter Test-Sell
    print("MomentumX: Starte Test-Sell...")
    result_sell = {
        "retCode": 10001,
        "retMsg": "TEST: Sell Order simuliert"
    }
    send_telegram(f"📤 TEST-ORDER Sell → {result_sell}")

    send_telegram("✅ MomentumX TEST abgeschlossen")

if __name__ == "__main__":
    test_order()
