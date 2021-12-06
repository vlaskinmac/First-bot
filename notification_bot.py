import os
import time

import requests
import telegram

from dotenv import load_dotenv
from requests import ReadTimeout, HTTPError, ConnectionError


def check_task_status(token_devman, token_bot, bot_chat_id):
    bot = telegram.Bot(token=token_bot)
    headers = {
               'Authorization': 'Token {}'.format(token_devman)
               }

    url = 'https://dvmn.org/api/long_polling/'

    timestamp_param = 0
    while True:
        payload = {'timestamp': timestamp_param}
        try:
            response = requests.get(url, headers=headers, params=payload)
            response.raise_for_status()
            response_reviews = response.json()
            if response_reviews['status'] == 'timeout':
                timestamp_param = response_reviews['timestamp_to_request']
            elif response_reviews['status'] == 'found':
                timestamp_param = response_reviews['last_attempt_timestamp']
                last_attempt = response_reviews['new_attempts'][0]
                if last_attempt['is_negative']:
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

        except ReadTimeout:
            pass
        except HTTPError as exc:
            print(exc)
        except ConnectionError:
            time.sleep(5)


if __name__ == '__main__':
    load_dotenv()
    token_devman = os.getenv('API_KEY_DEVMAN')
    token_bot = os.getenv('BOT_KEY')
    bot_chat_id = os.getenv('CHAT_ID')
    check_task_status(token_devman, token_bot, bot_chat_id)
