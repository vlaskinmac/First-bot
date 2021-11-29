import os

import requests
import telegram

from dotenv import load_dotenv
from requests import ReadTimeout, HTTPError, ConnectionError


def get_data(token_devman, token_bot, bot_chat_id):
    bot = telegram.Bot(token=token_bot)
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
                             ' (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',
               'Authorization': 'Token {}'.format(token_devman)
               }

    url = 'https://dvmn.org/api/long_polling/'

    timestamp_param = None
    payload = ''
    while True:
        if timestamp_param:
            payload = {'timestamp': timestamp_param}
        try:
            response = requests.get(url, headers=headers, params=payload)
            response.raise_for_status()
            timestamp_param = response.json()['last_attempt_timestamp']
            if [status['is_negative'] for status in response.json()['new_attempts']]:
                bot.send_message(text='Преподаватель проверил работу!', chat_id=bot_chat_id)
                bot.send_message(
                    text='К большому сожалению в хорошей работе нашлись незначчительные ошибки!',
                    chat_id=bot_chat_id,
                )
            else:
                bot.send_message(text='Преподаватель проверил работу!', chat_id=bot_chat_id)
                bot.send_message(
                    text='Преподавателю понравилось!',
                    chat_id=bot_chat_id,
                )
        except (ReadTimeout, HTTPError, ConnectionError) as exc:
            print(exc)


if __name__ == '__main__':
    load_dotenv()
    token_devman = os.getenv('API_KEY_DEVMAN')
    token_bot = os.getenv('BOT_KEY')
    bot_chat_id = os.getenv('CHAT_ID')
    get_data(token_devman, token_bot, bot_chat_id)
