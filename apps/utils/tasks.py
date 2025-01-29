import os
import uuid
import datetime
import base64
import requests
from celery import shared_task

from apps.utils.utils import code_generator
from apps.users.models import UserResetToken


@shared_task
def send_sms(user_id, phone: str) -> object:
    url = os.getenv("SMS_URL")
    username = os.getenv("SMS_USERNAME")
    password = os.getenv("SMS_PASSWORD")
    alias = os.getenv("CgPN")
    message_id = str(uuid.uuid4())
    code = code_generator()

    data = {
        "header": {
            "login": username,
            "pwd": password,
            "CgPN": alias
        },
        "body": {
            "message_id_in": message_id,
            "CdPN": phone,
            "text": code
        }
    }
    response = requests.post(url, json=data)

    expire_seconds = int(os.environ.get('EXPIRE_SECONDS'))
    expire_date = datetime.datetime.now() + datetime.timedelta(seconds=expire_seconds)
    encoded_content = base64.b64encode(code.encode('ascii')).decode('ascii')

    UserResetToken.objects.create(user_id=user_id, message_id=message_id, content=encoded_content, expire_date=expire_date)

    return response.json()