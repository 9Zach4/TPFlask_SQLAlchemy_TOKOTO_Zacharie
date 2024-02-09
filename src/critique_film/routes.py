from flask import Blueprint, render_template
from .forms import InscriptionForm, AjoutFilmForm, CritiqueForm
from werkzeug.security import generate_password_hash
from .database import db
from .models import *


main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('index.html')

@main.route('/inscription', methods=['GET', 'POST'])
def inscription():
    form = InscriptionForm()
    # opérations pour enregistrer le formulaire
    if form.validate_on_submit():
        # enregistrer le formulaire
        # générer le hash du mot de passe
        hashed_password = generate_password_hash(form.mot_de_passe.data, salt_length=8)
        # enregistrer l'utilisateur
        new_user = Utilisateur(
            nom=form.nom.data,
            email=form.email.data,
            mot_de_passe_hash=hashed_password
        )

        # ajouter l'utilisateur dans la base de données
        # Enregistrer la modification
        db.session.add(new_user)

        # Appliquer les modifications
        db.session.commit()
        return render_template('index.html')
    return render_template('inscription.html', form=form)



@main.route('/films')
def films():
    films = Film.query.all()
    return render_template('films.html', films=films)

@main.route('/film/<int:id>')
def film_detail(id):
    film = Film.query.get_or_404(id)
    return render_template('film_detail.html', film=film)

@main.route('/ajouter-film', methods=['GET', 'POST'])
def ajouter_film():
    form = AjoutFilmForm()
    if form.validate_on_submit():
        new_film = Film(
            titre=form.titre.data,
            realisateur=form.realisateur.data,
            annee_sortie=form.annee_sortie.data,
            genre=form.genre.data
        )
        db.session.add(new_film)
        db.session.commit()
        return render_template('index.html')
    return render_template('ajouter_film.html', form=form)

@main.route('/films/<int:id>/critique', methods=['GET', 'POST'])
def film_critique(id):
    form = CritiqueForm()
    film = Film.query.get_or_404(id)
    if form.validate_on_submit():
        new_critique = Critique(
            contenu=form.contenu.data,
            film=film,
        )
        db.session.add(new_critique)
        db.session.commit()
        return render_template('film_detail.html', film=film)
    return render_template('ajouter_critique.html', form=form, film=film)
