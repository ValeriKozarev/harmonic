from harmonic.auth import get_spotify_client
from harmonic.api import get_all_artist_tracks, get_track_details, get_matching_playlists, get_all_playlist_tracks
from harmonic.matching import rank_tracks
from harmonic.display import generate_results_table, show_playlist_picker
from rich.console import Console
import typer
import json


app = typer.Typer()

# using Typer to work with CLI commands more easily
@app.command()
def recommend(
    bpm: int = typer.Option(..., help="Target BPM"),
    key: str = typer.Option(..., help="Target Camelot Key"),
    artist: str = typer.Option(None, help="Filter by Artist Name"),
    playlist: str = typer.Option(None, help="Filter by Playlist Name")
):
    if not artist and not playlist:
        typer.echo("Please provide either an artist or a playlist.")
        raise typer.Exit()

    if artist and playlist:
        typer.echo("Please provide only one of artist or playlist, not both.")
        raise typer.Exit()
    
    console = Console()
    ranked = []

    # TODO: gracefully handle other errors like rate limits etc. and propagate those up
    # TODO: maybe also add some more loading indicators?

    if artist:
        with console.status("Initializing..."):
            sp = get_spotify_client()
            tracks = get_all_artist_tracks(sp, artist)

            if not tracks:
                typer.echo()
                typer.echo(f"No tracks found for artist: {artist}")
                raise typer.Exit()

        with console.status("Analyzing tracks..."):
            details = get_track_details(tracks)
            ranked = rank_tracks(details, bpm, key)
    
    elif playlist:
        with console.status("Initializing..."):
            sp = get_spotify_client()
            playlists = get_matching_playlists(sp, playlist)
            if not playlists:
                typer.echo()
                typer.echo(f"No playlists found for name: {playlist}")
                raise typer.Exit()
        
        show_playlist_picker(playlists)

        try:
            selection = int(typer.prompt("Select a playlist (enter number)")) - 1
        except ValueError:
            typer.echo("Please enter a valid number.")
            raise typer.Exit()

        if selection < 0 or selection >= len(playlists):
            typer.echo("Invalid selection.")
            raise typer.Exit()

        selected_playlist = playlists[selection]

        with console.status("Analyzing tracks..."):
            tracks = get_all_playlist_tracks(sp, selected_playlist["id"])
            details = get_track_details(tracks)
            ranked = rank_tracks(details, bpm, key)


    title = "Artist Track Recommendations" if artist else "Playlist Track Recommendations"
    generate_results_table(ranked, title)

    # TODO: it would be cool to show a stat of how many tracks were analyzed

@app.command()
def dummy_command():
    # TODO: future expansion goes here
    pass

if __name__ == "__main__":
    app()