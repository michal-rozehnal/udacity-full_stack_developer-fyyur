#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for, abort
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from flask_migrate import Migrate
from datetime import datetime
from enums import GenresEnum, StateEnum

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app, db)

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500)) 
    facebook_link = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    website = db.Column(db.String(300)) 
    seeking_talent = db.Column(db.Boolean()) 
    seeking_description = db.Column(db.String(300)) 


class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website = db.Column(db.String(300))
    seeking_venue = db.Column(db.Boolean())
    seeking_description = db.Column(db.String(300))

class Show(db.Model):
  __tablename__ = 'Show'

  artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'), primary_key = True)
  venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'), primary_key = True)
  start_time = db.Column(db.DateTime)

db.create_all()

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format)

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  venues_query = Venue.query.all()
  
  venues_by_location = {}
  for venue in venues_query:
    location = (venue.city, venue.state)
    location_venues = venues_by_location[location] if location in venues_by_location else []
    location_venues.append({
        "id": venue.id,
        "name": venue.name,
        "num_upcoming_shows": Show.query.filter(Show.venue_id == venue.id).filter(Show.start_time >= datetime.today()).count(),
      })

    venues_by_location[location] = location_venues

  data=[]
  for location in venues_by_location:
    data.append({
      "city": location[0],
      "state": StateEnum(int(location[1])).name,
      "venues": venues_by_location[location]
    })

  return render_template('pages/venues.html', areas=data)

@app.route('/venues/search', methods=['POST'])
def search_venues():
  search_term = request.form.get('search_term', '')

  venues = Venue.query.filter(Venue.name.ilike(f'%{ search_term }%')).all()
  shows_count = Show.query.filter(Show.venue_id == venue.id).filter(Show.start_time >= datetime.today()).count()
  
  data = []
  for venue in venues:
    data.append({
      "id": venue.id,
      "name": venue.name,
      "num_upcoming_shows": shows_count
    })

  response={
    "count": len(venues),
    "data": data
  }
  return render_template('pages/search_venues.html', results=response, search_term=search_term)

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  venue = Venue.query.get(venue_id)

  if not venue:
    abort(404)

  query = db.session.query(Show, Venue, Artist).filter(Show.artist_id == Artist.id).filter(Show.venue_id == Venue.id).filter(Venue.id == venue_id).all()
  past_shows = []
  upcoming_shows = []

  for item in query:
    show = {
      "artist_id": item.Artist.id,
      "artist_name": item.Artist.name,
      "artist_image_link": item.Artist.image_link,
      "start_time": str(item.Show.start_time)
    }

    if (item.Show.start_time < datetime.today()):
      past_shows.append(show)
    else:
      upcoming_shows.append(show)

  data = {
    "id": venue.id,
    "name": venue.name,
    "genres": map(lambda x: GenresEnum(int(x)).name, venue.genres.split(";") if venue.genres else []),
    "address": venue.address,
    "city": venue.city,
    "state": venue.state,
    "phone": venue.phone,
    "website": venue.website,
    "facebook_link": venue.facebook_link,
    "seeking_talent": Venue.seeking_talent,
    "seeking_description": venue.seeking_description,
    "image_link": venue.image_link,
    "past_shows": past_shows, 
    "upcoming_shows": upcoming_shows,
    "past_shows_count": len(past_shows),
    "upcoming_shows_count": len(upcoming_shows), 
  }

  return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  try:
    name = request.form.get('name')
    city = request.form.get('city')
    state = request.form.get('state')
    address = request.form.get('address')
    phone = request.form.get('phone')
    image_link = request.form.get('image_link')
    genres = ";".join(request.form.getlist('genres'))
    facebook_link = request.form.get('facebook_link')
    website = request.form.get('website')
    seeking_talent = request.form.get('seeking_talent')
    seeking_description = request.form.get('seeking_description')

    venue = Venue(
      name=name, 
      city=city,
      state=state, 
      address=address, 
      phone=phone, 
      image_link=image_link,
      genres=genres, 
      facebook_link=facebook_link,
      website=website,
      seeking_talent=seeking_talent,
      seeking_description=seeking_description
    )

    db.session.add(venue)
    db.session.commit()

    flash('Venue ' + request.form['name'] + ' was successfully listed!')

  except:
    db.session.rollback()
    flash(f'An error occurred. Venue {name} could not be listed.')

  return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  
  try:
    venue = Venue.query.get(venue_id)

    if not venue:
      abort(404)

    db.session.delete(venue)
    db.session.commit()

    return jsonify(success=True)
  except:
    db.session.rollback()
    return jsonify(success=False)

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  artists = Artist.query.all()

  data=[]

  for artist in artists:
    data.append({
      "id": artist.id,
      "name": artist.name,
    })

  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  search_term = request.form.get('search_term', '')

  artists = Artist.query.filter(Artist.name.ilike(f'%{ search_term }%')).all()
  shows_count = Show.query.filter(Show.artist_id == artist.id).filter(Show.start_time >= datetime.today()).count()

  data = []

  for artist in artists:
    data.append({
      "id": artist.id,
      "name": artist.name,
      "num_upcoming_shows": shows_count
    })

  response={
    "count": len(artists),
    "data": data
  }
  return render_template('pages/search_artists.html', results=response, search_term=search_term)

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  artist = Artist.query.get(artist_id)

  if not artist:
    abort(404)

  query = db.session.query(Show, Venue, Artist).filter(Show.artist_id == Artist.id).filter(Show.venue_id == Venue.id).filter(Show.artist_id == artist_id).all()
  past_shows = []
  upcoming_shows = []

  for item in query:
    show = {
      "venue_id": item.Venue.id,
      "venue_name": item.Venue.name,
      "venue_image_link": item.Venue.image_link,
      "start_time": str(item.Show.start_time)
    }

    if (item.Show.start_time < datetime.today()):
      past_shows.append(show)
    else:
      upcoming_shows.append(show)

  data = {
    "id": artist.id,
    "name": artist.name,
    "genres": map(lambda x: GenresEnum(int(x)).name, artist.genres.split(";") if artist.genres else []),
    "city": artist.city,
    "state": artist.state,
    "phone": artist.phone,
    "website": artist.website,
    "facebook_link": artist.facebook_link,
    "seeking_venue": artist.seeking_venue,
    "seeking_description": artist.seeking_description,
    "image_link": artist.image_link,
    "past_shows": past_shows,
    "upcoming_shows": upcoming_shows,
    "past_shows_count": len(past_shows),
    "upcoming_shows_count": len(upcoming_shows)
  }

  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  artist = Artist.query.get(artist_id)

  if not artist:
    abort(404)

  form = ArtistForm()
  artist={
    "id": artist.id,
    "name": artist.name,
    "genres": map(lambda x: GenresEnum(int(x)).name, artist.genres.split(";") if artist.genres else []),
    "city": artist.city,
    "state": artist.state,
    "phone": artist.phone,
    "website": artist.website,
    "facebook_link": artist.facebook_link,
    "seeking_venue": artist.seeking_venue,
    "seeking_description": artist.seeking_description,
    "image_link": artist.image_link
  }
  
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  try:
    artist = Artist.query.get(artist_id)

    if not artist:
      abort(404)

    artist.name = request.form.get("name")
    artist.genres = ";".join(request.form.getlist("genres"))
    artist.city = request.form.get("city")
    artist.state = request.form.get("state")
    artist.phone = request.form.get("phone")
    artist.website = request.form.get("website")
    artist.facebook_link = request.form.get("facebook_link")
    seeking_venue = request.form.get("seeking_venue")
    seeking_description = request.form.get("seeking_description")
    artist.image_link = request.form.get("image_link")

    db.session.commit()

    flash(f"Artist { artist.name } was updated")

  except:
    db.session.rollback()

    flash(f'An error occurred. Artist {artist.name} could not be updated.')

  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  venue = Venue.query.get(venue_id)

  if not venue:
    abort(404)

  form = VenueForm()
  venue={
    "id": venue.id,
    "name": venue.name,
    "genres": map(int, venue.genres.split(";") if venue.genres else []),
    "address": venue.address,
    "city": venue.city,
    "state": venue.state,
    "phone": venue.phone,
    "website": venue.website,
    "facebook_link": venue.facebook_link,
    "seeking_talent": venue.seeking_talent,
    "seeking_description": venue.seeking_description,
    "image_link": venue.image_link
  }
  
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  try:
    venue = Venue.query.get(venue_id)

    if not venue:
      abort(404)

    venue.name = request.form.get("name")    
    venue.city = request.form.get("city")
    venue.state = request.form.get("state")
    venue.address = request.form.get("address")
    venue.phone = request.form.get("phone")
    venue.image_link = request.form.get("image_link")
    venue.facebook_link = request.form.get("facebook_link")
    venue.genres = ";".join(request.form.getlist("genres"))
    venue.website = request.form.get("website")
    venue.seeking_talent = request.form.get("seeking_talent") == 'y'
    venue.seeking_description = request.form.get("seeking_description")

    db.session.commit()

    flash(f"Venue { venue.name } was updated")

  except:
    db.session.rollback()

    flash(f'An error occurred. Venue {venue.name} could not be updated.')

  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  try:
    name = request.form.get('name')
    city = request.form.get('city')
    state = request.form.get('state')
    phone = request.form.get('phone')
    genres = ";".join(request.form.getlist('genres'))
    image_link = request.form.get('image_link')
    facebook_link = request.form.get('facebook_link')
    website = request.form.get('website')
    seeking_venue = request.form.get('seeking_venue')
    seeking_description = request.form.get('seeking_description')

    artist = Artist(
      name=name, 
      city=city, 
      state=state, 
      phone=phone, 
      genres=genres,
      image_link=image_link,
      facebook_link=facebook_link,
      website=website,
      seeking_venue=seeking_venue,
      seeking_description=seeking_description,
    )

    db.session.add(artist)
    db.session.commit()

    flash(f'Artist {name} was successfully listed!')

  except:
    db.session.rollback()

    flash(f'An error occurred. Artist {name} could not be listed.')

  return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  shows = db.session.query(Show, Venue, Artist).filter(Show.venue_id == Venue.id).filter(Show.artist_id == Artist.id).all()

  data=[]
  for show in shows:
    data.append({
      "venue_id": show.Venue.id,
      "venue_name": show.Venue.name,
      "artist_id": show.Artist.id,
      "artist_name": show.Artist.name,
      "artist_image_link": show.Artist.image_link,
      "start_time": str(show.Show.start_time)
    })

  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  try:
    artist = request.form.get('artist_id')
    venue = request.form.get('venue_id')
    start_time = request.form.get('start_time')

    show = Show(
      artist_id = artist, 
      venue_id = venue, 
      start_time = start_time
    )
    db.session.add(show)
    db.session.commit()

    flash('Show was successfully listed!')

  except:
    db.session.rollback()

    flash('An error occurred. Show could not be listed.')

  return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
