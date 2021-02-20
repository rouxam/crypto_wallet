import json
import os
from binance.client import Client as binance_client
from datetime import datetime

from constants import *
from util.spot_api import Spot_Api
from util import futures_api_v2
from util.read_json import read_json
from util.pretty_now import pretty_datetime_now, MY_DATE_STYLE


def _get_price(tickers, symbol):
    for ticker in tickers:
        if ticker["symbol"] == symbol:
            return float(ticker["price"])
    return None

def get_last_tick():
    "Get time of the last tick of Napcopy."
    return read_json(LAST_TICK_PATH)["last_tick"]

def get_futures_positions():
    "Get positions details on `account`."
    ret = ""
    for account_name, api in ACCOUNTS.items():
        key = api["key"]
        secret = api["secret"]
        client = binance_client(key, secret)
        if futures_api.get_account(client):
            positions = futures_api.positions(client)
            acc = futures_api.get_account(client)
            usdt_pos = next(a for a in acc["assets"] if a["asset"] == "USDT")
            ret += "*************\n" + \
                f"Futures positions on {account_name} (USDT Available: " + \
                f" {format(float(usdt_pos['availableBalance']), '.2f')})\n" + \
                f"*************\n"
            for pos in positions:
                    ret += f"{pos['positionAmt']} {pos['symbol']} " + \
                    f"{pos['leverage']}x - " + \
                    f"Entry Price {format(float(pos['entryPrice']), '.2f')} - " + \
                    f"Mark Price {format(float(pos['markPrice']), '.2f')} - " + \
                    f"Liq. Price {format(float(pos['liquidationPrice']), '.2f')} - " + \
                    f"PNL {format(float(pos['unRealizedProfit']), '.2f')} [USDT]\n"
    return ret

def totals(account, tickers):
    "Get spot quantites and USDT balances dict from spot account."
    if not account:
        return ({}, {})

    # Price Tickers
    btcusdt_price = _get_price(tickers, "BTCUSDT")

    spot_quantities = {}
    spot_usdt_balances = {}

    spot_balances = account["balances"]
    for bal in spot_balances:
        asset = bal["asset"]
        qty = float(bal["free"]) + float(bal["locked"])
        if qty > 0.0:
            spot_quantities[asset] = qty
            if spot_quantities[asset] > 0.0:
                if asset == "USDT":
                    spot_usdt_balances[asset] = qty
                else:
                    # Determine USDT value
                    price = _get_price(tickers, asset + "USDT")
                    if price:
                        spot_usdt_balances[asset] = qty * price
                    else:
                        btc_price = _get_price(tickers, symbol=asset + "BTC")
                        if btc_price:
                            spot_usdt_balances[asset] = qty * btc_price * btcusdt_price
                        else:
                            # Ignore base asset if no symbol with BTC nor USDT as quote asset
                            spot_usdt_balances[asset] = 0.0

    return (spot_quantities, spot_usdt_balances)

def get_wallet():
    "Get wallets details."

    total_portfolio = 0
    tickers = None
    ret = ""
    for account_name, api in ACCOUNTS.items():
        key = api["key"]
        secret = api["secret"]
        client = binance_client(key, secret)


        # Spot
        spot_api = Spot_Api(client)
        spot_account = spot_api.get_account()
        tickers = spot_api.get_all_tickers() if not tickers else tickers
        spot_qty, spot_usdt_balances = totals(spot_account, tickers)
        total_spot_balance = sum(spot_usdt_balances.values())
        total_portfolio += total_spot_balance

        # Futures
        futures_account = futures_api.get_account(client)
        if futures_account:
            total_portfolio += float(futures_account['totalMarginBalance'])

        ret += f"*** Account {account_name} ***\n"
        ret += f"Spot Wallet: {format(total_spot_balance, '.2f')} USDT\n"
        for asset, qty in spot_qty.items():
            ret += f"> {format(qty, '.4f').rjust(14, ' ')} {asset.rjust(5, ' ')} = {format(spot_usdt_balances[asset], '.2f').rjust(8, ' ')} USDT\n"
        if futures_account:
            ret += f"Futures Wallet: {format(float(futures_account['totalMarginBalance']), '.2f')} USDT\n"
            ret += f"> Incl. Unrealized PNL: {format(float(futures_account['totalUnrealizedProfit']), '.2f')} USDT\n"
        else:
            ret += f"No Futures Wallet\n"

    ret += f"********************************\n"
    ret += f"Total Portfolio:\n"
    ret += f"{format(total_portfolio, '.2f')} USDT\n"
    ret += f"********************************\n"
    return ret

def get_config():
    return read_json(CFG_PATH)

def set_config(new_cfg):
    if not isinstance(new_cfg, dict):
        return
    with open(CFG_PATH, 'w') as cfg_file:
        json.dump(new_cfg, cfg_file)

def get_portfolio_plot(market="all", account="all"):
    """
    market must be "all", "spot" or "futures"
    account must be "all", or an account name from ACCOUNTS.keys()
    """

    assert market in ("all", "spot", "futures")
    assert account in ("all", *ACCOUNTS.keys())

    d = pretty_datetime_now().replace(' ', '_').replace('/', '').replace(':', '')
    image_path = Path(f"plots/{market}_{account}_{d}.png")

    if not image_path.parent.exists():
        image_path.parent.mkdir(parents=True, exist_ok=True)

    # Data for plotting
    portfolio_list = read_json(PORTFOLIO_HIST_PATH)

    # Sort out the data we want
    # TODO (mr) using df would be useful here
    y = []
    for snapshot in portfolio_list:
        total = 0
        total_by_account = snapshot["total_by_account"]
        if account == "all":
            for account_wallet in total_by_account.values():
                for mar, value in account_wallet.items():
                    if mar == market or market == "all":
                        total += float(value)
        else:
            for acc in total_by_account.keys():
                if acc == account:
                    for mar, value in total_by_account[account].items():
                        if mar == market or market == "all":
                            total += float(value)
        y.append(total)


    dates = [x["time"] for x in portfolio_list]
    x = [datetime.strptime(d, MY_DATE_STYLE).date() for d in dates]
    title = f"Portfolio History (Market: {market.upper()}, " +\
            f"Account:{account.upper()})"

    # Generate Image and set-up axis

    # X-axis setup
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter(('%d/%m %H:%M')))
    plt.gca().xaxis.set_major_locator(mdates.HourLocator(byhour=(0, 12)))

    # Y-axis setup
    formatter = mtick.StrMethodFormatter("${x:,.0f}")
    plt.gca().yaxis.set_major_formatter(formatter)

    # Show the grid lines as dark grey dotted lines
    plt.grid(b=True, which='major', color='#666666', linestyle='dotted')
    plt.title(title)

    plt.plot(x, y)
    plt.gcf().autofmt_xdate()
    plt.savefig(image_path)
    plt.clf()

    return image_path
