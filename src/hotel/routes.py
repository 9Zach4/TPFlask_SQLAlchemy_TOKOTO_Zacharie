from flask import Blueprint, render_template, jsonify, request
from .database import db
from .models import Client, Chambre, Reservation
from datetime import datetime

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('index.html')



def inscription():
    new_clients = [
        Client(name='Moussa', email='moussa@gmail.com'),
        Client(name='Zach', email='zachmai@gmail.com'),
        Client(name='Lorill', email='idiot@gmail.com'),
    ]
    db.session.add_all(new_clients)
    db.session.commit()
    return jsonify(Client.name)

@main.route('/api/client/liste', methods=['GET'])
def client_list():
    clients = Client.query.all()
    client_liste = []
    for client in clients:
        client_dict = {
            'id': client.id,
            'name': client.name,
            'email': client.email,
          
        }
        client_liste.append(client_dict)
    return jsonify(client_liste), 200



def room_list():
  simpleRoom = [
    Chambre(number=1, type='simple', price=80),
    Chambre(number=2, type='simple', price=80),
    Chambre(number=3, type='simple', price=80),
  ]

  suiteRoom = [
    Chambre(number=4, type='suite', price=150),  
    Chambre(number=5, type='suite', price=150),
    Chambre(number=6, type='suite', price=150),
 ]

  luxuryRoom = [ 
    Chambre(number=7, type='luxieuse', price=300),
    Chambre(number=8, type='luxieuse', price=300),
    Chambre(number=9, type='luxieuse', price=300),
 ]

  db.session.add_all(suiteRoom)   
  db.session.add_all(simpleRoom)
  db.session.add_all(luxuryRoom)
  db.session.commit()

@main.route('/api/chambres/liste', methods=['GET'])
def room_list():

    chambres = Chambre.query.all()

    chambre_liste = []
    for chambre in chambres:
        chambre_dict = {
            'number': chambre.number,
            'type': chambre.type,
            "id": chambre.id,
            'price': chambre.price
        }
        chambre_liste.append(chambre_dict)

    return jsonify(chambre_liste), 200

@main.route('/api/chambres/disponibles', methods=['GET'])
def room_available():
    date_arrivee_str = request.args.get('date_arrivee')
    date_depart_str = request.args.get('date_depart')
    # date_arrivee= 2024-02-15
    # date_depart=24-02-20

    date_arrivee = datetime.strptime(date_arrivee_str, '%Y-%m-%d')
    date_depart = datetime.strptime(date_depart_str, '%Y-%m-%d')

    chambres = Chambre.query.all()
    chambres_disponibles = []
    for chambre in chambres:
        reservations = Reservation.query.filter(Reservation.id_chambre == chambre.id).all()
        chambre_dict = {
            'number': chambre.number,
            'type': chambre.type,
            'price': chambre.price
        }
        chambre_disponible = True
        for reservation in reservations:
            if date_arrivee < reservation.departure_date and date_depart > reservation.arrival_date:
                chambre_disponible = False
        if chambre_disponible:
            chambres_disponibles.append(chambre_dict)
    return jsonify(chambres_disponibles), 200

@main.route('/api/reservations', methods=['POST'])
def reservation():
    id_client = request.json.get('id_client')
    id_chambre = request.json.get('id_chambre')
    date_arrivee = request.json.get('date_arrivee')
    date_depart = request.json.get('date_depart')

    chambre_disponible = check_room_availability(id_chambre, date_arrivee, date_depart)
    
    if not chambre_disponible:
        return jsonify({"message": "La chambre n'est pas disponible pour les dates demandées."}), 400

    reservation = Reservation(
        id_client=id_client,
        id_chambre=id_chambre,
        arrival_date=date_arrivee,
        departure_date=date_depart,
        statut='en attente'
    )
    db.session.add(reservation)
    db.session.commit()
    return jsonify('Reservation effectuee'), 201

def check_room_availability(id_chambre, date_arrivee, date_depart):
  
    date_arrivee = datetime.strptime(date_arrivee, '%Y-%m-%d')
    date_depart = datetime.strptime(date_depart, '%Y-%m-%d')

    
    reservations = Reservation.query.filter_by(id_chambre=id_chambre).all()

    for reservation in reservations:
        if date_arrivee < reservation.departure_date and date_depart > reservation.arrival_date:
            return False

    return True

@main.route('/api/reservations/<int:id>', methods=['DELETE'])
def delete_reservation(id):
    reservation = Reservation.query.get(id)
    if not reservation:
        return jsonify({"message": "La reservation n'existe pas"}), 404
    db.session.delete(reservation)
    db.session.commit()
    return jsonify({"message": "Réservation annulée avec succès"}), 200

@main.route('/api/chambres', methods=['POST'])
def add_room():
    data = request.json

    if not all(key in data for key in ['id', 'number', 'type', 'price']):
        return jsonify({'error': 'Informations manquante.'}), 400
    
    id = data.get('id')
    number = data.get('number')
    type = data.get('type')
    price = data.get('price')

    existing_room = Chambre.query.filter_by(number=number).first()
    if existing_room:
        return jsonify({'error': 'Une chambre avec ce numéro existe déjà.'}), 409  

    
    chambre = Chambre(id= id, number=number, type=type, price=price)
   
    db.session.add(chambre)
    db.session.commit()

    return jsonify({"message": "Chambre ajoutée avec succès."}), 201


@main.route('/api/chambres/<int:id>', methods=['DELETE'])
def delete_room(id):
    chambre = Chambre.query.get(id)
    if not chambre:
        return jsonify({"message": "La chambre n'existe pas"}), 404
    db.session.delete(chambre)
    db.session.commit()
    return jsonify({"message": "Chambre supprimée avec succès"}), 200

@main.route('/api/chambres/<int:id>', methods=['PUT'])
def update_room(id):
    chambre = Chambre.query.get(id)
    if not chambre:
        return jsonify({"message": "La chambre n'existe pas"}), 404
    data = request.json
    chambre.number = data.get('number')
    chambre.type = data.get('type')
    chambre.price = data.get('price')
    db.session.commit()
    return jsonify({"message": "Chambre modifiée avec succès"}), 200