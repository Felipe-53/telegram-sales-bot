from . import db
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.sqlite import BLOB
from uuid import uuid4
from datetime import datetime, timezone

db: SQLAlchemy


class Owner(db.Model):
    __tablename__ = 'owners'

    pk = db.Column(db.String, primary_key=True, default=lambda: str(uuid4()))
    token = db.Column(db.String)
    email = db.Column(db.String(), nullable=False)
    password = db.Column(db.String(), nullable=False)
    name = db.Column(db.String(50))
    phone = db.Column(db.String())

    products = db.relationship('Product', back_populates='owner')
    clients = db.relationship('Client', back_populates='owner')


class Client(db.Model):
    __tablename__ = 'clients'

    pk = db.Column(db.Integer, primary_key=True)
    phone = db.Column(db.String)
    name = db.Column(db.String)

    chat_id = db.Column(db.Integer)
    telegram_user_id = db.Column(db.Integer)

    stage = db.Column(db.String, nullable=False)

    cart = db.relationship('Cart', back_populates='client')

    owner_pk = db.Column(db.ForeignKey('owners.pk'), nullable=False)
    owner = db.relationship('Owner', back_populates='clients')

    purchases = db.relationship('Purchase', back_populates='client')
    addresses = db.relationship('ClientAddress', back_populates='client')


class Product(db.Model):
    __tablename__ = 'products'

    pk = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.String)
    picture = db.Column(BLOB)
    price = db.Column(db.Integer)
    quantity = db.Column(db.Integer)

    owner_pk = db.Column(db.String, db.ForeignKey('owners.pk'))
    owner = db.relationship('Owner', back_populates='products')

    product_orders = db.relationship('ProductOrder', back_populates='product')


class ProductOrder(db.Model):
    __tablename__ = 'product_orders'

    pk = db.Column(db.Integer, primary_key=True)

    belongs_to = db.Column(db.String)  # cart | purchase

    cart_pk = db.Column(db.ForeignKey('carts.pk'))
    cart = db.relationship('Cart', back_populates='products')

    purchase_pk = db.Column(db.ForeignKey('purchases.pk'))
    purchase = db.relationship('Purchase', back_populates='products')

    product_pk = db.Column(db.ForeignKey('products.pk'))
    product = db.relationship('Product', back_populates='product_orders')
    quantity = db.Column(db.Integer)

    @property
    def price(self) -> int:
        return self.quantity * self.product.price


class Cart(db.Model):
    __tablename__ = 'carts'

    pk = db.Column(db.Integer, primary_key=True)

    client_pk = db.Column(db.ForeignKey('clients.pk'))
    client = db.relationship('Client', back_populates='cart')

    products = db.relationship('ProductOrder', back_populates='cart')

    @property
    def total_price(self) -> int:
        total = 0
        product_order: ProductOrder

        for product_order in self.products:
            total += product_order.price

        return total


class Purchase(db.Model):
    __tablename__ = 'purchases'

    pk = db.Column(db.Integer, primary_key=True)

    client_pk = db.Column(db.ForeignKey('clients.pk'))
    client = db.relationship('Client', back_populates='purchases')

    products = db.relationship('ProductOrder', back_populates='purchase')

    datetime = db.Column(
        db.DateTime,
        default=lambda: datetime.now(tz=timezone.utc)
    )

    @property
    def total_price(self) -> int:
        total = 0
        product_order: ProductOrder

        for product_order in self.products:
            total += product_order.price

        return total


class ClientAddress(db.Model):
    __tablename__ = 'client_addresses'

    pk = db.Column(db.Integer, primary_key=True)

    number = db.Column(db.Integer)
    street = db.Column(db.String)
    neighborhood = db.Column(db.String)
    city = db.Column(db.String)
    state = db.Column(db.String)
    country = db.Column(db.String)
    details = db.Column(db.String)

    client_pk = db.Column(db.ForeignKey('clients.pk'), nullable=False)
    client = db.relationship('Client', back_populates='addresses')
