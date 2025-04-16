import os
import pandas as pd
import seaborn as sns
from dotenv import load_dotenv
import matplotlib.pyplot as plt
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Load .env file variables
load_dotenv()

# Get credentials
client_id = os.environ.get("CLIENT_ID")
client_secret = os.environ.get("CLIENT_SECRET")

# Authenticate with Spotify
spotify = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id = client_id, client_secret = client_secret))

# Birdy's Spotify URI
birdy_uri = 'spotify:artist:4q3ewBCX7sLwd24euuV69X'

# Fetch albums
results = spotify.artist_albums(birdy_uri, album_type='album')
albums = results['items']
while results['next']:
    results = spotify.next(results)
    albums.extend(results['items'])

# Transform to DataFrame
albums_data = [{
    'name': album['name'],
    'release_date': album['release_date'],
    'total_tracks': album['total_tracks'],
    'id': album['id']
} for album in albums]

df_albums = pd.DataFrame(albums_data)

# Convert release_date to datetime
df_albums['release_date'] = pd.to_datetime(df_albums['release_date'], errors='coerce')

# Sort by release_date
df_albums.sort_values('release_date', inplace=True)

# Plot total tracks over time
plt.figure(figsize=(10, 5))
sns.lineplot(data=df_albums, x='release_date', y='total_tracks', marker='o')
plt.title('Total Tracks per Album Over Time')
plt.xlabel('Release Date')
plt.ylabel('Total Tracks')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Show basic stats
print(df_albums['total_tracks'].describe())
