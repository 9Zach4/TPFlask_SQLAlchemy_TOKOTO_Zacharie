from .database import db
from datetime import datetime


class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(75), nullable=False)
    email = db.Column(db.String(150), nullable=False, unique=True)
    bookings = db.relationship('Reservation', backref='client', lazy="dynamic")


class Chambre(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer, nullable=False, unique=True)
    type = db.Column(db.String(60), nullable=False)
    price = db.Column(db.Float, nullable=False)
    bookings = db.relationship('Reservation', backref='chambre', lazy="dynamic")


class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_client = db.Column(db.Integer, db.ForeignKey('client.id'))
    id_chambre = db.Column(db.Integer, db.ForeignKey('chambre.id'))
    arrival_date = db.Column(db.DateTime, default=datetime.utcnow)
    departure_date = db.Column(db.DateTime, default=datetime.utcnow)
    statut = db.Column(db.String(50), nullable=True)