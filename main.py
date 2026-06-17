from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse
from dotenv import load_dotenv
import os
from twilio.rest import Client

load_dotenv()

app = FastAPI()

TWILIO_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_WHATSAPP_NUMBER = "whatsapp:+14155238886"  # Twilio sandbox number, check yours in console
client = Client(TWILIO_SID, TWILIO_TOKEN)

@app.get("/")
def health_check():
    return {"status": "alive"}

@app.post("/webhook/whatsapp")
async def whatsapp_webhook(request: Request):
    form_data = await request.form()
    incoming_msg = form_data.get("Body", "")
    sender = form_data.get("From", "")

    print(f"Received message: '{incoming_msg}' from {sender}")

    client.messages.create(
        body="Got your message!",
        from_=TWILIO_WHATSAPP_NUMBER,
        to=sender
    )

    return PlainTextResponse("OK", status_code=200)