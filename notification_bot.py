import os
import re
import time

import requests
import telegram

from dotenv import load_dotenv
from requests import ReadTimeout, HTTPError, ConnectionError


def checks_status_task(token_devman, token_bot, bot_chat_id):
    bot = telegram.Bot(token=token_bot)
    headers = {
               'Authorization': 'Token {}'.format(token_devman)
               }

    url = 'https://dvmn.org/api/long_polling/'

    timestamp_param = 0
    read_timeout = 0.06
    while True:
        payload = {'timestamp': timestamp_param + read_timeout}
        try:
            response = requests.get(url, headers=headers, params=payload)
            response.raise_for_status()
            response_collections = response.json()
            if response_collections['status'] == 'timeout':
                timestamp_param = response_collections['timestamp_to_request']
                bot.send_message(
                    text='Работа все еще не поверена! Нужно дать преподавателю еще 90 секунд на проверкку!',
                    chat_id=bot_chat_id
                )
            elif response_collections['status'] == 'found':
                timestamp_param = response_collections['last_attempt_timestamp']
                if [status['is_negative'] for status in response_collections['new_attempts']][0]:
                    bot.send_message(text='Преподаватель проверил работу!', chat_id=bot_chat_id)
                    bot.send_message(
                        text='К большому сожалению в хорошей работе нашлись незначительные ошибки!',
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
            if re.findall(r'NewConnectionError', str(exc)):
                time.sleep(5)


if __name__ == '__main__':
    load_dotenv()
    token_devman = os.getenv('API_KEY_DEVMAN')
    token_bot = os.getenv('BOT_KEY')
    bot_chat_id = os.getenv('CHAT_ID')
    checks_status_task(token_devman, token_bot, bot_chat_id)
