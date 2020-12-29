from dataclasses import dataclass, field
from ..models import Owner
from ..models import Client
from .data_models import WebhookData
from .helpers import GlobalHelper
from .helpers import DefineQuantityHelper
from .helpers import AddressInfoHelper
from .helpers import ConfirmPurchaseHelper
from .loading_functions import load_owner_from
from .loading_functions import parse_webhook_data
from .loading_functions import load_or_create_client


@dataclass
class Bot:
    client: Client = field(init=False)
    owner: Owner = field(init=False)
    parsed_data: WebhookData = field(init=False)

    def __post_init__(self):
        self.helper_classes_mapping = {
            'global': GlobalHelper,
            'define_quantity': DefineQuantityHelper,
            'address_info': AddressInfoHelper,
            'confirm_purchase': ConfirmPurchaseHelper
        }

    def parse_webhook_data(self, data: dict):
        self.parsed_data = parse_webhook_data(data)

    def load_owner_from(self, token: str):
        self.owner = load_owner_from(token)

    def load_or_create_client(self):
        self.client = load_or_create_client(self.parsed_data, self.owner)

    def respond(self) -> None:

        HelperClass = self.helper_classes_mapping[self.client.stage]

        helper = HelperClass(
            client=self.client,
            owner=self.owner,
            parsed_data=self.parsed_data
        )

        helper.respond()
