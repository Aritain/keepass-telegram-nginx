import os
import time
import telegram


db_file = '/db/main.kdbx'
timeout = int(os.environ['TIMEOUT'])
telegram_token = os.environ['TOKEN']
user_id = os.environ['USER']


def send_db():
    try:
        message = bot.sendDocument(chat_id=user_id, document=open(db_file, 'rb'))
    except:
        pass
    try:
        bot.delete_message(chat_id=user_id, message_id=message.message_id-1)
    except:
        pass
    return 


if __name__ == '__main__':
    bot = telegram.Bot(token=telegram_token)
    while True:
        send_db()
        time.sleep(timeout)
