from ..models import Owner, Client, Cart, ProductOrder
from ..models import Product, ClientAddress, Purchase
from .data_models import WebhookData, Address
from .. import db
import re


def create_client(parsed_data: WebhookData, owner: Owner):
    client = Client(
        owner=owner,
        chat_id=parsed_data.chat_id,
        name=parsed_data.first_name,
        telegram_user_id=parsed_data.telegram_user_id,
        stage='global'
    )

    db.session.add(client)
    db.session.commit()

    return client


def update_client_stage(client: Client, stage: str) -> None:
    client.stage = stage
    db.session.commit()


def add_product_to_client_cart(product: Product, client: Client) -> bool:

    cart_list = client.cart

    if len(cart_list) == 0:
        cart = Cart(client=client)
        db.session.add(cart)
        db.session.commit()
    elif len(cart_list) == 1:
        cart = cart_list[0]
    else:
        raise Exception('client has more than one cart')

    for cart_order in cart.products:
        if cart_order.product.pk == product.pk:
            return False

    new_product_order = ProductOrder(
        belongs_to='cart',
        cart=cart,
        product=product
    )

    db.session.add(new_product_order)
    db.session.commit()

    return True


def get_referenced_product(parsed_data: WebhookData):
    reply_to_message = parsed_data.reply_to_message
    telegram_user_id = parsed_data.telegram_user_id
    caption = reply_to_message['caption']

    client = Client.query.filter_by(
        telegram_user_id=telegram_user_id
    ).first()

    owner = client.owner

    mapping = {}

    for product in owner.products:
        mapping.update({
            r'\b' + product.name + r'\b': product.name
        })

    for regexp in mapping:
        result = re.search(regexp, caption)
        if result:

            product = Product.query\
                .filter_by(name=mapping[regexp]).first()

            assert product is not None

            return product


def add_address_to_client(address: Address, client: Client):
    client_address = ClientAddress(
        client=client,
        number=address.number,
        street=address.street,
        neighborhood=address.neighborhood,
        state=address.state,
        city=address.city,
        country=address.country
    )

    db.session.add(client_address)
    db.session.commit()


def clean_cart(cart: Cart):
    if cart and len(cart.products) != 0:
        for product_order in cart.products:
            db.session.delete(product_order)

        db.session.commit()


def create_purchase_for(client: Client) -> Purchase:
    new_purchase = Purchase(
        client=client
    )

    db.session.add(new_purchase)
    db.session.commit()

    return new_purchase


def from_cart_to_purchase(cart: Cart, purchase: Purchase):
    product_order: ProductOrder
    for product_order in cart.products:
        product_order.belongs_to = 'purchase'
        product_order.cart_pk = None
        product_order.purchase_pk = purchase.pk

    db.session.commit()


def get_client_purchases(client: Client):
    purchases = Purchase.query.filter_by(client_pk=client.pk).all()
    return purchases
