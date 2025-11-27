import factory
from faker import Faker
from module_30_ci_linters.homework.app.models import (
    Client,
    Parking,
)
from module_30_ci_linters.homework.app.extensions import db

fake = Faker()


class ClientFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Client
        sqlalchemy_session = db.session
        sqlalchemy_session_persistence = 'commit'

    name = factory.Faker('first_name')
    surname = factory.Faker('last_name')
    credit_card = factory.LazyFunction(
        lambda: fake.credit_card_number() if fake.boolean() else None
    )
    car_number = factory.Faker('bothify', text='???-####')


class ParkingFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Parking
        sqlalchemy_session = db.session
        sqlalchemy_session_persistence = 'commit'

    address = factory.Faker('address')
    opened = factory.Faker('boolean')
    count_places = factory.Faker('random_int', min=5, max=100)
    count_available_places = factory.LazyAttribute(
        lambda obj: obj.count_places
    )
