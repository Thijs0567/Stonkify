from tkinter import ttk
import customtkinter as ctk
import tkinter as tk
import os
import utils


def populate_treeview(tree, playlist_data):
    # Clear existing items in the Treeview
    tree.delete(*tree.get_children())

    # Loop through each entry in the playlist data
    for entry in playlist_data:
        # Extract information from the entry
        song_id = entry['id']
        song_name = entry['name']
        artists = ", ".join(entry['artists'])
        album = entry['album']
        release_date = entry['release_date']
        duration = entry['duration_ms']
        popularity = entry['popularity']
        danceability = entry['danceability']
        energy = entry['energy']
        key = entry['key']
        loudness = entry['loudness']
        mode = entry['mode']
        speechiness = entry['speechiness']
        acousticness = entry['acousticness']
        instrumentalness = entry['instrumentalness']
        liveness = entry['liveness']
        valence = entry['valence']
        tempo = entry['tempo']

        # Insert the information into the Treeview
        tree.insert('', 'end', values=(song_name, artists, album, release_date, duration, popularity, song_id, danceability, energy, key, loudness, mode, speechiness, acousticness, instrumentalness, liveness, valence, tempo))

def create_treeview(overview_frame):
    global tree
    tree = ttk.Treeview(overview_frame)
    tree['columns'] = ('Name', 'Artists', 'Album', 'Release Date', 'Duration', 'Popularity', 'Spotify ID', 'danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo')
    # DIRTY FIX: Hide the first column (tree column)
    tree.column("#0", width=0)

    # Configure column headings
    for col in tree['columns']:
        tree.heading(col, text=col)

    # Configure Treeview to display only 10 songs at a time
    vsb = ttk.Scrollbar(overview_frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=vsb.set)
    vsb.grid(row=2, column=2, sticky="ns")
    tree.grid(row=2, column=0, columnspan=3, pady=(50, 0), padx=10, sticky="nsew")

     # Add horizontal scrollbar
    hsb = ttk.Scrollbar(overview_frame, orient="horizontal", command=tree.xview)
    tree.configure(xscrollcommand=hsb.set)
    hsb.grid(row=3, column=0, columnspan=3, padx=10, sticky="ew")

    # After creating the treeview widget:
    setup_treeview_sorting(tree)

    #Populate tree with previous data if available:
    # Check if the file exists and then populate the treeview
    jsonfile = 'playlist_data.json'
    if os.path.exists(os.path.join("resources/playlists", jsonfile)):
        playlist_data = utils.load_playlist_data(jsonfile)
        populate_treeview(tree, playlist_data)
    else:
        print("Failed to populate")
    return tree

def setup_treeview_sorting(tree):
    # Bind the sorting function to column headers
    for col_id in tree['columns']:
        tree.heading(col_id, text=col_id, command=lambda _col=col_id: sort_treeview_column(tree, _col))

def sort_treeview_column(tree, col_id):

    # Get the current sorting state of the column
    current_state = tree.heading(col_id, option="text")

    # Reset sorting indicators in all columns
    for col in tree['columns']:
        if col != col_id:  # Skip the current column
            tree.heading(col, text=col)

    # Check if the column is already sorted in ascending order
    if current_state == f"{col_id} ▲":
        # If yes, sort in descending order
        tree.heading(col_id, text=f"{col_id} ▼")
        reverse = True
    else:
        # Otherwise, sort in ascending order
        tree.heading(col_id, text=f"{col_id} ▲")
        reverse = False

    # Get all items in the treeview
    items = [(tree.set(item, col_id), item) for item in tree.get_children('')]

    # Sort the items based on the column values
    if col_id in ('Duration', 'Popularity', 'loudness', 'key', 'tempo'):  # Check if the column contains numeric data
        items.sort(key=lambda x: float(x[0]), reverse=reverse)  # Convert values to float for numeric sorting
    else:
        items.sort(reverse=reverse)

    # Rearrange items in the treeview based on the sorted order
    for index, (val, item) in enumerate(items):
        tree.move(item, '', index)
