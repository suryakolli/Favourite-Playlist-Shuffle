Signup to save your favourite playlists. Login anytime and listen to awesome shuffle from your favourite playlists.

To run the project clone it into local directory create a .env file containing below mentioned parameters

client_id -> client id from spotify

client_secret -> client secret from spotify

genius_access_token -> from genius developer api

PORT -> 5000 (default)

SQLALCHEMY_DATABASE_URI -> URL for database

once all of these are valid, you can start the project by executing ```python main.py``` command

Integrated with heroku. https://project2-skolli1.herokuapp.com/login

What are at least 3 technical issues you encountered with your project? How did you fix them?

Heroku deployment - fixed that by creating a pipeline. with the help of stackoverflow, there was a space missing in Procfile, that is fixed.
Understanding Spotify API Responses - Used JSON formatter where i can close the unnecessary json parts
fetching Lyrics links - from the help of internet, i used URL insted of module, to search for song lyrics and linked the same.

---

What are known problems (still existing), if any, with your project?

Sometimes, to some songs (especially for some anime openings), there is no proper lyrics, so genius api isnt returning correct api.

---

What would you do to improve your project in the future?

I could give the search user feature, so that we can list all playlists of the user and then we can save the playlist.

---

Improvements:
1. Adding password auth
    - add another field with password as name and hash it to store in db. everytime request comes for login, we can hash the given password to compare it with hashed password and give access.
2. Logout functionality
   - can implement logout by adding a logout button and clear session in backend whenever logout happens. by doing this, we can control number of active logged in sessions.
3. Listing playlists instead of taking ID
   - Instead of taking id in search box, we can take usernames, and list playlists of that user. and then select the favourite playlist among them.

---

Problems Solved:
1. Added a form from which we can take id of playlist and add it into saved playlist of logged in user.
    - used HTML forms to take input and process it with flask forms.
2. Implemented Login 
   - used forms to take username and send it to database to store it as a record.