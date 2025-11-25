import pytest


@pytest.mark.parametrize('url', ['/clients', '/clients/1'])
def test_get_endpoints(client, url):
    resp = client.get(url)
    assert resp.status_code == 200



def test_create_client(client):
    data = {'name': 'New', 'surname': 'Client', 'credit_card': '987654321', 'car_number': 'XYZ789'}
    resp = client.post('/clients', json=data)
    assert resp.status_code == 201


def test_create_parking(client):
    data = {'address': 'New Addr', 'opened': True, 'count_places': 20}
    resp = client.post('/parkings', json=data)
    assert resp.status_code == 201


@pytest.mark.parking
def test_client_enter_parking(client):
    resp = client.post('/client_parkings', json={'client_id': 1, 'parking_id': 1})
    assert resp.status_code == 201


@pytest.mark.parking
def test_client_exit_parking(client):
    resp = client.delete('/client_parkings', json={'client_id': 1, 'parking_id': 1})
    assert resp.status_code == 200
