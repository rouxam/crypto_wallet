"python-binance Futures API wrapper."

import logging
from binance.client import Client

Log = logging.getLogger("napcopy")

def positions(client):
    "Get all opened positions on Futures account from `client`."
    ret = []
    assert isinstance(client, Client)
    try:
        pos_info = client.futures_coin_position_information()
    except Exception as err: # pylint: disable=broad-except
        err_msg = f"`futures_position_information()` failed: {err}"
        Log.warning(err_msg)
        return None

    # Get only opened positions
    for pos in pos_info:
        if float(pos["positionAmt"]) != 0.0:
            ret.append(pos)
    return ret

def create_order(client, **order):
    "Create order on Futures account from `client`."
    assert isinstance(client, Client)
    try:
        _ = client.futures_coin_create_order(**order)
    except Exception as err: # pylint: disable=broad-except
        err_msg = f"`futures_create_order()` failed: {err}"
        Log.warning(err_msg)

def get_account(client):
    "Create order on Futures account from `client`."
    assert isinstance(client, Client)
    try:
        return client.futures_coin_account()
    except Exception as err: # pylint: disable=broad-except
        if "code=-2015" in str(err):
            # No futures account
            pass
        else:
            err_msg = f"`get_account()` failed: {err}"
            Log.warning(err_msg)
        return None
