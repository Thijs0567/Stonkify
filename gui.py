
import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
import utils
import os

class MyApplication(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.create_widgets()

    def create_widgets(self):
        # Create a notebook (tabs container) with the "clam" style
        self.notebook = ttk.Notebook(self, style="TNotebook")
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Create the Overview page
        self.create_overview_page()

        # Create the Details page
        self.create_details_page()

        # Create the Settings page
        self.create_settings_page()

    def create_overview_page(self):
        overview_frame = ctk.CTkFrame(self.notebook)
        # Add content to the Overview page

        # Create a label with centered text
        label_text = "Paste Spotify playlist link here:"
        overview_label = ctk.CTkLabel(overview_frame, text=label_text, font=('Helvetica', 16))
        overview_label.grid(row=0, column=0, pady=(10, 5), sticky="n")

        # Create an input box centered and spans 75% of the width
        input_box = ctk.CTkEntry(overview_frame, width=50) # Adjust width as needed
        input_box.insert(0, 'https://open.spotify.com/playlist/333sK6VxQ6b4iSlcD5iRWY?si=f02345d1c5fb440b')
        input_box.grid(row=1, column=0, pady=(0, 5), padx=10, sticky="ew")

        # Configure the column to make the input box span 75% of the width
        overview_frame.columnconfigure(0, weight=3)  # 75% of the width

        # Create a button
        def button_clicked():
            # Get the input from the entry widget
            link = input_box.get()

             # Extract the playlist ID from the link
            playlist_id = utils.extract_playlist_id(link)

             # Load the playlist data to a JSON:
            playlist_data = utils.load_playlist(playlist_id)

            # Populate the Treeview widget with JSON data
            utils.populate_treeview(tree, playlist_data)

            if playlist_id:
                tk.messagebox.showinfo("Success", f"Playlist ID: {playlist_id}")
            else:
                tk.messagebox.showerror("Error", "Invalid Spotify playlist link")

        button = ctk.CTkButton(overview_frame, text="Submit", command=button_clicked)
        button.grid(row=1, column=1, pady=(0, 5), padx=(0, 10), sticky="w")

        # Create a Treeview widget
        tree = ttk.Treeview(overview_frame)
        tree['columns'] = ('Name', 'Artists', 'Album', 'Release Date', 'Duration', 'Popularity', 'Spotify ID')
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

        # After creating the treeview widget:
        setup_treeview_sorting(tree)

        #Populate tree with previous data if available:
        # Check if the file exists and then populate the treeview
        jsonfile = './resources\playlist_data.json'
        if os.path.exists(jsonfile):
            playlist_data = utils.read_playlist_data_from_json(jsonfile)
            utils.populate_treeview(tree, playlist_data)

        # Add Overview page to the notebook
        self.notebook.add(overview_frame, text="Overview")


    def create_details_page(self):
        details_frame = ctk.CTkFrame(self.notebook)
        # Add content to the Details page
        details_label = ctk.CTkLabel(details_frame, text="Details Page", font=('Helvetica', 16))
        details_label.pack(pady=10)
        # Add Details page to the notebook
        self.notebook.add(details_frame, text="Details")

    def create_settings_page(self):
        settings_frame = ctk.CTkFrame(self.notebook)
        # Add content to the Settings page
        settings_label = ctk.CTkLabel(settings_frame, text="Settings Page", font=('Helvetica', 16))
        settings_label.pack(pady=10)
        # Add Settings page to the notebook
        self.notebook.add(settings_frame, text="Settings")


##### Functions:

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
    if col_id in ('Duration', 'Popularity'):  # Check if the column contains numeric data
        items.sort(key=lambda x: float(x[0]), reverse=reverse)  # Convert values to float for numeric sorting
    else:
        items.sort(reverse=reverse)

    # Rearrange items in the treeview based on the sorted order
    for index, (val, item) in enumerate(items):
        tree.move(item, '', index)

def setup_treeview_sorting(tree):
    # Bind the sorting function to column headers
    for col_id in tree['columns']:
        tree.heading(col_id, text=col_id, command=lambda _col=col_id: sort_treeview_column(tree, _col))