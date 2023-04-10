from tkinter import *
from tkinter import ttk
import os
from PIL import ImageTk, Image
import poke_api
import image_lib

# GUI Init
root = Tk()
root.title("Jon's PokeViewer!")



# Get the path of the script and its parent directory
script_path = os.path.abspath(__file__)
script_dir = os.path.dirname(script_path)
# Set the window icon
icon_path = os.path.join(script_dir, 'pokeball.ico')
root.iconbitmap(icon_path)

#Button Handlers
def handle_poke_sel(event):
    sel_name_index = dropdown.current()
    img_path = poke_api.download_pokemon_artwork(poke_name_list[sel_name_index], script_dir)
    img_logo['file'] = img_path
    return


# Frame Creation
frm = ttk.Frame(root)
frm.grid(row=0, column=0)

# Add Widgets
img_logo = ImageTk.PhotoImage(file=os.path.join(script_dir, 'pokeball.png'))
pic = ttk.Label(frm, image=img_logo)
pic.grid(row=0)

poke_name_list = sorted(poke_api.get_pokemon_names())
dropdown = ttk.Combobox(frm, values=poke_name_list, state='readonly')
dropdown.grid(row=1, padx=10, pady=10)
dropdown.set("Select a Pokemon")
dropdown.bind('<<ComboboxSelected>>', handle_poke_sel)

btn = ttk.Button(frm, text="Set as Desktop Image")
btn.grid(row=2, padx=10, pady=10)

# GUI Loop
root.mainloop()