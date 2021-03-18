"""Flask app for adopt app."""

from flask import Flask, render_template, redirect, flash

from flask_debugtoolbar import DebugToolbarExtension

from models import db, connect_db, Pet

from forms import AddPetForm, EditPetForm

from petfinder import get_auth_token, get_random_pet

app = Flask(__name__)

app.config['SECRET_KEY'] = "secret"

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///adopt"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

connect_db(app)
db.create_all()

toolbar = DebugToolbarExtension(app)
auth_token = None


@app.before_first_request
def refresh_credentials():
    global auth_token
    auth_token = get_auth_token()


@app.route('/')
def show_index():
    """ Display home page with all pets listed """

    pets = Pet.query.all()
    petfinder_pet = get_random_pet()

    return render_template('pet_list.html', pets=pets, random_pet=petfinder_pet)


@app.route('/add', methods=["GET", "POST"])
def show_pet_form():
    """ Display form for adding new pet and handle form submission """ 

    form = AddPetForm()

    if form.validate_on_submit():
        new_pet = Pet(name=form.name.data,
                      species=form.species.data,
                      photo_url=form.photo_url.data,
                      age=form.age.data,
                      notes=form.notes.data)
        db.session.add(new_pet)
        db.session.commit()
        flash(f"Pet {new_pet.name} added!", "success")
        return redirect("/")
    else:
        return render_template("pet_form.html",form=form)


@app.route('/<int:id>', methods=["GET", 'POST'])
def show_pet_details(id):
    """ Display pet details and edit form, and handle edit submissions """

    pet = Pet.query.get_or_404(id)
    form = EditPetForm(obj=pet)

    if form.validate_on_submit():
        pet.photo_url = form.photo_url.data
        pet.notes = form.notes.data
        pet.available = form.available.data
        db.session.commit()
        flash(f"Pet {pet.name} updated!", "success")
        return redirect(f"/{id}")
    else:
        return render_template('pet_details.html', form=form, pet=pet)
        
