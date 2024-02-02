import os
import logging


class Settings:
    TOKEN = os.environ.get("TOKEN") or "Your_secret_key"
    CHAT_ID = os.environ.get("CHAT_ID") or "Your_chat_id"
    FILE_LOCATION = os.path.join(os.path.expanduser("~"), "ebayklein.db")
    TELEGRAM_API_URL = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&parse_mode=HTML&"""
    LOGGING = os.environ.get("LOGGING") or logging.ERROR
    URL_BASE = "https://www.kleinanzeigen.de"


settings = Settings()
