from dataclasses import dataclass
from .base_class import BaseHelper
import requests
from ...URLs import TELEGRAM_BASE_URL
from ..utils import format_product_from_database
from ..utils import format_purchase
from .. import database_actions


@dataclass
class GlobalHelper(BaseHelper):
    def __post_init__(self):
        self.mapping = {
            r'/start\b|\bhi\b|\bhello\b|\bhey\b': self.greet_client,
            r'/cart': self.show_cart,
            r'/checkout': self.checkout,
            r'/clean_cart': self.clean_cart,
            r'/products': self.send_products,
            r'/bye': self.bye,
            r'\bthis\b': self.select_product,
            r'/purchases': self.show_purchases
        }

    def greet_client(self):
        message = (
            f'Hello, {self.parsed_data.first_name}! '
            'We are glad to see you here. \n'
            'To check our products, just type in /products!'
        )

        self.send_message(message)

    def bye(self):
        message = (
            f'Bye, bye, {self.parsed_data.first_name}, '
            'We hope to see you soon.'
        )

        self.send_message(message)

    def send_products(self):
        message = (
            'Great, here are our products. To select one, '
            'just reply to the message that it\'s in saying: "this"'
        )

        self.send_message(message)

        for product in self.owner.products:
            requests.post(
                TELEGRAM_BASE_URL + self.owner.token + '/sendPhoto',

                data={
                    'chat_id': self.client.chat_id,
                    'caption': format_product_from_database(product)
                },

                files={
                    'photo': product.picture,
                }
            )

    def select_product(self):
        product = database_actions\
            .get_referenced_product(self.parsed_data)

        success = database_actions\
            .add_product_to_client_cart(product, self.client)

        if success:
            database_actions\
                .update_client_stage(self.client, 'define_quantity')

            message = (
                'Nice choice, now tell me: '
                'how many of those would you like '
                'to purchase? You can awnser with a simple number. '
                'If you\'d like to cancel, just say "cancel"'
            )
        else:
            message = (
                'Looks like you already have '
                'that item in your cart. Type '
                '/cart to see if that\'s the case.'
            )

        self.send_message(message)

    def clean_cart(self):
        cart = self.get_cart()
        database_actions\
            .clean_cart(cart)

        message = 'Your cart is clean'
        self.send_message(message)

    def checkout(self):
        cart = self.get_cart()

        if not cart:
            message = (
                'Looks like you cart is empty'
            )
            self.send_message(message)

        elif len(self.client.addresses) == 0:
            message = (
                'Right. You haven\'t got any adressess information '
                'in our systems. The good news is you only have to '
                'do this once. Please send us your fixed location and '
                'we will work your address from there!'
            )

            database_actions\
                .update_client_stage(self.client, 'address_info')

            self.send_message(message)

        else:
            message = (
                'Aewsome! Check the products in your '
                'cart below. If you are happy with '
                'it, just say "finish" and we will be '
                'done with it'
            )
            self.send_message(message)

            self.show_cart()

            database_actions\
                .update_client_stage(self.client, 'confirm_purchase')

    def show_purchases(self):
        purchases = database_actions\
            .get_client_purchases(self.client)

        if not purchases:
            message = 'You don\'t have purchases yet'
            self.send_message(message)
        else:
            self.send_message('Here are your purchases:\n')
            for purchase in purchases:
                formatted_purchase = format_purchase(purchase)
                self.send_message(formatted_purchase)

    def respond(self):
        self.match_and_respond()
