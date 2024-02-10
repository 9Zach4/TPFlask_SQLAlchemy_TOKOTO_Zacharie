# importer l'instanciation db de SQLAlchemy
from .database import db
from datetime import datetime

class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
  
class Chambre(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    numero = db.Column(db.String(10), unique=True, nullable=False)  
    type = db.Column(db.String(50), nullable=False)
    prix = db.Column(db.Float, nullable=False)
    reservations = db.relationship('Reservation', backref='chambre', lazy='dynamic')


class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_client = db.Column(db.Integer, db.ForeignKey('client.id'))  
    id_chambre = db.Column(db.Integer, db.ForeignKey('chambre.id'))  
    date_arrivee = db.Column(db.DateTime, nullable=False)
    date_depart = db.Column(db.DateTime, nullable=False)
    statut = db.Column(db.String(50), nullable=False)