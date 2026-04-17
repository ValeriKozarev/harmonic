# Harmonic — Roadmap

## Completed

- `auth.py` — Spotify OAuth with token caching, `playlist-read-private` scope
- `api.py` — full data pipeline: Spotify search → ReccoBeats ID mapping (batched in chunks of 40) → audio features fetch → track data merging with ISRC deduplication
- `api.py` — artist catalog fetch with full pagination (albums + tracks)
- `api.py` — playlist search with full pagination across user's full library
- `api.py` — playlist track fetch with full pagination
- `matching.py` — Camelot lookup table, `to_camelot()` conversion, circular Camelot distance, `rank_tracks()` with tiered scoring sorted by tier then proximity
- `display.py` — color-coded rich terminal table (green/yellow/orange by tier), empty results handling
- `main.py` — `recommend` command with both `--artist` and `--playlist` flows, loading spinner, input validation, empty results guards, selection validation with try/except

**Working commands:**
```
python3 main.py recommend --bpm 123 --key 10B --artist "Disclosure"
python3 main.py recommend --bpm 123 --key 10B --playlist "chill hosting"
```
---

## In Progress / TODOs

### `recommend` command — remaining flows
- disambiguating between artists with common names
- `--track "Song Name"` input: disambiguate track, auto-fetch BPM and key, then run recommendation flow (works with both `--artist` and `--playlist`)

### Display
- Table title could be more descriptive — include BPM and key used in the query
- Consider capping table output (50+ rows is unwieldy)
- Listing how many tracks got analyzed could be cool
- More graceful error handling

### Robustness
- Playlist search could be smarter about exact vs. partial matches and auto-selecting in these cases

---

## Future: set command

Propose a running order for a full DJ set from a Spotify playlist.

- User provides a playlist and one or more starting tracks
- Tool proposes an order for the remaining tracks using harmonic compatibility logic
- Intentional randomness so repeated runs produce different but musically valid suggestions
- Built on top of the same Camelot chain logic as `recommend`

**Example:**
```
harmonic set --playlist --start "One More Time"
```

---

## Future: local track database

Cache all fetched track data in a local SQLite database so the app builds up a personal knowledge base over time.

- Every track looked up via ReccoBeats gets stored locally (Spotify ID, name, artist, BPM, key, Camelot, full audio features)
- On subsequent lookups, check local cache first — faster and resilient to API changes
- If ReccoBeats ever goes away, cached data remains usable
- Could eventually support `harmonic stats` or similar commands

Implementation: `sqlite3` from Python stdlib. A new `db.py` module in the package.

---

## Known Constraints
- Spotify audio features, audio analysis, and recommendations endpoints are restricted for new developer apps (since Nov 2024) — audio data sourced from ReccoBeats instead
- No broad discovery without a candidate pool (artist or playlist required)
