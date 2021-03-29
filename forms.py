"""Forms for adopt app."""
from flask_wtf import FlaskForm
from wtforms.validators import InputRequired, Optional, AnyOf, URL
from wtforms import StringField, SelectField, BooleanField
from flask_wtf.file import FileField, FileRequired, FileAllowed
# from flask_uploads import UploadSet, IMAGES


# images = UploadSet('images', IMAGES)


class AddPetForm(FlaskForm):
    """Form for adding pets"""

    name = StringField("Pet Name", 
                       validators=[InputRequired()])
    species = StringField("Pet species",
                          validators=[InputRequired(), AnyOf(["cat", "dog", "porcupine"])])
    # photo_url = StringField("Pet photo URL link", 
    #                         validators=[InputRequired(), URL()])
    photo_file = FileField('Pet Image', validators=[
        FileRequired(),
        FileAllowed(['png', 'jpg', 'jpeg'], 'Images only!')
    ])
    age = SelectField("Age", choices=[("baby", "Baby"), 
                                      ("young","Young"), 
                                      ("adult", "Adult"), 
                                      ("senior", "Senior")],
                                validators=[InputRequired(), AnyOf(["baby", "young", "adult", "senior"])])
    notes = StringField("Notes", validators=[Optional()])


class EditPetForm(FlaskForm):
    """Form for editing pets"""

    # photo_url = StringField("Pet photo URL link", 
    #                         validators=[InputRequired(), URL()])
    photo_file = FileField('Pet Image', validators=[
        FileRequired(),
        FileAllowed(['png', 'jpg', 'jpeg'], 'Images only!')
    ])
    notes = StringField("Notes", validators=[Optional()])
    available = BooleanField("Available", default="checked")