import pytest
from module_30_ci_linters.homework.app import create_app, db
from module_30_ci_linters.homework.app.models import (
    Client,
    Parking,
    ClientParking,
)
from datetime import datetime, timedelta


@pytest.fixture(scope='module')
def app():
    app = create_app()
    app.config.update({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'SQLALCHEMY_TRACK_MODIFICATIONS': False,
    })

    with app.app_context():
        db.create_all()
        client = Client(
            name='Test',
            surname='User',
            credit_card='12345678',
            car_number='ABC123',
        )
        parking = Parking(
            address='Test Address',
            opened=True,
            count_places=10,
            count_available_places=10,
        )
        db.session.add_all([client, parking])
        db.session.commit()

        time_in = datetime.utcnow() - timedelta(hours=1)
        time_out = datetime.utcnow()
        client_parking = ClientParking(
            client_id=client.id,
            parking_id=parking.id,
            time_in=time_in,
            time_out=time_out,
        )
        db.session.add(client_parking)
        db.session.commit()

    yield app

    with app.app_context():
        db.drop_all()


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def db_session(app):
    with app.app_context():
        yield db
