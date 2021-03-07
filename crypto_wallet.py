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

    def get_client(self, key, secret):
        attempts = 0
        while True:
            attempts += 1
            try:
                client = Client(key, secret)
            except Exception as err: # pylint: disable=broad-except
                if attempts > 10:
                    msg = f"Cannot connect to client (key={key[:8]}): {err}. Retrying ..."
                    self.__log.warning(msg)
                time.sleep(5) # Sleep for 5 seconds and try again
            else:
                # Leave loop if we initialized client without errors
                break
        return client

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
        # Save portfolio value every 3 hours
        limit_mn = cfg.get("save_every_minutes", 20)

        json_data = read_json(PORTFOLIO_HIST_PATH)
        if not json_data:
            self.__log.info("Could not open portfolio json !")
            return

        if "time" in json_data[-1]:
            last_save = datetime.strptime(json_data[-1]["time"], MY_DATE_STYLE)

            delta = datetime.now() - last_save
            if delta < timedelta(minutes=limit_mn):
                return

        wallet_by_account = {}
        tickers = None
        total_portfolio = 0
        btcusdt_price = -1

        for account_name, api in ACCOUNTS.items():
            client = self.get_client(api["key"], api["secret"])
            market = api["market"]

            # Spot
            if market == "spot":
                spot_api = Spot_Api(client)
                spot_account = spot_api.get_account()
                tickers = spot_api.get_all_tickers() if not tickers else tickers
                _, spot_usdt_balances = totals(spot_account, tickers)
                total_account = sum(spot_usdt_balances.values())

            # Futures
            elif market == "futures":
                futures_account = futures_api_v2.get_account(client)
                if futures_account:
                    total_account = float(futures_account['totalMarginBalance'])
                else:
                    total_account = 0

            if btcusdt_price == -1:
                tickers = spot_api.get_all_tickers()
                btcusdt_price = spot_api.get_price("BTCUSDT")

            total_account_btc = total_account / btcusdt_price

            # Wallet Total for this Account
            wallet_by_account[account_name] = f"{total_account:.0f} USDT = {total_account_btc:.5f} BTC"
            total_portfolio += total_account

        new_dict = {
            "Total": f"{total_portfolio:.0f} USDT = {total_portfolio/btcusdt_price:.5f} BTC",
            "BTC/USDT":  f"{btcusdt_price:.0f} USDT",
            "time": pretty_datetime_now(),
            "details": wallet_by_account,
        }

        json_data.append(new_dict)
        file_ = open(str(PORTFOLIO_HIST_PATH), "w")
        file_.write(json.dumps(json_data))
        file_.close()

        # "Sexy" print for Telegram logger:
        msg = f""
        for key, val in new_dict.items():
            if val == "details":
                val_1 = "\n"
                for key_, val_ in val.items():
                    val_1 = f"{key_}: {val_}"
            else:
                val_1 = val
            msg += f"{key}: {val_1}\n"
        self.__log.info(msg)

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
