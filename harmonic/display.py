from rich.console import Console
from rich.table import Table

tier_styles = {
    "Perfect Match": "green",
    "Workable": "yellow",
    "Ok": "orange3"
}

# TODO: add disclaimer that data might be incorrect as we aren't using Spotify for all our data

def generate_results_table(results, title):
    table = Table(title=title) # TODO: might be worth making this a bit more robust based on the query we are answering

    table.add_column("Track", justify="center")
    table.add_column("Artist", justify="center")
    table.add_column("BPM", justify="center")
    table.add_column("Camelot", justify="center")
    table.add_column("Tier", justify="center")

    if not results:
        console = Console()
        console.print()
        console.print("No matching tracks found.")
        return

    for result_row in results:
        row_style = tier_styles.get(result_row["tier"], "white")
        table.add_row(result_row["name"], result_row["artist_name"], str(result_row["bpm"]), result_row["camelot_key"], result_row["tier"], style=row_style)

    # TODO: we probably want to cap how many entries the table will show? how helpful is a 50+ line output?

    console = Console()
    console.print() # adding a blank line to make things a bit cleaner
    console.print(table)

def show_playlist_picker(playlists):
    console = Console()

    for idx, playlist in enumerate(playlists, start=1):
        console.print(f"{idx}. {playlist['name']} ({playlist['track_count']} tracks)")

def write_setlist_to_file(tracks, playlist_name):
    filename = playlist_name.strip().lower().replace(" ", "_") + "_setlist.txt"
    # TODO: look into tracks getting dropped in the merge_tracks_data function
    with open(filename, 'w') as f:
        f.write(f"{playlist_name}\n\n")
        f.write(f"{'Track':<40} {'Artist':<25} {'BPM':<6} {'Key'}\n")
        f.write("-" * 80 + "\n")
        for track in tracks:
            f.write(f"{_truncate(track['name'], 40):<40} {_truncate(track['artist_name'], 25):<25} {track['bpm']:<6} {track['camelot_key']}\n")

    return filename

def _truncate(text, width):
    return text if len(text) <= width else text[:width-3] + "..."