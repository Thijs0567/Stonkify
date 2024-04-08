
import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
import utils
import gui_utils
import os

class MyApplication(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.create_widgets()

    def create_widgets(self):
        # Create a notebook (tabs container)
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
        label_text = "Spotify playlist link here:"
        overview_label = ctk.CTkLabel(overview_frame, text=label_text, font=('Helvetica', 16))
        overview_label.grid(row=0, column=0, pady=(10, 5), sticky="n")

        # Create an input box centered and spans 75% of the width
        input_box = ctk.CTkEntry(overview_frame, width=50) # Adjust width as needed
        input_box.insert(0, 'https://open.spotify.com/playlist/333sK6VxQ6b4iSlcD5iRWY?si=f02345d1c5fb440b')
        input_box.grid(row=1, column=0, pady=(0, 5), padx=10, sticky="ew")

        # Configure the column to make the input box span 75% of the width
        overview_frame.columnconfigure(0, weight=3)  # 75% of the width

        # Create a Treeview widget
        tree = gui_utils.create_treeview(overview_frame)

        # Define submit button function:
        def submit_playlist_link():
            # Get the input from the entry widget
            link = input_box.get()

            # Extract the playlist ID from the link
            playlist_id = utils.extract_playlist_id(link)

            # Load the playlist data to a JSON:
            playlist_data = utils.load_playlist(playlist_id)

            # Populate the Treeview widget with JSON data
            gui_utils.populate_treeview(tree, playlist_data)

            if playlist_id:
                tk.messagebox.showinfo("Success", f"Playlist ID: {playlist_id}")
            else:
                tk.messagebox.showerror("Error", "Invalid Spotify playlist link")

        # Create submit button
        button = ctk.CTkButton(overview_frame, text="Submit", command=submit_playlist_link)
        button.grid(row=1, column=1, pady=(0, 5), padx=(0, 10), sticky="w")

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

