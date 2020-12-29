from ..models import Product, Purchase
from ..models import ProductOrder
from .data_models import Address
from requests import Response
from datetime import datetime, timedelta


def format_price(price: int) -> str:
    price = str(price)

    return '$ ' + price[:-2] + '.' + price[-2:]


def format_product_from_database(product: Product) -> str:

    formated = (
        f'{product.name}\n\n'
        f'{product.description}\n'
        f'Price: {format_price(product.price)}'
    )

    return formated


def format_product_order(product_order: ProductOrder) -> str:
    return (
        f'{product_order.quantity} {product_order.product.name}: '
        f'{format_price(product_order.price)}'
    )


def address_model_instance_from_api_response(response: Response) -> Address:

    json_response = response.json()
    address_components = json_response['results'][0]['address_components']

    data = {
        'number': None,
        'street': None,
        'neighborhood': None,
        'city': None,
        'state': None,
        'country': None,
    }

    for index, key in enumerate(data):
        data[key] = address_components[index]['long_name']

    address = Address(
        number=data['number'],
        street=data['street'],
        neighborhood=data['neighborhood'],
        city=data['city'],
        state=data['state'],
        country=data['country']
    )

    return address


def format_address(address: Address) -> str:

    formatted_address = (
        f'Number: {address.number}' + '\n'
        f'Street: {address.street}' + '\n'
        f'Neighborhood: {address.neighborhood}' + '\n'
        f'State: {address.state}' + '\n'
        f'City: {address.city}' + '\n'
        f'Country: {address.country}' + '\n'
    )

    return formatted_address


def format_purchase(purchase: Purchase) -> str:
    formatted_purchase = ''

    formatted_purchase += (
        f'{format_datetime(purchase.datetime)}'
        '\n\n'
    )

    for product_order in purchase.products:
        formatted_purchase += (
            f'{format_product_order(product_order)}'
            '\n'
        )

    formatted_purchase += (
        '--------------------------\n'
        f'TOTAL: {format_price(purchase.total_price)}'
    )

    return formatted_purchase


def format_datetime(datetime: datetime):
    # all datetime saved in db is in UTC
    local_time = datetime - timedelta(hours=3)  # Brazil, PB
    return (
        local_time.strftime('%d/%m/%y %H:%M')
    )
