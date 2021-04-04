"""Flask app for adopt app."""
import os

import copy

from flask import Flask, render_template, redirect, flash, request

from flask_debugtoolbar import DebugToolbarExtension

from models import db, connect_db, Pet

from forms import AddPetForm, EditPetForm

from petfinder import get_auth_token, get_random_pet

from werkzeug.utils import secure_filename
from werkzeug.datastructures import CombinedMultiDict

UPLOAD_FOLDER = './static'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = "secret"
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///adopt"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()

auth_token = None


@app.before_first_request
def refresh_credentials():
    global auth_token
    auth_token = get_auth_token()


@app.route('/')
def show_index():
    """ Display home page with all pets listed """

    pets = Pet.query.order_by(Pet.available.desc()).all()
    petfinder_pet = get_random_pet()

    return render_template('pet_list.html', pets=pets, random_pet=petfinder_pet)


@app.route('/add', methods=["GET", "POST"])
def show_pet_form():
    """ Display form for adding new pet and handle form submission """ 
    
    form = AddPetForm(CombinedMultiDict((request.files, request.form)))
    if form.validate_on_submit():
        new_pet = Pet()
        form.populate_obj(new_pet)
        if form.photo_file.data:
            f = form.photo_file.data
            filename = secure_filename(f.filename)
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            new_pet.photo_file = filename
        if new_pet.photo_url == '':
            new_pet.photo_url = None
        db.session.add(new_pet)
        db.session.commit()
        flash(f"Pet {new_pet.name} added!", "success")
        return redirect("/")
    else:
        return render_template("pet_form.html", form=form)


@app.route('/<int:id>', methods=["GET", 'POST'])
def show_pet_details(id):
    """ Display pet details and edit form, and handle edit submissions """

    pet = Pet.query.get_or_404(id)
    object_for_form = copy.deepcopy(pet)
    del object_for_form.photo_url
    form = EditPetForm(CombinedMultiDict((request.files, request.form)), obj=object_for_form)

    if form.validate_on_submit():
        if form.photo_url.data == '':
            del form.photo_url
        if isinstance(form.photo_file.data, str):
            del form.photo_file
        form.populate_obj(pet)
        if form.photo_file and form.photo_file.data:
            f = form.photo_file.data
            filename = secure_filename(f.filename)
            pet.photo_file = filename
            pet.photo_url = None
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        elif form.photo_url:
            pet.photo_file = None
        
        db.session.commit()
        flash(f"Pet {pet.name} updated!", "success")
        return redirect(f"/{id}")
    else:
        form.available.data = object_for_form.available
        return render_template('pet_details.html', form=form, pet=pet)


@app.route('/static/<path:path>')
def static_file(path):
    return app.send_static_file(path)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
