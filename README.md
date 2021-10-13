Listen to my personal playlists at any time. Fetches randomly one playlist among my 3 playlists and randomly selects a song. Lyrics link will be avaliable from genius API.

To run the project clone it into local directory create a .env file containing below mentioned parameters

client_id -> client id from spotify
client_secret -> client secret from spotify
genius_access_token -> from genius developer api
once all of these are valid, you can start the project by executing python main.py command

Integrated with heroku. https://se-project-skolli1.herokuapp.com/

What are at least 3 technical issues you encountered with your project? How did you fix them?

Heroku deployment - fixed that by creating a pipeline. with the help of stackoverflow, there was a space missing in Procfile, that is fixed.
Understanding Spotify API Responses - Used JSON formatter where i can close the unnecessary json parts
fetching Lyrics links - from the help of internet, i used URL insted of module, to search for song lyrics and linked the same.
What are known problems (still existing), if any, with your project?

Sometimes, to some songs (especially for some anime openings), there is no proper lyrics, so genius api isnt returning correct api.

What would you do to improve your project in the future?

I could give the user to select from list of my playlists and show them the songs and ability to play the desired song.