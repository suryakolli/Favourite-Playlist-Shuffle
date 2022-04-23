import flask
import api
import requests
from lyricsgenius import Genius
import random
import html
import os
from dotenv import load_dotenv
from flask_login import LoginManager, current_user, login_user, logout_user
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_required, UserMixin


load_dotenv()

app = flask.Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# Models
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))

    def get_username(self):
        return self.username


class Playlist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    playlist_id = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(50), nullable=False)

    def get_username(self):
        return self.username

    def get_playlist_id(self):
        return self.playlist_id

# db.drop_all()
db.create_all()

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)


@login_manager.user_loader
def load_user(username):
    return User.query.get(username)


# render sign up page
@app.route('/signup')
def signup():
    return flask.render_template("signup.html")


@app.route('/signup', methods=["POST"])
def signup_user_route():
    username = flask.request.form.get('username')
    user = User.query.filter_by(username=username).first()
    if user is None:
        user = User(username=username)
        db.session.add(user)
        db.session.commit()

    return flask.redirect(flask.url_for('login'))


# render login page
@app.route('/login')
def login():
    logout_user()
    return flask.render_template("login.html")


@app.route('/login', methods=["POST"])
def login_user_route():
    username = flask.request.form.get('username')
    user = User.query.filter_by(username=username).first()
    if user is None:
        return flask.jsonify(
            {"status": 401, "reason": "Username not found, try signing up"}
        )

    login_user(user)
    return flask.redirect(flask.url_for('home'))


@app.route('/add-favourite', methods=["POST"])
@login_required
def add_favourite():
    playlist_id = flask.request.form.get('playlist_id')
    print(playlist_id)
    try:
        response = api.client.get_resource(playlist_id)
        print(response)
        if len(response) == 0:
            flask.flash("Playlist Not Found")
            return flask.redirect(flask.url_for('home'))
    except (ValueError, Exception):
        flask.flash("Playlist Not Found")
        return flask.redirect(flask.url_for('index'))

    db.session.add(
        Playlist(
            playlist_id=playlist_id,
            username=current_user.username
        ))
    db.session.commit()
    return flask.redirect(flask.url_for('home'))


@app.route('/')
def index():
    if current_user.is_authenticated:
        return flask.redirect(flask.url_for('home'))
    return flask.redirect(flask.url_for('login'))


genius = Genius(os.getenv('genius_access_token', ""))


@app.route('/home')
def home():
    playlists = Playlist.query.filter_by(username=current_user.username).all()
    if len(playlists) > 0:
        return play_song(playlists)
    else:
        return flask.render_template('no_playlists.html',
                                     username=current_user.username)



@app.route('/about')
def about():
    return flask.render_template('about.html')


@app.route('/desc')
def desc():
    return flask.render_template('desc.html')

@app.route('/checklist')
def checklist():
    return flask.render_template('checklist.html')


def play_song(playlists):
    response = api.client.get_resource(getattr(playlists[random.randint(0, len(playlists) - 1)], 'playlist_id'))
    
    playlist_image = response['images'][0]['url']
    playlist_name = response['name']
    playlist_description = html.unescape(response['description'])
    preview_url = None
    item = response['tracks']['items'][random.randint(0, len(response['tracks']['items']) - 1)]
    while preview_url is None:
        item = response['tracks']['items'][random.randint(0, len(response['tracks']['items']) - 1)]
        preview_url = item['track']['preview_url']
    info = item['track']['album']['release_date']
    track_image = item['track']['album']['images'][0]['url']
    track_name = item['track']['name']
    artist_name = item['track']['artists'][0]['name']
    search_term = f"{track_name} {artist_name}"
    client_access_token = os.getenv('genius_access_token', "")
    genius_search_url = f"https://api.genius.com/search?q={search_term}&access_token={client_access_token}"
    res = requests.get(genius_search_url)
    json_data = res.json()
    lyrics_url = '#'
    is_lyrics_available = 'disabled'
    if len(json_data['response']['hits']) > 0:
        lyrics_url = json_data['response']['hits'][0]['result']['url']
        is_lyrics_available = ''

    return flask.render_template('index.html',
                                 username=current_user.username,
                                 playlist_image=playlist_image,
                                 playlist_name=playlist_name,
                                 playlist_description=playlist_description,
                                 preview_url=preview_url,
                                 track_image=track_image,
                                 track_name=track_name,
                                 artist_name=artist_name,
                                 lyrics=lyrics_url,
                                 is_lyrics_available=is_lyrics_available,
                                 info=info)


app.secret_key = "ThereAreNoSecrets"


app.run(
    debug=True,
    port=int(os.getenv("PORT", "8080")),
    host=os.getenv("IP", "0.0.0.0"))
