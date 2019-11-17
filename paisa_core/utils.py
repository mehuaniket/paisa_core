import base64
import uuid


# get a UUID - URL safe, Base64
def get_a_uuid():
    r_uuid = base64.urlsafe_b64encode(uuid.uuid4().bytes).decode()
    return r_uuid.replace('=', '')
