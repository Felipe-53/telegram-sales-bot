from server.models import Owner, Product
from server import create_app, db, bcrypt
import requests
from os import environ, path
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))
token = environ.get('TOKEN')


def convert_to_binary_data(filename) -> bytes:
    with open(filename, 'rb') as file:
        blob_data = file.read()
    return blob_data


owner = Owner(
    name='Fernanda',
    email='fernanda@email.com',
    password=bcrypt.generate_password_hash('fernanda').decode(),
    token=token
)

products = {
    'p1': Product(
        name='Shirt',
        description='A beautiful shirt',
        picture=convert_to_binary_data('./images/shirt.jpg'),
        price=2500,
        quantity=10,
        owner=owner
    ),

    'p2': Product(
        name='Shoes',
        description='Some awesome shoes',
        picture=convert_to_binary_data('./images/shoes.jpg'),
        price=7000,
        quantity=10,
        owner=owner
    )
}

data = []
data.append(owner)
for key in products:
    data.append(products[key])

app = create_app()
with app.app_context():

    db.drop_all()
    db.create_all()

    for item in data:
        db.session.add(item)

    db.session.commit()

response = requests.post('http://localhost:5000/register_bot', json={
    'token': token
})

if response.json()['ok'] is True:
    print('Webhook for the user was properly set')
else:
    print('Something went wrong')
