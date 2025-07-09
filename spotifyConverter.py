import re
import time
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
load_dotenv()

import os
CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')
REDIRECT_URI = os.getenv('SPOTIFY_REDIRECT_URI')

# CLIENT_ID = 'put_your_client_id'
# CLIENT_SECRET = 'put_your_client_secret'
# REDIRECT_URI = 'http://127.0.0.1:8888/callback'
SCOPE = 'playlist-modify-public'

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    scope=SCOPE
))

def clean_text(text):
    return re.sub(r'[♥♫♪]+', '', text).strip()

def is_skippable(line):
    skip_keywords = ['intro', 'outro', 'replay']
    line_lower = line.lower()
    return any(keyword in line_lower for keyword in skip_keywords)

def extract_songs_from_text(raw_text):
    """
    Extract songs from a raw text with timestamps, different formats.
    Supports:
    - timestamps like 0:00, 00:00:01, etc.
    - lines with 'by Artist' or 'Artist - Title' or just 'Title'
    - ignores skippable lines
    """
    pattern = re.compile(
       r'^\s*\d{1,2}:\d{2}(?::\d{2})?\.?\s*["“]?(.+?)["”]?\s*(?:by\s+(.+))?$',
        re.IGNORECASE
    )

    songs = []
    for line in raw_text.splitlines():
        line = clean_text(line)
        if is_skippable(line):
            continue

        match = pattern.match(line)
        if match:
            title = match.group(1).strip()
            artist = match.group(2).strip() if match.group(2) else None
            if artist:
                song_str = f"{artist} - {title}"
            # When lines are 'Artist = Title' without 'by'
            # Try to detect if a dash exist and split accrodingly:
            elif ' - ' in title:
                parts = title.split(' - ', 1)
                song_str = f"{parts[0].strip()} - {parts[1].strip()}"
            else:
                song_str = title
            songs.append(song_str)
    
        # If line doesn't match pattern, try 'Artist - Title' fallback
        elif ' - 'in line:
            parts = line.split(' - ', 1)
            parts_str = f"{parts[0].strip()} - {parts[1].strip()}"
            songs.append(parts_str)
        else:
            # If just a title, accept it.
            songs.append(line)
    return songs

def main():
    input_file = "raw_playlist4.txt"
    with open(input_file, 'r', encoding='utf-8') as f:
        raw_text = f.read()
    
    songs = extract_songs_from_text(raw_text)
    print(f"Extracted {len(songs)} songs.")

    user_id = sp.me()['id']
    playlist = sp.user_playlist_create(user_id, name="good vibe pop songs", public = True)
    playlist_id = playlist['id']
    print(f"Created Playlist: {playlist['external_urls']['spotify']}")

    not_found = []

    for song in songs:
        query = song.replace('–', '-').strip()  # normalize dash to hyphen for search
        result = sp.search(q=query, type='track', limit=1)
        tracks = result['tracks']['items']

        if tracks:
            track_id = tracks[0]['id']
            sp.playlist_add_items(playlist_id=playlist_id, items=[track_id])
            print(f"Added: {song}")
        else:
            not_found.append(song)
            print(f"Not found: {song}")
        time.sleep(0.2)
    if not_found:
        print("\nSongs not found on Spotify:")
        for nf in not_found:
            print(" -", nf)
    
if __name__ == "__main__":
    main()