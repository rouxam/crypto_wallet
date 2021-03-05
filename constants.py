import sys
import os
from pathlib import Path

# Environment variables
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
TELEGRAM_CRYPTO_WALLET_TOKEN = os.getenv("TELEGRAM_CRYPTO_WALLET_TOKEN")

ACCOUNTS = {
    "MASTER": {
        "key": os.getenv("MASTER_KEY"),
        "secret": os.getenv("MASTER_SECRET")
    },
    "3c MASTER": {
        "key": os.getenv("MASTER_3C_KEY"),
        "secret": os.getenv("MASTER_3C_SECRET")
    },
    "3c BTC ETH HODL": {
        "key": os.getenv("BTC_3C_KEY"),
        "secret": os.getenv("BTC_3C_SECRET")
    },
    "3c ALT HODL": {
        "key": os.getenv("ETH_3C_KEY"),
        "secret": os.getenv("ETH_3C_SECRET")
    },
    "3c LEVERAGE": {
        "key": os.getenv("BLVT_3C_KEY"),
        "secret": os.getenv("BLVT_3C_SECRET")
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
