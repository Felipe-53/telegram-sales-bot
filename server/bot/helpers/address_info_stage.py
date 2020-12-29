from dataclasses import dataclass
from .base_class import BaseHelper
import requests
from .. import database_actions
from ...URLs import build_geocoding_api_url
from ..utils import address_model_instance_from_api_response
from ..utils import format_address


@dataclass
class AddressInfoHelper(BaseHelper):
    def __post_init__(self):
        self.mapping = {
            r'confirm': self.confirm_address,
        }

    def update_address_info(self):
        if not self.parsed_data.location:
            message = (
                'You must send your location so we '
                'can work your address from there'
            )

            self.send_message(message)
        else:
            # send request and get response
            url = build_geocoding_api_url(self.parsed_data.location)
            response = requests.get(url)

            address = address_model_instance_from_api_response(
                response
            )

            # add to db
            database_actions\
                .add_address_to_client(address, self.client)

            message = (
                'Here\'s what we could deduce from your location: \n\n'
                f'{format_address(address)}' + '\n'
                '\n Say "confirm" to confirm.'
            )

            self.send_message(message)

    def confirm_address(self):
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

    def respond(self):
        if self.parsed_data.incoming_message_text:
            self.match_and_respond()
        else:
            self.update_address_info()
