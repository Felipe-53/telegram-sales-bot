from dataclasses import dataclass
from .base_class import BaseHelper
from .. import database_actions
from ... import db
import re


@dataclass
class DefineQuantityHelper(BaseHelper):
    def __post_init__(self):
        self.mapping = {
            r'\b\d+\b': self.update_product_order_quantity,
            r'cancel': self.giveup_product
        }

    def update_product_order_quantity(self):

        user_input = self.parsed_data.incoming_message_text
        result = re.search(r'\d+', user_input)
        quantity = result.group()

        cart = self.get_cart()
        for product_order in cart.products:
            if product_order.quantity is None:
                product_order.quantity = int(quantity)
                db.session.commit()
                break

        message = (
            'Excellent. You can say /cart '
            'to check what\'s in your cart or say '
            '/checkout to proceed for paying'
            'To keep buying you can say reply "this" '
            'like before'
        )

        database_actions\
            .update_client_stage(self.client, 'global')

        self.send_message(message)

    def giveup_product(self):
        cart = self.client.cart[0]

        for product_order in cart.products:
            if product_order.quantity is None:
                db.session.delete(product_order)
                db.session.commit()
                break

        database_actions\
            .update_client_stage(self.client, 'global')

        message = (
            'Done, you can continue browsing our products '
            'and, if you like one, just reply "this" to it '
            'like before 😜'
        )
        self.send_message(message)

    def respond(self):
        for regexp in self.mapping:
            result = re.search(regexp, self.parsed_data.incoming_message_text)
            if result:
                mapped_function = self.mapping[regexp]
                mapped_function()
