import json
import time
import logging
import math
import socket

from datetime import datetime, timedelta
from binance.client import Client
from typing import Dict

from constants import *
from operations import totals
from util.spot_api import Spot_Api
from util import futures_api_v2
from util.read_json import read_json
from util.pretty_now import pretty_datetime_now, MY_DATE_STYLE
from logger import TelegramNormalHandler, TerminalHandler


class Monitor():
    """
    Object to monitor and replicate Napbot operations
    """

    def __init__(self, cfg):
        # Setup loggers
        self.__log = logging.getLogger("crypto_wallet")
        self.__log.setLevel(level=logging.DEBUG)
        self.__log.addHandler(TelegramNormalHandler())
        self.__log.addHandler(TerminalHandler())

        self.__last_timestamp = datetime.now()

        hostname = socket.gethostname()
        self.__log.info("Initializing on %s with cfg: %s", hostname, str(cfg))
        self.__log.info("Succesfully initialized on %s", hostname)

    def save_last_tick(self, cfg):

        limit_seconds = 10 * float(cfg.get("sleep_time"))

        d = read_json(LAST_TICK_PATH)

        # Monitor how long I was sleeping
        last_tick = datetime.strptime(
            d.get("last_tick", pretty_datetime_now()),
            MY_DATE_STYLE)

        delta = datetime.now() - last_tick
        if delta > timedelta(seconds=limit_seconds):
            msg = f"Program was dead for {delta.seconds}s"
            self.__log.warning(msg)

        tick_file = open(str(LAST_TICK_PATH), "w")
        tick_file.write(json.dumps({"last_tick": pretty_datetime_now()}))
        tick_file.close()

    def save_portfolio(self, cfg):
        "Save portfolio value in JSON every now and then."
        print("saving portfolio")
        # Save portfolio value every 3 hours
        limit_hours = cfg.get("save_every_hours", 6)

        json_data = read_json(PORTFOLIO_HIST_PATH)
        if not json_data:
            print("no data")
            return

        if "time" in json_data[-1]:
            last_save = datetime.strptime(json_data[-1]["time"], MY_DATE_STYLE)

            delta = datetime.now() - last_save
            if delta < timedelta(hours=limit_hours):
                return

        print("saving portfolio beta")
        wallet_by_account = {}
        tickers = None
        total_portfolio = 0
        for account_name, api in ACCOUNTS.items():
            print("saving portfolio charly")
            key = api["key"]
            secret = api["secret"]
            client = Client(key, secret)

            # Spot
            spot_api = Spot_Api(client)
            spot_account = spot_api.get_account()
            tickers = spot_api.get_all_tickers() if not tickers else tickers
            _, spot_usdt_balances = totals(spot_account, tickers)
            total_spot = sum(spot_usdt_balances.values())

            # Futures
            futures_account = futures_api_v2.get_account(client)
            if futures_account:
                total_futures = float(futures_account['totalMarginBalance'])
            else:
                total_futures = 0

            # Wallet Total for this Account
            wallet_by_account[account_name] = {
                "spot": format(total_spot, '.2f'),
                "futures": format(total_futures, '.2f')
            }

            total_portfolio += total_spot + total_futures

        new_dict = {
            "time": pretty_datetime_now(),
            "total_by_account": wallet_by_account,
            "total": total_portfolio
        }

        json_data.append(new_dict)
        file_ = open(str(PORTFOLIO_HIST_PATH), "w")
        file_.write(json.dumps(json_data))
        file_.close()

def main():
    "Run the bot."

    cfg = read_json(CFG_PATH)
    monitor = Monitor(cfg)

    while True:
        cfg = read_json(CFG_PATH) # re-read everytime

        monitor.save_last_tick(cfg)
        monitor.save_portfolio(cfg)

        time.sleep(float(cfg.get("sleep_time")))

if __name__ == "__main__":
    main()
