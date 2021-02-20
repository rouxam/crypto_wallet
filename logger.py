import os
import abc
import logging
import telegram
import traceback

from constants import *
from util.pretty_now import pretty_datetime_now

class TelegramFormatter(logging.Formatter):
    def __init__(self):
        super().__init__()

    def format(self, record):
        # Format traceback if available
        if record.exc_info:
            exc_msg = "\n" + "\n".join(
                traceback.format_exception(*record.exc_info))
        else:
            exc_msg = ""
        msg = record.module + ": " + (record.msg % record.args) + exc_msg
        return msg

class TerminalFormatter(logging.Formatter):
    def __init__(self):
        super().__init__()

    def format(self, record):
        # Format traceback if available
        if record.exc_info:
            exc_msg = "\n" + "\n".join(
                traceback.format_exception(*record.exc_info))
        else:
            exc_msg = ""
        msg = pretty_datetime_now() + ": " + \
                record.module + ": "+ \
                (record.msg % record.args) + exc_msg
        return msg

class TelegramNormalHandler(logging.Handler):
    "Handler object to send Low Priority messages via Telegram"

    def __init__(self):
        super().__init__(level=logging.DEBUG)
        self.__client = telegram.Bot(TELEGRAM_CRYPTO_WALLET_TOKEN)
        self.setFormatter(TelegramFormatter())
        self.setLevel(logging.DEBUG)

    def emit(self, record: logging.LogRecord):
        message = self.format(record)
        try:
            self.__client.sendMessage(chat_id=TELEGRAM_CHAT_ID, text=message)
        except Exception as err: # pylint: disable=broad-except
            pass

class TerminalHandler(logging.StreamHandler):
    "Handler object to send Low Priority messages via Telegram"

    def __init__(self):
        super().__init__()
        self.setLevel(logging.DEBUG)
        self.setFormatter(TerminalFormatter())
