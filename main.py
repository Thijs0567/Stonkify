import customtkinter as ctk
import gui
from PIL import Image

if __name__ == "__main__":
    # Create a window
    root = ctk.CTk()
    root.geometry("1000x650")
    
    # Set window title
    root.title("Stonkify")

    # # Set the application icon
    # img = Image.open('resources/logo.png')

    # # Convert to ICO format with transparency
    # img.save('resources/logo.ico', format="ICO", transparency=0)
    root.iconbitmap('resources/logo.ico')

    # Create the GUI
    app = gui.MyApplication(root)
    app.pack(fill=ctk.BOTH, expand=True)

    # Run the event loop
    root.mainloop()
