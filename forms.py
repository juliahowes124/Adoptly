"""Forms for adopt app."""
from flask_wtf import FlaskForm
from wtforms.validators import InputRequired, Optional, AnyOf, URL, ValidationError
from wtforms import StringField, SelectField, BooleanField
from flask_wtf.file import FileField, FileRequired, FileAllowed
# from flask_uploads import UploadSet, IMAGES


# images = UploadSet('images', IMAGES)

def one_photo_check(form, field):
    if form.photo_url.data and not isinstance(form.photo_file.data, str) and form.photo_file.data:
        raise ValidationError('Only one photo allowed')


class AddPetForm(FlaskForm):
    """Form for adding pets"""

    name = StringField("Pet Name", 
                       validators=[InputRequired()])
    species = StringField("Pet species",
                          validators=[InputRequired(), AnyOf(["cat", "dog", "porcupine"])])
    photo_url = StringField("Pet photo URL link", 
                            validators=[one_photo_check])
    photo_file = FileField('Pet Image', validators=[
        FileAllowed(['png', 'jpg', 'jpeg'], 'Images only!'), one_photo_check
    ])
    age = SelectField("Age", choices=[("baby", "Baby"), 
                                      ("young", "Young"), 
                                      ("adult", "Adult"), 
                                      ("senior", "Senior")],
                                validators=[InputRequired(), AnyOf(["baby", "young", "adult", "senior"])])
    notes = StringField("Notes", validators=[Optional()])


class EditPetForm(FlaskForm):
    """Form for editing pets"""

    name = StringField("Pet Name", validators=[InputRequired()])
    photo_url = StringField("Pet photo URL link", 
                            validators=[one_photo_check])
    photo_file = FileField('Pet Image', validators=[
        FileAllowed(['png', 'jpg', 'jpeg'], 'Images only!'), one_photo_check
    ])
    notes = StringField("Notes", validators=[Optional()])
    available = BooleanField("Available", default="checked")