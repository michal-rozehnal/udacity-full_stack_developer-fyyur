from datetime import datetime
from flask_wtf import Form
from wtforms import StringField, SelectField, SelectMultipleField, DateTimeField, BooleanField
from wtforms.validators import DataRequired, AnyOf, URL, Length
from enums import StateEnum, GenresEnum

class ShowForm(Form):
    artist_id = StringField(
        'artist_id'
    )
    venue_id = StringField(
        'venue_id'
    )
    start_time = DateTimeField(
        'start_time',
        validators=[DataRequired()],
        default= datetime.today()
    )

class VenueForm(Form):
    name = StringField(
        'name', 
        validators=[DataRequired()]
    )
    city = StringField(
        'city', 
        validators=[DataRequired()]
    )
    state = SelectField(
        'state',
        validators=[DataRequired()],
        choices = StateEnum.choices(),
        coerce = StateEnum.coerce
    )
    address = StringField(
        'address', 
        validators=[DataRequired()]
    )
    phone = StringField(
        'phone', 
        validators=[Length(min=9, max=9)]
    )
    image_link = StringField(
        'image_link',
        validators=[URL()]
    )
    genres = SelectMultipleField(
        'genres', 
        validators=[DataRequired()],
        choices = GenresEnum.choices(),
        coerce = GenresEnum.coerce
    )
    facebook_link = StringField(
        'facebook_link', 
        validators=[URL()]
    )
    image_link = StringField(
        'image_link', 
        validators=[URL()]
    )
    website = StringField(
        'website', 
        validators=[URL()]
    )
    seeking_talent = BooleanField(
        'seeking_talent',
        false_values={False, 'false', ''}
    )
    seeking_description = StringField(
        'seeking_description', 
        validators=[URL()]
    )

class ArtistForm(Form):
    name = StringField(
        'name', 
        validators=[DataRequired()]
    )
    city = StringField(
        'city', 
        validators=[DataRequired()]
    )
    state = SelectField(
        'state',
        validators=[DataRequired()],
        choices = StateEnum.choices(),
        coerce = StateEnum.coerce
    )
    phone = StringField(
        'phone', 
        validators=[Length(min=9, max=9)]
    )
    image_link = StringField(
        'image_link'
    )
    genres = SelectMultipleField(
        'genres', 
        validators=[DataRequired()],
        choices = GenresEnum.choices(),
        coerce = GenresEnum.coerce
    )
    facebook_link = StringField(
        'facebook_link', 
        validators=[URL()]
    )
    website = StringField(
        'website', 
        validators=[URL()]
    )
    seeking_venue = BooleanField(
        'seeking_venue',
        false_values={False, 'false', ''}
    )
    seeking_description = StringField(
        'seeking_description', 
        validators=[URL()]
    )