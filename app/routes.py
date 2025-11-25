from flask import Blueprint, request, jsonify
from .models import db, Client, Parking, ClientParking
from datetime import datetime

bp = Blueprint('api', __name__)


@bp.route('/clients', methods=['GET'])
def get_clients():
    clients = Client.query.all()
    return jsonify([{
        'id': c.id,
        'name': c.name,
        'surname': c.surname,
        'credit_card': c.credit_card,
        'car_number': c.car_number
    } for c in clients])


@bp.route('/clients/<int:client_id>', methods=['GET'])
def get_client(client_id):
    client = Client.query.get_or_404(client_id)
    return jsonify({
        'id': client.id,
        'name': client.name,
        'surname': client.surname,
        'credit_card': client.credit_card,
        'car_number': client.car_number
    })


@bp.route('/clients', methods=['POST'])
def create_client():
    data = request.get_json()
    new_client = Client(
        name=data['name'],
        surname=data['surname'],
        credit_card=data.get('credit_card'),
        car_number=data.get('car_number')
    )
    db.session.add(new_client)
    db.session.commit()
    return jsonify({'message': 'Client created', 'id': new_client.id}), 201


@bp.route('/parkings', methods=['POST'])
def create_parking():
    data = request.get_json()
    new_parking = Parking(
        address=data['address'],
        opened=data.get('opened', True),
        count_places=data['count_places'],
        count_available_places=data['count_places']
    )
    db.session.add(new_parking)
    db.session.commit()
    return jsonify({'message': 'Parking created', 'id': new_parking.id}), 201


@bp.route('/client_parkings', methods=['POST'])
def client_enter_parking():
    data = request.get_json()
    client = Client.query.get_or_404(data['client_id'])
    parking = Parking.query.get_or_404(data['parking_id'])

    if not parking.opened or parking.count_available_places <= 0:
        return jsonify({'error': 'Parking closed or no available places'}), 400

    parking.count_available_places -= 1
    client_parking = ClientParking(
        client_id=client.id,
        parking_id=parking.id,
        time_in=datetime.utcnow(),
        time_out=None
    )
    db.session.add(client_parking)
    db.session.commit()
    return jsonify({'message': 'Entry recorded'}), 201


@bp.route('/client_parkings', methods=['DELETE'])
def client_exit_parking():
    data = request.get_json()
    client = Client.query.get_or_404(data['client_id'])
    parking = Parking.query.get_or_404(data['parking_id'])

    client_parking = ClientParking.query.filter_by(client_id=client.id, parking_id=parking.id, time_out=None).first()
    if not client_parking:
        return jsonify({'error': 'Entry not found or already exited'}), 404

    if not client.credit_card:
        return jsonify({'error': 'Payment failed: no credit card attached'}), 400

    client_parking.time_out = datetime.utcnow()
    parking.count_available_places += 1
    db.session.commit()

    return jsonify({'message': 'Exit recorded, payment processed'}), 200
