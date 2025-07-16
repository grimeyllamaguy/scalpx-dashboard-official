# scalpx_email_sms_discord.py
import smtplib
from email.message import EmailMessage
import requests
from twilio.rest import Client
import os

# Load env vars or config for creds
EMAIL_SENDER = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_APP_PASSWORD")
EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER")
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_TOKEN")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")
SMS_RECIPIENT = os.getenv("SMS_RECIPIENT")

def send_discord_alert(message: str):
    if not DISCORD_WEBHOOK_URL:
        print("⚠️ No Discord webhook URL configured")
        return False
    data = {"content": message}
    try:
        response = requests.post(DISCORD_WEBHOOK_URL, json=data)
        response.raise_for_status()
        print("✅ Discord alert sent")
        return True
    except Exception as e:
        print(f"❌ Discord alert failed: {e}")
        return False

def send_email_alert(subject: str, body: str):
    if not (EMAIL_SENDER and EMAIL_PASSWORD and EMAIL_RECEIVER):
        print("⚠️ Email credentials missing")
        return False
    try:
        email = EmailMessage()
        email["From"] = EMAIL_SENDER
        email["To"] = EMAIL_RECEIVER
        email["Subject"] = subject
        email.set_content(body)

        with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
            smtp.starttls()
            smtp.login(EMAIL_SENDER, EMAIL_PASSWORD)
            smtp.send_message(email)
        print("✅ Email alert sent")
        return True
    except Exception as e:
        print(f"❌ Email alert failed: {e}")
        return False

def send_sms_alert(body: str):
    if not (TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN and TWILIO_PHONE_NUMBER and SMS_RECIPIENT):
        print("⚠️ Twilio SMS credentials missing")
        return False
    try:
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        message = client.messages.create(
            body=body,
            from_=TWILIO_PHONE_NUMBER,
            to=SMS_RECIPIENT
        )
        print("✅ SMS alert sent")
        return True
    except Exception as e:
        print(f"❌ SMS alert failed: {e}")
        return False

def send_alert(message: str, discord=True, email=True, sms=True):
    results = {}
    if discord:
        results['discord'] = send_discord_alert(message)
    if email:
        results['email'] = send_email_alert("ScalpX Alert", message)
    if sms:
        results['sms'] = send_sms_alert(message)
    return results
