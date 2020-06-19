import requests

TOKEN = ""
CHAT_ID = ""

def sendMessage(message):
    send_text = 'https://api.telegram.org/bot{}/sendMessage?chat_id={}&parse_mode=Markdown&text={}'.format(TOKEN,
                                                                                                           CHAT_ID,
                                                                                                           message)
    response = requests.get(send_text)
    return response.json()['ok']

if __name__ =="__main__":
    sendMessage("Coucou\nC'est un test. ")