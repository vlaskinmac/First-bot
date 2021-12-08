import logging


class TelegramLogsHandler(logging.Handler):

    def __init__(self, bot, bot_chat_id):
        super().__init__()
        self.bot_chat_id = bot_chat_id
        self.bot = bot

    def emit(self, record):
        log_entry = self.format(record)
        self.bot.send_message(chat_id=self.bot_chat_id, text=log_entry)


