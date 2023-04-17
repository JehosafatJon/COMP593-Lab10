""" ~~~ Jonathan Hughes COMP593 ~~~~~~
               __
              / _) < woohoo python!
     _.----._/ /
    /         /
 __/ (  | (  |
/__.-'|_|--|_|   
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Pokemon Image Viewer

Description:
  Displays the shiny sprite for any pokemon
  in a nice GUI, and allows the user to set
  that picture as their desktop background

Usage:
  python pokemon_image_viewer.py

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"""

from tkinter import *
from tkinter import ttk
import os
from PIL import ImageTk, Image
import poke_api
import image_lib

# GUI Init
root = Tk()
root.geometry("475x565")
root.title("Jon's PokeViewer!")
root.resizable(0,0)

# Get the path of the script and its parent directory
script_path = os.path.abspath(__file__)
script_dir = os.path.dirname(script_path)

# Set the window icon
icon_path = os.path.join(script_dir, 'pokeball.ico')
root.iconbitmap(icon_path)

#Button Handlers

def handle_poke_sel(event):
    """Handler to download and display 
       the pokemon when the user selects 
       from the dropdown box

    Args:
        event: the automatically passed event 
               argument for handlers
    """

    # Gets selection from dropdown and
    # Downloads/saves the image
    sel_name_index = dropdown.current()
    global img_path
    img_path = poke_api.download_pokemon_artwork(poke_name_list[sel_name_index], script_dir)

    # Resizes image
    unsized_img = Image.open(img_path)
    new_size = image_lib.scale_image(image_size=(unsized_img.width, unsized_img.height), max_size=(475,475))
    resized_img = unsized_img.resize(new_size)

    # Configures widget
    global img_poke
    img_poke = ImageTk.PhotoImage(resized_img)
    pic.configure(image=img_poke)

    # Enables the button if first selection
    if btn.instate(['disabled']):
        btn.state(['!disabled'])
    
    return

def handle_set_desktop():
    """Handler that sets the current pokemon as
       the desktop background.
    """

    # Uses the global var img_path to set desktop background
    image_lib.set_desktop_background_image(img_path)

    return

# Frame Creation
frm = ttk.Frame(root, width=475, height = 600)
frm.grid(row=0, column=0)

# Add Widgets
# Resize Image
unsized_img = Image.open(f"{script_dir}\\pokeball.png")
new_size = image_lib.scale_image(image_size=(unsized_img.width, unsized_img.height), max_size=(475,475))
resized_img = unsized_img.resize(new_size)

img_logo = ImageTk.PhotoImage(resized_img, size=(475,475))
pic = ttk.Label(frm, image=img_logo, width=475)
pic.grid(row=0)

poke_name_list = sorted(poke_api.get_pokemon_names())
dropdown = ttk.Combobox(frm, values=poke_name_list, state='readonly')
dropdown.grid(row=1, padx=10, pady=10, sticky=NSEW)
dropdown.set("Select a Pokemon")
dropdown.bind('<<ComboboxSelected>>', handle_poke_sel)

btn = ttk.Button(frm, text="Set as Desktop Image", state=DISABLED, command=handle_set_desktop)
btn.grid(row=2, padx=10, pady=10, sticky=NSEW)

# GUI Loop
root.mainloop()