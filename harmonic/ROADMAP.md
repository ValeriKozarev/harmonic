# Harmonic — Roadmap

## MVP (current focus)

### recommend command
Find compatible tracks for mixing based on BPM and Camelot key proximity.

**Candidate pool options (one required):**
- `--artist "Artist Name"` — search within that artist's Spotify catalog
- `--playlist` — pick from the user's Spotify playlists

**Input options:**
- `--bpm` and `--key` — provide values directly (key in Camelot notation, e.g. 10B)
- `--track "Song Name"` — auto-fetch BPM and key from a named track (with disambiguation)

**Ranking rules:**
- Perfect match: within ±5 BPM and ±2 Camelot positions
- Looser match: within ±10 BPM and ±3 Camelot positions
- Results sorted by proximity to input values, closest first
- Future enhancement: incorporate other audio features (energy, danceability) into ranking

**Examples:**
```
harmonic recommend --bpm 123 --key 10B --artist "Disclosure"
harmonic recommend --bpm 123 --key 10B --playlist
harmonic recommend --track "One More Time" --artist "Disclosure"
harmonic recommend --track "One More Time" --playlist
```

---

## Future: set command

Propose a running order for a full DJ set from a Spotify playlist.

- User provides a playlist and one or more starting tracks
- Tool proposes an order for the remaining tracks using harmonic compatibility logic
- Intentional randomness in the output so repeated runs produce different but musically valid suggestions — useful for stimulating creativity
- The Camelot chain logic built for `recommend` is the foundation for this feature

**Example:**
```
harmonic set --playlist --start "One More Time"
```

---

## Future: local track database

Cache all fetched track data in a local SQLite database so the app builds up a personal knowledge base over time.

- Every track looked up via ReccoBeats gets stored locally (Spotify ID, name, artist, BPM, key, Camelot, full audio features)
- On subsequent lookups, check the local cache first before hitting the API — faster and resilient to API changes
- If ReccoBeats ever goes away, the locally cached data remains usable
- Could eventually support `harmonic stats` or similar commands to explore your personal track database

Implementation: `sqlite3` from Python stdlib, no extra dependencies needed. A new `db.py` module in the package.

---

## Known constraints
- Spotify audio features, audio analysis, and recommendations endpoints are restricted for new developer apps (since Nov 2024) — audio data sourced from ReccoBeats instead
- No-artist / no-playlist broad discovery not supported in MVP (requires a candidate pool)
