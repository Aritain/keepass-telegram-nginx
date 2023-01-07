import os
import time
import telegram
import pyminizip


db_name = os.environ['DB']
db_file = f'/db/{db_name}.kdbx'
zip_file = f'/tmp/{db_name}.zip'
timeout = int(os.environ['TIMEOUT'])
telegram_token = os.environ['TOKEN']
user_id = os.environ['USER']
zip_passwd = os.environ['ZIP_PASSWD']


def prepare_db():
    if os.path.exists(zip_file):
        os.remove(zip_file)
    pyminizip.compress(db_file, "", zip_file, zip_passwd, 1)

def send_db():
    try:
        message = bot.sendDocument(chat_id=user_id, document=open(zip_file, 'rb'))
    except:
        pass
    for i in range (1,10):
        try:
            bot.delete_message(chat_id=user_id, message_id=message.message_id-i)
        except:
            pass
            break
    return


if __name__ == '__main__':
    bot = telegram.Bot(token=telegram_token)
    while True:
        prepare_db()
        send_db()
        time.sleep(timeout)
