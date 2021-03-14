import requests
from ebAlert import create_logger


log = create_logger(__name__)

def send_message(message, bot):


    send_text = """https://api.telegram.org/bot{}/sendMessage?chat_id={}
    &parse_mode=Markdown&text={}""".format(bot.token,
                                           bot.chat_id,
                                           message)
    response = requests.get(send_text)
    return response.json()['ok']


class TelegramBotError(Exception):
    def __init__(self):
        self.message = "Telegram Bot token and chat_id not found in database\n"
        super(TelegramBotError, self).__init__(self.message)