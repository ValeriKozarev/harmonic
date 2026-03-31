# harmonic

A CLI tool for DJs to find compatible tracks using the Spotify API. Given a song, harmonic helps you find what to play next — searching an artist's catalog for tracks that match by key, BPM, and energy.

---

## The Problem

When building or performing a DJ set, finding a good transition means finding a song that matches (or intentionally contrasts) the current track's key, tempo, and energy. Doing this manually — opening Spotify, cross-referencing a Camelot wheel, scanning an artist's catalog — is tedious. Harmonic automates it.

---

## Planned Features

### Song Lookup
Look up any track's musical characteristics, displayed in DJ-friendly format (Camelot key notation, not raw music theory).

```
$ harmonic lookup "One More Time" --artist "Daft Punk"

  One More Time — Daft Punk
  BPM:     123
  Key:     8B (C major)
  Energy:  0.84
  Vibe:    Dance / High energy
```

### Artist Catalog Match
Given a song, search an artist's full catalog and return ranked results by compatibility — harmonic key relationships first, then BPM proximity, then energy similarity.

```
$ harmonic match "One More Time" --artist "Disclosure"

  Compatible tracks from Disclosure's catalog:

  PERFECT MATCH
  ┌─────────────────────────────┬──────┬──────┬────────┐
  │ Track                       │ BPM  │ Key  │ Energy │
  ├─────────────────────────────┼──────┼──────┼────────┤
  │ Latch                       │ 121  │ 8A   │ 0.79   │
  │ White Noise                 │ 124  │ 9B   │ 0.88   │
  └─────────────────────────────┴──────┴──────┴────────┘

  WORKABLE
  │ You & Me                    │ 120  │ 7B   │ 0.71   │
```

### Catalog Browse
Browse any artist's catalog with explicit filters — useful when you already know what you're looking for.

```
$ harmonic browse "Bicep" --bpm 125-132 --key 4A
```

---

## Compatibility Logic

Compatibility is based on the **Camelot Wheel** — the DJ standard for harmonic mixing. A track is considered:

- **Perfect match** — same Camelot key, BPM within ±3%
- **Harmonic match** — adjacent key on the wheel (±1), or relative major/minor swap (8A ↔ 8B), BPM within ±5%
- **Workable** — compatible key, BPM close enough to beatmatch

BPM compatibility also accounts for half/double time (e.g. 75 BPM can work over 150 BPM).

---

## What Spotify Gives Us

The Spotify audio features endpoint returns everything we need:

| Field | Description |
|---|---|
| `tempo` | BPM |
| `key` | Integer 0–11 (C through B) |
| `mode` | 0 = minor, 1 = major |
| `energy` | 0.0–1.0, intensity/loudness feel |
| `danceability` | 0.0–1.0 |
| `valence` | 0.0–1.0, musical "positivity" |

`key` + `mode` together map to Camelot notation, which is where the compatibility logic lives.

---

## Tech Stack

| Library | Purpose |
|---|---|
| `spotipy` | Spotify API wrapper, handles OAuth |
| `typer` | CLI interface |
| `rich` | Terminal tables and formatted output |
| `python-dotenv` | Spotify API credentials management |

---

## Potential Future Features

- Match against your own Spotify playlists (not just an artist's catalog)
- Export a shortlist directly to a new Spotify playlist
- Transition path finder — given song A and song B, find a middle track that bridges them
- Energy arc planning for a full set

---

## Setup (TBD)

Spotify API credentials will be required. Setup instructions to be added once the initial implementation is complete.
