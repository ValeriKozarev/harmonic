from rich.console import Console
from rich.table import Table
import typer

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

    for result_row in results[:20]:
        row_style = tier_styles.get(result_row["tier"], "white")
        table.add_row(result_row["name"], result_row["artist_name"], str(result_row["bpm"]), result_row["camelot_key"], result_row["tier"], style=row_style)

    console = Console()
    console.print() # adding a blank line to make things a bit cleaner
    console.print(table)

# display a numbered list of options for the user to select from to disambiguate (e.g. playlists, artists, etc.)
def show_option_picker(options, query=None):
    console = Console()

    # if there is only one option, just select it and move on instead of asking the user to confirm
    if len(options) == 1:
        console.print()
        console.print(f"Only one option found, selecting \"{options[0]}\" automatically.")
        return 0
    
    # if there's an exact match, select that automatically as well
    if query:
        for idx, option in enumerate(options):
            if option.strip().lower() == query.strip().lower():
                console.print()
                console.print(f"Exact match found for \"{query}\", selecting \"{option}\" automatically.")
                return idx

    # otherwise we want to ask them to confirm which one they meant
    for idx, option in enumerate(options, start=1):
        console.print(f"{idx}. {option}")
    
    try:
        selection = int(typer.prompt("Select an option (enter number)")) - 1
    except ValueError:
        typer.echo("Please enter a valid number.")
        raise typer.Exit()

    if selection < 0 or selection >= len(options):
        typer.echo("Invalid selection.")
        raise typer.Exit()
    
    # TODO: add option to try again if no match

    return selection


# exports the setlist and associated track metadata to a text file in the current directory
def write_setlist_to_file(tracks, playlist_name):
    filename = playlist_name.strip().lower().replace(" ", "_") + "_setlist.txt"
    with open(filename, 'w') as f:
        f.write(f"{playlist_name}\n\n")
        f.write(f"{'Track':<40} {'Artist':<25} {'BPM':<6} {'Key'}\n")
        f.write("-" * 80 + "\n")
        for track in tracks:
            bpm = track['bpm'] if track['bpm'] != -1 else '???'
            camelot_key = track['camelot_key'] if track['camelot_key'] != 'X' else '???'
            f.write(f"{_truncate(track['name'], 40):<40}")
            f.write(f"{_truncate(track['artist_name'], 25):<25}") 
            f.write(f"{bpm:<6}")
            f.write(f"{camelot_key}\n")

    return filename

# helper for writing to text file, just shortens long strings
def _truncate(text, width):
    return text if len(text) <= width else text[:width-3] + "..."