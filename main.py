import os
import requests
from fastapi import FastAPI, HTTPException, Request

app = FastAPI(title="Radar Entry Win Bot - Alertas")

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "TU_BOT_TOKEN_AQUI")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "TU_CHAT_ID_AQUI")

def send_telegram_message(message: str) -> bool:
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }
    response = requests.post(url, json=payload)
    return response.status_code == 200

@app.get("/")
def read_root():
    return {"status": "online", "system": "Radar Entry Win Telegram Bridge"}

@app.post("/webhook")
async def receive_webhook(request: Request):
    try:
        data = await request.json()
    except Exception:
        body = await request.body()
        data = {"message": body.decode("utf-8")}

    ticker = data.get("ticker", "XAUUSD")
    action = data.get("action", "SEÑAL").upper()
    price = data.get("price", "N/A")
    quality = data.get("quality", "N/A")

    telegram_msg = (
        f"<b>🎯 NUEVA SEÑAL DETECTADA</b>\n\n"
        f"<b>Activo:</b> {ticker}\n"
        f"<b>Acción:</b> {action}\n"
        f"<b>Precio de Entrada:</b> {price}\n"
        f"<b>Calidad de Señal:</b> ({quality})\n\n"
        f"<i>🤖 Radar Entry Win Localizator - Pro Bot</i>"
    )

    success = send_telegram_message(telegram_msg)
    if not success:
        raise HTTPException(status_code=500, detail="Error al despachar el mensaje a Telegram")

    return {"status": "success", "message_sent": True}
