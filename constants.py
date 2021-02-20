import sys
import os
from pathlib import Path

# Environment variables
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
TELEGRAM_CRYPTO_WALLET_TOKEN = os.getenv("TELEGRAM_CRYPTO_WALLET_TOKEN")

ACCOUNTS = {
    # "3c_master": {
    #     "key": os.getenv("BINANCE_ALTPUMP_KEY"),
    #     "secret": os.getenv("BINANCE_ALTPUMP_SECRET")
    # },
    # "3c_btc": {
    #     "key": os.getenv("BINANCE_3C_KEY"),
    #     "secret": os.getenv("BINANCE_3C_SECRET")
    # },
    # "3c_eth": {
    #     "key": os.getenv("BINANCE_MAIN_KEY"),
    #     "secret": os.getenv("BINANCE_MAIN_SECRET")
    # }
    "3c_master": {
        "key": "RaqHY2dYKXrkuGDD2AqXOad4IC0w5E9tXAcLrBNMLgGoTs93d803Wzgd60se8ypm",
        "secret": "j3rYCf0FzJHj1D1vhHfLC8CAO2hR4qoTuYCfTAbyQSLbATeak8LUejVRSi9Ks7Ct" 
    },
    "3c_btc": {
        "key": "5WHPpBe3TVFvSTyZtH8Urdjbuk4uckl7Y6WKYj1MlhVB3CRsQA7mhm2OXVn9pDGm",
        "secret": "g6ez76JW3XNNFqervHA3XbrpbI0wVlaLKjE9J2Zdhc3VXsIG4jSSIXkRpDcjN3uH"
    },
    "3c_eth": {
        "key": "aZwIUzGtWZxEyQzlk5LiyxXQe67UXUa0ZwYiFBfhiUcyyAflQhoDw2YFs3hfMRrJ",
        "secret": "o5BIayXBunsLzCEmY4a7Qq8C7WHycqiDPcNHSHdrroxH4lL6HM3faG4kNoS0N6bs"
    }
}


# Paths setup
if 'win' in sys.platform:
    ROOT = Path(__file__).parent
else:
    ROOT = "/usr/bin/wallet_monitor"

CFG_PATH = ROOT / Path("cfg.json")
LAST_TICK_PATH = ROOT / Path("last_tick.json")
PORTFOLIO_HIST_PATH = ROOT / Path("portfolio_history.json")
