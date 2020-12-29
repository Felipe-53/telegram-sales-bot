from dataclasses import dataclass
from .base_class import BaseHelper
from .. import database_actions


@dataclass
class ConfirmPurchaseHelper(BaseHelper):
    def __post_init__(self):
        self.mapping = {
            r'finish': self.finish,
        }

    def finish(self):
        purchase = database_actions\
            .create_purchase_for(self.client)

        cart = self.get_cart()

        database_actions\
            .from_cart_to_purchase(cart, purchase)

        database_actions\
            .update_client_stage(self.client, 'global')

        message = (
            'Horray, we are done. You will soon '
            'have your purchase be delivered to you '
            'Thanks and until next time!'
        )

        self.send_message(message)

    def respond(self):
        self.match_and_respond()
