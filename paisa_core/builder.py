
import socket
import requests
import netifaces as nif


def build_head(settings):
    return {
            "appName": settings.APP_NAME.value,
            "appVer": "1.0",
            "key": settings.USER_KEY.value,
            "osName": "WEB",
            "requestCode": None,
            "userId": settings.USER_ID.value,
            "password": settings.PASSWORD.value
    }


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
            "Password":  password,
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