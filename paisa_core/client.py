import json

import requests

from paisa_core import utils
from paisa_core.aes_ciper import AESCipher
from paisa_core.builder import build_head, build_login_body, build_get_margin_body, build_placer_modify_order_body
from paisa_core.config import default_headers, BASE_CONFIG, OrderFor, Exchange, ExchangeSegment, OrderType, \
    OrderValidity


def get_request_session():
    request_session = requests.Session()
    request_session.headers.update(default_headers)
    return request_session


class FivePaisaClient:
    """
    This would be the main library class. All communication will happen from here other than utility functions and other
    helper class will be accessible.

    This class expected to work as proxy so that other people can understand the code easily, it will also make it easy
    to use.

    """

    def __init__(self, settings):
        """
        settings object will be dictionary object containing.
        APP_NAME, APP_SOURCE, USER_ID, PASSWORD, USER_KEY, ENCRYPTION_KEY

        Other variables passed with setting will work as speed control paddle.
        :param settings:
        """
        self.settings = settings
        self.head = build_head(self.settings)
        self.cryptic = AESCipher(self.settings.ENCRYPTION_KEY)
        self.request_session = get_request_session()

        self.auth = {
            "cookie": ''
        }
        self.profile = None
        self.client_code = None
        self.incremental_order_id = 0
        self.is_logged = False
        self.last_remote_order_ID = None
        self.last_traded_qty = None

    def authenticate(self, username, password, pin):
        username = self.cryptic.encrypt(username)
        password = self.cryptic.encrypt(password)
        pin = self.cryptic.encrypt(pin)
        endpoint_detail = BASE_CONFIG["api"]["user_login"]

        body = build_login_body(self.head, endpoint_detail["request_code"],
                                username, password, pin)
        print(body)
        response = self.request_session.post(endpoint_detail["url"], data=json.dumps(body))

        self.profile = json.loads(response.content)["body"]
        self.client_code = self.profile["ClientCode"]
        self.is_logged = True
        return self.profile

    def get_user_info(self, key):
        endpoint_detail = BASE_CONFIG["api"][key]
        body = build_get_margin_body(self.head, endpoint_detail["request_code"], self.client_code)
        response = self.request_session.post(endpoint_detail["url"], data=json.dumps(body))
        margin = json.loads(response.content)["body"]
        return margin

    def place_modify_order(self,
                           order_for,
                           exchange,
                           exchange_type,
                           price,
                           order_id,
                           order_type,
                           quantity,
                           script_code,
                           at_market,
                           order_validity,
                           after_market):
        endpoint_detail = BASE_CONFIG["api"]["order_request"]

        # Generate UUID for tracking
        uuid = utils.get_a_uuid()
        body = build_placer_modify_order_body(self.head,
                                              endpoint_detail["request_code"],
                                              self.client_code,
                                              app_code=self.settings.APP_SOURCE,
                                              order_for=order_for,
                                              exchange=exchange,
                                              exchange_type=exchange_type,
                                              price=price,
                                              order_id=order_id,
                                              order_type=order_type,
                                              quantity=quantity,
                                              script_code=script_code,
                                              at_market=at_market,
                                              remote_order_id=uuid,
                                              order_validity=order_validity,
                                              after_market=after_market
                                              )
        print(body)
        response = self.request_session.post(endpoint_detail["url"], data=json.dumps(body))
        placed_order = json.loads(response.content)["body"]
        return placed_order
