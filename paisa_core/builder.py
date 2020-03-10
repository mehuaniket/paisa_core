import datetime
import socket

import netifaces as nif
import requests


def build_head(settings):
    return {
        "appName": settings.APP_NAME,
        "appVer": "1.0",
        "key": settings.USER_KEY,
        "osName": "WEB",
        "requestCode": None,
        "userId": settings.USER_ID,
        "password": settings.PASSWORD
    }


def get_current_date(days=None):
    date_now = datetime.datetime.now()
    if days:
        date_now = date_now + datetime.timedelta(days=days)
    milliseconds = int(date_now.timestamp() * 1000)

    return "/Date({})/".format(milliseconds)


def get_my_ip():
    """
    Find my IP address
    :return:
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    local_ip = s.getsockname()[0]
    s.close()
    return local_ip


def mac_for_ip(ip):
    """It will bring mac address for the local IP address passed to argument"""
    for i in nif.interfaces():
        addrs = nif.ifaddresses(i)
        try:
            if_mac = addrs[nif.AF_LINK][0]['addr']
            if_ip = addrs[nif.AF_INET][0]['addr']
        except (IndexError, KeyError):
            if_mac = if_ip = None
        if if_ip == ip:
            return if_mac
    return None


def get_public_ip():
    public_ip = requests.get("https://api.ipify.org").text
    return public_ip


def build_login_body(head, request_code, email, password, pin):
    head["requestCode"] = request_code
    local_ip = get_my_ip()
    mac_address = mac_for_ip(local_ip)
    body = {
        "head": head,
        "body": {
            "Email_id": email,
            "Password": password,
            "LocalIP": local_ip,
            "PublicIP": get_public_ip(),
            "HDSerailNumber": "C02XR4M2JG5H",
            "MACAddress": mac_address,
            "MachineID": "039377 ",
            "VersionNo": "1.7",
            "RequestNo": "1",
            "My2PIN": pin,
            "ConnectionType": "1"
        }
    }
    return body


def build_get_margin_body(head, request_code, client_code):
    head["requestCode"] = request_code
    body = {
        "head": head,
        "body": {
            "ClientCode": client_code
        }
    }
    return body


def build_placer_modify_order_body(head,
                                   request_code,
                                   client_code,
                                   app_code,
                                   order_for,
                                   exchange,
                                   exchange_type,
                                   price,
                                   order_id,
                                   order_type,
                                   quantity,
                                   script_code,
                                   at_market,
                                   remote_order_id,
                                   order_validity,
                                   valid_till_date=get_current_date(),
                                   exchange_id=0,
                                   disclosed_quantity=0,
                                   stoploss=0,
                                   is_stoploss_order=False,
                                   is_ioc_order=False,
                                   is_intraday=True,
                                   after_market="N",
                                   traded_quantity=0,
                                   trigger_price=None,
                                   squareoff=None,
                                   ):
    """Place an order.

    - `ClientCode`: Client code for whom order is being placed.
       Validation": "Cannot be empty."
       Sample Value": 12345678

    - `OrderFor`: P- Place (Fresh ), M-Modify, C- Cancel Order
       Validation": "Cannot be empty."
       Sample Value": "P\nM\nC"

    - `Exchange`: Exchange in which order has been placed. N- NSE, B- BSE, M-MCX
       Validation": "Cannot be empty."
       Sample Value": "N\nB\nM"

    - `ExchangeType`: Exchange segment. C-Cash, D-Derivative, U - Currency
       Validation": "Cannot be empty."
       Sample Value": "C\nD\nU"

    - `Price`: Rate at which client wants to Buy / Sell the stock.(Price=0 for at market order)
       Validation": "Cannot be empty."
       Sample Value": 10200

    - `OrderID`: It is an incremental number for each order after login.
       Validation": "Cannot be empty."
       Sample Value": "-"

    - `OrderType`: Client want to buy or sell the
       Validation": "Cannot be empty."
       Sample Value": "Buy\nMSell"

    - `Qty`: Total quantity client want to buy or sell (In Case Of Derivative Send Market Lot in Qty)
       Validation": "Cannot be empty."
       Sample Value": 2

    - `OrderDateTime`: Local date at which order has been placed.
       Validation": "Cannot be empty."
       Sample Value": "/Date(1522923287588)/"

    - `ScripCode`: Scrip Code of the requested order.
       Validation": "Cannot be empty."
       Sample Value": 22

    - `AtMarket`: Specifies where the order placed is at market or Limit Order. Send False for Limit Order and True for At Market Order.
       Validation": "Cannot be empty."
       Sample Value": "true\nfalse"

    - `RemoteOrderID`: This will be unique ID for each order created by you.
       Validation": "Cannot be empty."
       Sample Value": 5.712977620180405e+22

    - `ExchOrderID`: This is order reference number generated by exchange for an order. Send 0 for fresh order and for modify cancel send the exchange order id received from exchange.
       Validation": "Cannot be empty."
       Sample Value": 5

    - `DisQty`: Quantity exposed in the exchange. Disclosed quantity is never larger than order quantity.
       Validation": "Cannot be empty."
       Sample Value": 0

    - `StopLossPrice`: This will be the trigger price. This will be set when user want to place stop loss order. (For Buy Stop loss, Trigger price should not be greater than Limit Price. And for Sell Stop Loss Order Trigger Price should not be less than Limit Price)
       Validation": "Cannot be empty."
       Sample Value": "-"

    - `IsStopLossOrder`: This will indicate where client has placed stop loss order. Send True if order placed is stop loss and send False if it is regular order
       Validation": "Cannot be empty."
       Sample Value": "true\nfalse"

    - `IOCOrder`: Send False in case order is not IOC
       Validation": "Cannot be empty."
       Sample Value": "true\nfalse"

    - `IsIntraday`: For Intraday order send this flag as True and for Delivery order send it as False
       Validation": "Cannot be empty."
       Sample Value": "true\nfalse"

    - `ValidTillDate`: Order Validity Date For VTD (GTD in Case of Commodity) Order should not be today’s or earlier date. Date should be in Range of 45 days from next Day
       Validation": "Cannot be empty."
       Sample Value": "/Date(1522923270611)/"

    - `AHPlaced`: Y-in case order placed after market closed\nN-Normal Market time Order
       Validation": "Cannot be empty."
       Sample Value": "Y\nN"

    - `PublicIP`: Local IP address of the Device used by client to place an order
       Validation": "Cannot be empty."
       Sample Value": "10.0.2.15"

    - `iOrderValidity`: Enum of OrderValidity
       Validation": "Cannot be empty.",
        "Sample Value": "0 - Day\n4 - EOS\n2 - GTC\n1- GTD\n3 - IOC\n6 - FOK"

    - `TradedQty`: Pass the traded qty. For placing fresh order, value should be 0. For modification/cancellation, send the actual traded qty. Incorrect value would lead to order rejection.
       Validation": "Cannot be empty."
       Sample Value": 0

    - `OrderRequesterCode`: Clientcode of customer
       Validation": "Cannot be empty."
       Sample Value": 12345678

    - `AppSource`: App source generated at the time of registration
       Validation": "Cannot be empty."
       Sample Value": 5


    """
    params = locals()
    # print(params)
    head["requestCode"] = request_code
    body = {
        "head": head,
        "body": {
            "ClientCode": client_code,
            "OrderFor": order_for,
            "Exchange": exchange,
            "ExchangeType": exchange_type,
            "Price": price,
            "OrderID": 0,
            "OrderType": order_type,
            "Qty": quantity,
            "OrderDateTime": get_current_date(),
            "ScripCode": script_code,
            "AtMarket": at_market,
            "RemoteOrderID": remote_order_id,
            "ExchOrderID": 0,
            "DisQty": 0,
            "IsStopLossOrder": is_stoploss_order,
            "StopLossPrice": stoploss,
            "IsVTD": False,
            "IOCOrder": False,
            "IsIntraday": False,
            "PublicIP": get_public_ip(),
            "AHPlaced": after_market,
            "ValidTillDate": get_current_date(days=2),
            "iOrderValidity": order_validity,
            "TradedQty": 0,
            "OrderRequesterCode": client_code,
            "AppSource": app_code

        }
    }
    return body


