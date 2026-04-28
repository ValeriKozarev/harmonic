from harmonic.auth import get_spotify_client
from harmonic.api import get_artists, get_all_artist_tracks, get_track_details, get_matching_playlists, get_all_playlist_tracks
from harmonic.matching import rank_tracks
from harmonic.display import generate_results_table, show_option_picker, write_setlist_to_file
from rich.console import Console
import typer

app = typer.Typer()

# TODO: it would be nice to cleanup/improve the console statuses, maybe showing a step is done and adding a line below for the subsequent step?

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

    if artist:
        with console.status("Initializing..."):
            sp = get_spotify_client()
            artists = get_artists(sp, artist)

        if not artists:
            typer.echo()
            typer.echo(f"No artists found for name: {artist}")
            raise typer.Exit()
        
        artist_options = [a['name'] for a in artists]
        
        selection = show_option_picker(artist_options)
        selected_artist = artists[selection]

        typer.echo()

        with console.status("Fetching tracks..."):
            tracks = get_all_artist_tracks(sp, selected_artist["id"])

        if not tracks:
            typer.echo()
            typer.echo(f"No tracks found for artist: {artist}")
            raise typer.Exit()
        
        typer.echo()

        with console.status("Analyzing tracks..."):
            details = get_track_details(tracks)

        with console.status("Ranking tracks..."):
            ranked = rank_tracks(details, bpm, key)
    
    elif playlist:
        with console.status("Initializing..."):
            sp = get_spotify_client()
            playlists = get_matching_playlists(sp, playlist)
            if not playlists:
                typer.echo()
                typer.echo(f"No playlists found for name: {playlist}")
                raise typer.Exit()
        
        options = [p['name'] for p in playlists]
        selection = show_option_picker(options)

        selected_playlist = playlists[selection]
        typer.echo()

        with console.status("Analyzing tracks..."):
            tracks = get_all_playlist_tracks(sp, selected_playlist["id"])
            details = get_track_details(tracks)

        with console.status("Ranking tracks..."):
            ranked = rank_tracks(details, bpm, key)


    title = "Artist Track Recommendations" if artist else "Playlist Track Recommendations"
    generate_results_table(ranked, title)

    # TODO: it would be cool to show a stat of how many tracks were analyzed

@app.command()
def export(playlist: str = typer.Option(None, help="Export setlist from a specific playlist")):
    if not playlist:
        typer.echo("Please provide a playlist.")
        raise typer.Exit()
    
    console = Console()
    
    with console.status("Initializing..."):
        sp = get_spotify_client()
        playlists = get_matching_playlists(sp, playlist)
        if not playlists:
            typer.echo()
            typer.echo(f"No playlists found for name: {playlist}")
            raise typer.Exit()
    
    options = [p['name'] for p in playlists]
    selection = show_option_picker(options)

    selected_playlist = playlists[selection]
    typer.echo()

    with console.status("Analyzing tracks..."):
        tracks = get_all_playlist_tracks(sp, selected_playlist["id"])
        details = get_track_details(tracks)

    with console.status("Exporting setlist..."):
        filename = write_setlist_to_file(details, selected_playlist['name'])
        typer.echo()
        typer.echo(f"Setlist exported to {filename}")

@app.callback()
def disclaimer():
    typer.echo("Disclaimer: The recommendations provided by this tool are based on data from Spotify and other 3rd party APIs, and may not always be accurate. Consider double-checking any information received from this tool, and have fun!")
    typer.echo()

if __name__ == "__main__":
    app()