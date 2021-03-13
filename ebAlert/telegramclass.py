import requests
from ebAlert import sqlmodel
from ebAlert import create_logger


log = create_logger(__name__)

def send_message(message):
    try:
        token, chat_id = sqlmodel.get_telegram_bot()
    except Exception as e:
        raise TelegramBotError


    send_text = """https://api.telegram.org/bot{}/sendMessage?chat_id={}
    &parse_mode=Markdown&text={}""".format(token,
                                           chat_id,
                                           message)
    response = requests.get(send_text)
    return response.json()['ok']


class TelegramBotError(Exception):
    def __init__(self):
        self.message = "Telegram Bot token and chat_id not found in database\n"
        super(TelegramBotError, self).__init__(self.message)