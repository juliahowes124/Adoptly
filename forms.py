"""Forms for adopt app."""
from flask_wtf import FlaskForm
from wtforms.validators import InputRequired, Optional, AnyOf, URL
from wtforms import StringField, SelectField


class AddPetForm(FlaskForm):
    """Form for adding pets"""

    name = StringField("Pet Name", 
                       validators=[InputRequired()])
    species = StringField("Pet species",
                          validators=[InputRequired(), AnyOf(["cat", "dog", "porcupine"])])
    photo_url = StringField("Pet photo URL link", 
                            validators=[InputRequired(), URL()])
    age = SelectField("Age", choices=[("baby", "Baby"), 
                                      ("young","Young"), 
                                      ("adult", "Adult"), 
                                      ("senior", "Senior")],
                             validators=[InputRequired(), AnyOf(["baby", "young", "adult", "senior"])])
    notes = StringField("Notes", validators=[Optional()])