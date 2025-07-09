This Python script extracts song titles and artists from raw text files (such as Youtube playlist descriptions or timestamps) 
and creates a Spotify playlist by searching and adding those songs automatically.

Features
- Parses various timestamped song list formats, including different edge cases like missing artist names or extra symbols.
- Cleans and normalizes song data for better search results.
- Uses Spotify API to create playlists and add tracks programmatically.
- Handles skipping intros/outros or replay tracks.

Requirements
- Python 3.6 or higher.
- Spotify library (pip install spotify)
- python-dotenv (pipi install python-dotenv)
- A Spotify Developer account with an app created (to get CLIENT_ID, CLIENT_SECRET, and SET_REDIRECT_URI)

Setup
1. Clone the repository
2. Create an activate your Python virtual environment
3. Install dependencies
4. Create a .env file in the project root and add your Spotify credentials:
  SPOTIFY_CLIENT_ID=your_client_id_here
  SPOTIFY_CLIENT_SECRET=your_client_secret_here
  SPOTIFY_REDIRECT_URI=http://127.0.0.1:8888/callback
5. Add your raw playlist text to a file like raw_playlist.txt.
   raw_playlist without artist has low accuracy.

Usage

Run the script with: python spotifyConverter.py
- It reads your raw playlist text file.
- Extract and clean song titles and artists.
- Create a new Spotify playlist on your account.
- Search and add songs to the playlist.
- Print out any songs it couldn't find.
