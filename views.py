from flask import Blueprint, jsonify, request, render_template
from kanpai import Kanpai

from models import db, Client, Order

myapp = Blueprint('myapp', __name__)

@myapp.route('/')
def show_page():
    return render_template('clients.html')

@myapp.route('/clients', methods=['GET'])
def get_clients():
    clients = Client.get_all()
    results = [
        {
            'id': client.id,
            'name' : client.name,
            'phone' : str(client.phone)
            #'orders' : [ str(order.date) for order in client.orders ]
        } for client in clients ]
    return jsonify(results)

client_schema = Kanpai.Object({
    "id": Kanpai.Number(),
    "name": Kanpai.String().trim().required("Ім'я не може бути порожнім").max(90, error="Ім'я задовге"),
    "phone": Kanpai.Number('Телефон має складатись з чисел').required("Телефон не може бути порожнім").max(9999999999, error='Номер задовгий')
})

@myapp.route('/clients', methods=['POST'])
def create_client():
    validation_result = client_schema.validate(request.json)

    if validation_result.get('success', False) is False:
        return jsonify({
            'status': 'Error',
            'errors': validation_result.get('error')
        })

    data = validation_result.get('data')
    if not data['name'].replace(' ', '').isalpha():
        return jsonify({
            'status': 'Error',
            'errors': "Ім'я має складатись лише з літер"
        })
    if Client.query.filter_by(phone=data['phone']).first() is not None:
        return jsonify({
            'status': 'Error',
            'errors': "Клієнт з таким номером вже існує"
        })

    Client(name=data['name'], phone=data['phone']).save()
    return jsonify({
        'status': 'Success'})

@myapp.route('/clients/<id>', methods=['DELETE'])
def delete_client(id):
    data = request.json
    client = Client.query.get(id).delete()
    db.session.delete(client)
    db.session.commit()
    return jsonify({
        'status': 'Success'
    })

@myapp.route('/clients/<id>', methods=['PUT'])
def update_client(id):
    data = request.json
    client = Client.query.get(id)


    validation_result = client_schema.validate(request.json)

    if validation_result.get('success', False) is False:
        return jsonify({
            'status': 'Error',
            'errors': validation_result.get('error')
        })

    data = validation_result.get('data')
    if not data['name'].replace(' ', '').isalpha():
        return jsonify({
            'status': 'Error',
            'errors': "Ім'я має складатись лише з літер"
        })
    exists = Client.query.filter_by(phone=data['phone']).first()
    if exists is not None and str(exists.id) != str(id):
        return jsonify({
            'status': 'Error',
            'errors': "Клієнт з таким номером вже існує"
        })

    client.phone = data['phone']
    client.name = data['name']
    client.save()
    return jsonify({
        'status': 'Success'
    })

#====================Orders Views ========================
@myapp.route('/orders', methods=['GET'])
def get_orders():
    orders = Order.get_all()
    results = [
        {
            'id': order.id,
            'client_id' : order.client_id,
            'date' : str(order.date)
        } for order in orders ]
    return jsonify(results)

@myapp.route('/orders', methods=['POST'])
def create_order():
    data = request.json

    Order(client_id=data['client_id'], date=data['date']).save()
    return jsonify({
        'status': 'Success'})

@myapp.route('/orders/<id>', methods=['DELETE'])
def delete_order(id):
    data = request.json
    Order.query.get(id).delete()
    return jsonify({
        'status': 'Success'
    })

@myapp.route('/orders/<id>', methods=['PUT'])
def update_order(id):
    data = request.json
    order = Order.query.get(id)

    order.date = data['date']
    order.client_phone = data['client_phone']
    order.save()
    return jsonify({
        'status': 'Success'
    })
