# importer l'instanciation db de SQLAlchemy
from .database import db
from datetime import datetime

class Utilisateur(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    mot_de_passe_hash = db.Column(db.String(500), nullable=False)
    critiques= db.relationship('Critique', backref='utilisateur', lazy='dynamic')


class Film(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String(100), nullable=False)
    realisateur = db.Column(db.String(100))
    annee_sortie = db.Column(db.Integer)
    genre = db.Column(db.String(100))
    # critiques = db.relationship('Critique', backref='film', lazy='dynamic')
class Critique(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    contenu = db.Column(db.Text, nullable=False)
    date_post = db.Column(db.DateTime, default=datetime.utcnow)
    date_posts = db.Column(db.DateTime, default=datetime.utcnow)
    id_utilisateur = db.Column(db.Integer, db.ForeignKey('utilisateur.id'))
    id_film = db.Column(db.Integer, db.ForeignKey('film.id'))
    film = db.relationship('Film', backref='critique', lazy=True)