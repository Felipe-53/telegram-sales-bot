from flask import Blueprint, request
from .bot.bot import Bot

bp = Blueprint('webhook', __name__)


@bp.route('/webhook<token>', methods=['POST'])
def index(token):

    bot = Bot()

    data = request.get_json()
    print(f'\n{data}\n')

    # load data
    bot.parse_webhook_data(data)
    bot.load_owner_from(token)
    bot.load_or_create_client()

    bot.respond()

    return '', 200
