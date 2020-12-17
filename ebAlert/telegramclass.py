import requests
try:
    from ebAlert.credential import TOKEN, CHAT_ID
except ImportError:
    TOKEN = ""
    CHAT_ID = ""

def sendMessage(message):
    send_text = """https://api.telegram.org/bot{}/sendMessage?chat_id={}
    &parse_mode=Markdown&text={}""".format(TOKEN,
                                           CHAT_ID,
                                           message)
    response = requests.get(send_text)
    return response.json()['ok']
