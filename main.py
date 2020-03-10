import pickle
from enum import Enum
from paisa_core.client import FivePaisaClient
from paisa_core.base import EnumDirectValueMeta
import os.path
from paisa_core.config import OrderFor, Exchange, ExchangeSegment, OrderType, \
    OrderValidity
import pprint

class Settings(Enum, metaclass=EnumDirectValueMeta):
    APP_NAME = os.environ.get('APP_NAME')
    APP_SOURCE = int(os.environ.get('APP_SOURCE'))
    USER_ID = os.environ.get('USER_ID')
    PASSWORD = os.environ.get('PASSWORD')
    USER_KEY = os.environ.get('USER_KEY')
    ENCRYPTION_KEY = os.environ.get('ENCRYPTION_KEY')


if __name__ == "__main__":

    pickle_name = "request_instance.pkl"
    if os.path.exists(pickle_name):
        print("loading object from pickle file {}".format(pickle_name))
        pickle_object = open(pickle_name, 'rb')
        client_5 = pickle.load(pickle_object)
    else:
        client_5 = FivePaisaClient(Settings)
        username = os.environ.get('USERNAME')
        password = os.environ.get('USER_PASSWORD')
        birthdate= os.environ.get('USER_BIRTHDATE')
        response = client_5.authenticate(username, password, birthdate)
        response = client_5.authenticate(username, password, birthdate)
        print(response)
        with open(pickle_name, 'wb') as output:
            pickle.dump(client_5, output)
    price = 34.83
    quantity = 2
    script_code = 522
    response = client_5.get_user_info("user_holdings")
    pprint.pprint(response)
    response = client_5.place_modify_cancel_order(order_for=OrderFor.PLACE,
                                                  exchange=Exchange.NSE,
                                                  exchange_type=ExchangeSegment.CASH,
                                                  price=price,
                                                  order_id=0,
                                                  order_type=OrderType.BUY,
                                                  quantity=quantity,
                                                  script_code=script_code,
                                                  at_market=False,
                                                  order_validity=OrderValidity.GTD,
                                                  after_market="Y")
    # pprint.pprint(response)
