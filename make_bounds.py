from tkinter import *
import tkinter.messagebox
from tkinter.filedialog import askopenfilename
from PIL import Image, ImageTk
import tkinter.simpledialog
from pathlib import Path
import os
import warnings

root = Tk()
path = Path(__file__).parent
out_dir = path / 'coordinates'
out_dir.mkdir(exist_ok=True)


def get_coords(file):
    # setting up a tkinter canvas
    w = Canvas(root, width=1000, height=1000)
    w.pack()

    # adding the image
    File = path / 'images' / file
    original = Image.open(File)
    original = original.resize((1000, 1000))  # resize image
    img = ImageTk.PhotoImage(original)
    w.create_image(0, 0, image=img, anchor="nw")

    # create output file for image
    file_name = re.split(r'[.]', str(file))  # TODO: replace this with re.sub
    out_file = out_dir / (file_name[0] + '.txt')
    if os.path.isfile(out_file):
        os.remove(out_file)
    with open(out_file, 'w') as f:  # required as to not get an error with appending to file below on first coordinate
        f.write(f"{file}\n\n")

    def print_coords(event):
        # print coordinates
        with open(out_file, 'a') as f:
            f.write(f"{event.x}, {event.y}\n")

        # number of lines in file
        with open(out_file) as f:
            file_length = len([1 for _ in f])

        # if four coordinates found print new line
        if file_length % 5 == 2:  # four coordinates and \n (5) == title line and \n (2)
            with open(out_file, 'a') as f:
                f.write('\n')

    def close_window():
        # number of lines in file
        with open(out_file) as f:
            file_length = len([1 for _ in f])

        # if four coordinates found print new line
        if file_length % 5 != 2:  # four coordinates and one \n line == title line and one \n line
            print("Last set of coordinates incomplete. Please fix manually")  # TODO: make this better. warnings.warn not working for some reason

        w.quit()
        w.destroy()

    # buttons
    w.bind("<Button 1>", print_coords)
    button = Button(root, text='Click to quit', command=close_window)
    w.create_window(35, 35, anchor='nw', window=button)

    root.mainloop()


# files and folders
files = [file for file in os.listdir(path / 'images') if not 'DS' in file]  # TODO: change 'if not' to regex with valid file extensions
for fimage in files:
    get_coords(fimage)
