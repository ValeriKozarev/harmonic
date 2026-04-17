# harmonic

A CLI tool for DJs to find compatible tracks using the Spotify API. Given a BPM and Camelot key (or a source track), harmonic searches an artist's catalog or your Spotify playlists and returns ranked recommendations for your next mix.

---

## The Problem

When building or performing a DJ set, finding a good transition means finding a song that matches (or intentionally contrasts) the current track's key, tempo, and energy. Doing this manually — opening Spotify, cross-referencing a Camelot wheel, scanning an artist's catalog — is tedious. Harmonic automates it.

---

## Usage

### Recommend by artist catalog
```
python3 main.py recommend --bpm 123 --key 10B --artist "Disclosure"
```

### Recommend by Spotify playlist
```
python3 main.py recommend --bpm 123 --key 10B --playlist "moshi"
```
Searches your Spotify library for matching playlists, lets you pick one, then finds compatible tracks within it.

Results are color-coded by compatibility tier:
- **Green** — Perfect Match (±5 BPM, ±2 Camelot)
- **Yellow** — Workable (±10 BPM, ±3 Camelot)
- **Orange** — Ok (±15 BPM, ±4 Camelot)

Results are sorted by tier first, then by proximity to your target values within each tier.

---

## How It Works

1. **Spotify** — searches the artist's catalog or your playlists and retrieves track metadata
2. **ReccoBeats** — fetches BPM, key, and audio features for each track (batched in chunks of 40)
3. **Camelot wheel logic** — calculates harmonic compatibility using circular distance on a 12-point wheel
4. **Rich** — displays results as a formatted, color-coded terminal table

> Note: Spotify deprecated their audio features endpoint for new apps in November 2024. ReccoBeats is used as a free alternative with comparable accuracy.

---

## Setup

### 1. Clone and create a virtual environment

```bash
git clone https://github.com/yourusername/harmonic.git
cd harmonic
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Spotify API credentials

Create an app at [developer.spotify.com/dashboard](https://developer.spotify.com/dashboard) with redirect URI `http://127.0.0.1:8888/callback`.

### 3. Configure `.env`

```
SPOTIFY_CLIENT_ID=your_client_id
SPOTIFY_CLIENT_SECRET=your_client_secret
SPOTIFY_REDIRECT_URI=http://127.0.0.1:8888/callback
```

On first run, a browser window will open for Spotify OAuth. After that, the token is cached and login is silent.

---

## Tech Stack

| Library | Purpose |
|---|---|
| `spotipy` | Spotify API wrapper, handles OAuth |
| `requests` | HTTP calls to ReccoBeats API |
| `typer` | CLI interface |
| `rich` | Terminal tables and formatted output |
| `python-dotenv` | Credentials management |

---

## Known Limitations

- No broad discovery — an artist name or playlist is required as a candidate pool
- ReccoBeats is a free, unattributed service with no SLA — local caching coming in a future release
