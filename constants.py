import sys
import os
from pathlib import Path

# Environment variables
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
TELEGRAM_CRYPTO_WALLET_TOKEN = os.getenv("TELEGRAM_CRYPTO_WALLET_TOKEN")

ACCOUNTS = {
    "MASTER": {
        "key": os.getenv("MASTER_KEY"),
        "secret": os.getenv("MASTER_SECRET"),
        "market":"spot"
    },
    "USDT DCA bots": {
        "key": os.getenv("MASTER_3C_KEY"),
        "secret": os.getenv("MASTER_3C_SECRET"),
        "market": "spot"
    },
    "BTC DCA bots": {
        "key": os.getenv("BTC_DCA_3C_KEY"),
        "secret": os.getenv("BTC_DCA_3C_SECRET"),
        "market": "spot"
    },
    "Futures": {
        "key": os.getenv("MASTER_3C_KEY"),
        "secret": os.getenv("MASTER_3C_SECRET"),
        "market": "futures"
    },
    "BTC ETH HODL": {
        "key": os.getenv("BTC_3C_KEY"),
        "secret": os.getenv("BTC_3C_SECRET"),
        "market": "spot"
    },
    "Altcoins HODL": {
        "key": os.getenv("ETH_3C_KEY"),
        "secret": os.getenv("ETH_3C_SECRET"),
        "market": "spot"
    },
    "Leveraged tokens": {
        "key": os.getenv("BLVT_3C_KEY"),
        "secret": os.getenv("BLVT_3C_SECRET"),
        "market": "spot"
    }
}


# Paths setup
if 'win' in sys.platform:
    ROOT = Path(__file__).parent
else:
    ROOT = "/usr/bin/crypto_wallet"

CFG_PATH = ROOT / Path("cfg.json")
LAST_TICK_PATH = ROOT / Path("last_tick.json")
PORTFOLIO_HIST_PATH = ROOT / Path("portfolio_history.json")
