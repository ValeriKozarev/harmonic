from rich.console import Console
from rich.table import Table

tier_styles = {
    "Perfect Match": "green",
    "Workable": "yellow",
    "Ok": "orange3"
}

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