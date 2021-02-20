import sys
import os
from pathlib import Path

# Environment variables
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
TELEGRAM_CRYPTO_WALLET_TOKEN = os.getenv("TELEGRAM_CRYPTO_WALLET_TOKEN")

ACCOUNTS = {
    "master": {
        "key": os.getenv("MASTER_KEY"),
        "secret": os.getenv("MASTER_SECRET")
    },
    "3c_master": {
        "key": os.getenv("3C_MASTER_KEY"),
        "secret": os.getenv("3C_MASTER_SECRET")
    },
    "3c_btc": {
        "key": os.getenv("3C_BTC_KEY"),
        "secret": os.getenv("3C_BTC_SECRET")
    },
    "3c_eth": {
        "key": os.getenv("3C_ETH_KEY"),
        "secret": os.getenv("3C_ETH_SECRET")
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
