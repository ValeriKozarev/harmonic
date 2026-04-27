from rich.console import Console
from rich.table import Table

### This module handles all the display logic for the CLI, including results table, playlist selection, and more.

# TODO: add more configurability in the future
tier_styles = {
    "Perfect Match": "green",
    "Workable": "yellow",
    "Ok": "orange3"
}

# generate a nicely formatted Rich table for the provided result set
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

# display a numbered list of playlists for the user to select from
# TODO: add something like this for tracks and artists as those flows get built out
def show_playlist_picker(playlists):
    console = Console()

    for idx, playlist in enumerate(playlists, start=1):
        console.print(f"{idx}. {playlist['name']} ({playlist['track_count']} tracks)")

# exports the setlist and associated track metadata to a text file in the current directory
def write_setlist_to_file(tracks, playlist_name):
    filename = playlist_name.strip().lower().replace(" ", "_") + "_setlist.txt"
    with open(filename, 'w') as f:
        f.write(f"{playlist_name}\n\n")
        f.write(f"{'Track':<40} {'Artist':<25} {'BPM':<6} {'Key'}\n")
        f.write("-" * 80 + "\n")
        for track in tracks:
            f.write(f"{_truncate(track['name'], 40):<40} {_truncate(track['artist_name'], 25):<25} {track['bpm']:<6} {track['camelot_key']}\n")

    return filename

# helper for writing to text file, just shortens long strings
def _truncate(text, width):
    return text if len(text) <= width else text[:width-3] + "..."