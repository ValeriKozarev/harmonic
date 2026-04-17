from harmonic.auth import get_spotify_client
from harmonic.api import get_all_artist_tracks, get_track_details
from harmonic.matching import rank_tracks
from harmonic.display import generate_results_table
from rich.console import Console
import typer
import json


app = typer.Typer()

# using Typer to work with CLI commands more easily
@app.command()
def recommend(
    bpm: int = typer.Option(..., help="Target BPM"),
    key: str = typer.Option(..., help="Target Camelot Key"),
    artist: str = typer.Option(None, help="Filter by Artist Name") # TODO: we'll want to make artist name optional and add other commands for other workflows later
):
    console = Console()
    with console.status("Analyzing tracks..."):
        sp = get_spotify_client()
        tracks = get_all_artist_tracks(sp, artist)
        details = get_track_details(tracks)
        ranked = rank_tracks(details, bpm, key)

    generate_results_table(ranked, f"{artist} Track Recommendations")

@app.command()
def analyze():
    pass

if __name__ == "__main__":
    app()