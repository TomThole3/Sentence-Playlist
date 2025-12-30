# Sentence Playlist

This project is a python application that creates a Spotify Playlist based on a user's input sentence. It will match every (set of) word(s) in the sentence to a song with the associated title, falling back to shorter phrases if necessary. The Spotify Web API, SQLite3 and OAuth2 are used to achieve this functionality.

If the concept is still vague, the following playlist provides a practical example and the reason why this project exists in the first place (:
https://open.spotify.com/playlist/1CjvjBZEUxQV20eVuwitXS

## Requirements:
Python 3.10+
Spotify Account
Spotify Developer Credentials

For more information on how to set up the necessary Spotify Credentials and app etc., I recommend following the tutorial provided by Spotify:
https://developer.spotify.com/documentation/web-api


## Explanation of example files
To run the script, a preconstructed .env and token.json file are required. The .env file has the following attributes, see also the .env.example file.
'SPOTIFY_ENCODED_CREDENTIALS=base64(client_id:client_secret)
SPOTIFY_REFRESH_TOKEN=your_refresh_token
SPOTIFY_USER_ID=your_spotify_user_id'

The token.json file has the following attributes, see also token.json.example
'{
 "access_token": (spotify access token),
 "token_type": "Bearer", 
 "expires_in": 3600, 
 "refresh_token": (spotify refresh token), 
 "scope": "playlist-modify-public", 
 "expires_at": (in absolute time)
}'

 ## Running the script
 The file is run from main.py. The user will be prompted for the title of the playlist, the sentence which the playlist will contain and the maximum number of words in one song. The latter is recommended to be a high number for more flexibility, although this results in longer execution times. 
 If a song is not found, the user is asked to either replace the word with a different word, exit the program or provide a valid url for the song. The url can be copied directly from Spotify's share button, the program automatically converts such urls to song ids. 

 ## How it works (High level)
 - A valid token is acquired
 - User is prompted for input
 - The input sentence is split into words
 - The app attempts to resolve the longest possible phrase first
 - If no match is found, it retries with shorter phrases
 - Resolved tracks are cached in a local SQLite database
 - A new Spotify playlist is created and populated with the tracks

 ## Limitations
 The project has several limitations. Firstly, the Spotify Search API does not always return a song with an exact title match, even if it exists. This can be circumvented by manually adding the song, but this takes time. Secondly, the database cannot be edited and may become corrupt if songs are deleted from spotify. Thirdly, the program has no GUI and details can only be entered through the console or CLI based. Finally, the project was coded without the use of git, and thus no intermediate versions can be shown.