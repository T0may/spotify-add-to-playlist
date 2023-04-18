from bs4 import BeautifulSoup
import requests
import pandas as pd

import spotipy
from spotipy.oauth2 import SpotifyOAuth

details = pd.read_csv("details.txt", sep=",", header=None)
client_id = details[0][0]
client_secret = details[0][1]
artist = details[0][2]
artist_url = details[0][2].replace(" ", "%20")

SPOTIPY_CLIENT_ID = client_id
SPOTIPY_CLIENT_SECRET= client_secret

sp = spotipy.Spotify(
    auth_manager= SpotifyOAuth(
        client_id=SPOTIPY_CLIENT_ID,
        client_secret=SPOTIPY_CLIENT_SECRET,
        redirect_uri="http://example.com/",
        scope= "playlist-modify-private",
        cache_path="token.txt",
        show_dialog=True,
    )
)



user_id = sp.current_user()["id"]

response = requests.get(f"https://www.top50songs.info/artist.php?artist={artist_url}&v=70885014")
response.raise_for_status()

data = response.text

soup = BeautifulSoup(data, "html.parser")

titles = soup.select("div li a")

title_list = []
for el in titles:
    title_list.append(el.get("title"))

#creating a private playlist
playlist_title = f"{artist} - Top 50"
uri_list = []
for song in title_list:
    # print(song)
    result = sp.search(q = f"track:{song} {artist}", type="track")
    try:
        uri = result["tracks"]["items"][0]["uri"]
        uri_list.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in shopify")

playlist = sp.user_playlist_create(user_id, playlist_title, public = False)
playlist_id = playlist["id"]

# Adding into a playlist
sp.playlist_add_items(playlist_id, uri_list)


