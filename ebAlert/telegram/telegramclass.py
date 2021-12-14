import requests
from ebAlert.core.config import settings


def send_message(message):
    send_text_url = settings.TELEGRAM_API_URL + message + ""
    response = requests.get(send_text_url)
    return response.json()['ok']
