from flask import Blueprint, render_template, jsonify
from .database import db
from .models import Client, Chambre

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/api/inscription')
def inscription():
    new_clients = [
        Client(name='Moussa', email='moussa@gmail.com'),
        Client(name='Zach', email='zachmai@gmail.com'),
        Client(name='Lorill', email='idiot@gmail.com'),
    ]
    db.session.add_all(new_clients)
    db.session.commit()
    return jsonify(Client.name)


@main.route('/api/chambre-liste')
def chambre_liste():
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