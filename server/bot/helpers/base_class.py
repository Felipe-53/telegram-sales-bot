from dataclasses import dataclass
from ...models import Client, Owner, Cart
from ..data_models import WebhookData
from ...URLs import TELEGRAM_BASE_URL
from ..utils import format_price
from ..utils import format_product_order
import requests
from typing import Union, Optional
import re


@dataclass
class BaseHelper:
    client: Client
    owner: Owner
    parsed_data: WebhookData
    mapping: Optional[dict] = None

    def send_message(self, message: str) -> bool:
        """returns True on success, False otherwise"""
        response = requests.post(
            TELEGRAM_BASE_URL + self.owner.token + '/sendMessage',
            json={
                'chat_id': self.client.chat_id,
                'text': message
            }
        )

        if response.json()['ok']:
            return True

        return False

    def respond_to_unknown_input(self):
        self.send_message(
            'Sorry, I couldn\'t understand what you said'
        )

    def get_cart(self) -> Union[Cart, None]:
        non_empty_cart = True  # initial assumption

        try:
            cart = self.client.cart[0]

            if len(cart.products) == 0:
                non_empty_cart = False
        except IndexError:
            non_empty_cart = False

        if non_empty_cart:
            return cart

        return None

    def show_cart(self):
        cart = self.get_cart()

        if cart:
            message = (
                'Here\'s what your cart looks like: \n\n'
            )

            for product_order in cart.products:
                message = message + format_product_order(product_order) + '\n'

            message = message + (
                '\n' + f'TOTAL: {format_price(cart.total_price)}'
            )

        else:
            message = (
                'Looks like your cart is empty 😕'
            )

        self.send_message(message)

    def match_and_respond(self):
        for regexp in self.mapping:
            result = re.search(regexp, self.parsed_data.incoming_message_text)
            if result:
                mapped_function = self.mapping[regexp]
                mapped_function()
