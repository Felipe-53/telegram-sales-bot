from ..models import Owner
from ..models import Client
from .data_models import WebhookData
from .database_actions import create_client
from werkzeug.exceptions import InternalServerError


def parse_webhook_data(data: dict) -> WebhookData:

    try:
        message = data['message']
    except KeyError:
        message = data['edited_message']

    parsed_data = WebhookData(
        telegram_user_id=message['from']['id'],
        chat_id=message['chat']['id'],
        first_name=message['from']['first_name'],
    )

    try:
        parsed_data.last_name = message['from']['last_name']
    except KeyError:
        pass

    try:
        parsed_data.reply_to_message = message['reply_to_message']
    except KeyError:
        pass

    try:
        parsed_data.incoming_message_text = message['text'].lower()
    except KeyError:
        pass

    try:
        parsed_data.location = [
            message['location']['latitude'],
            message['location']['longitude']
        ]
    except KeyError:
        pass

    return parsed_data


def load_owner_from(token: str) -> Owner:
    owner = Owner.query.filter_by(token=token).first()
    if owner is None:
        raise InternalServerError

    return owner


def load_or_create_client(parsed_data: WebhookData, owner: Owner) -> Client:
    telegram_user_id = parsed_data.telegram_user_id
    client = Client.query\
        .filter_by(telegram_user_id=telegram_user_id).first()

    if not client:
        client = create_client(parsed_data, owner)

    return client
