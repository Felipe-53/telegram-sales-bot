from flask import Blueprint, request
import requests
from ..URLs import TELEGRAM_BASE_URL, WEBHOOK_BASE_URL

bp = Blueprint('platform', __name__)


@bp.route('/register_bot', methods=['POST'])
def register():
    data = request.get_json()
    token = data['token']
    success = set_user_webhook(token)

    return {
        'ok': success
    }


def set_user_webhook(token):

    USER_WEBHOOK_URL = WEBHOOK_BASE_URL + token
    USER_TELEGRAM_URL = TELEGRAM_BASE_URL + token

    response = requests.get(USER_TELEGRAM_URL + '/getWebhookInfo')
    assert response.ok is True

    json_response = response.json()

    if json_response['result']['url'] != USER_WEBHOOK_URL:
        response = requests.post(USER_TELEGRAM_URL + '/setWebhook', json={
            'url': USER_WEBHOOK_URL
        })

        if response.json()['ok'] is True:
            return True

        return False

    return True
