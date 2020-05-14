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
    image_file = path / 'images' / file
    open_image = Image.open(image_file)
    open_image = open_image.resize((1000, 1000))  # resize image
    img = ImageTk.PhotoImage(open_image)
    w.create_image(0, 0, image=img, anchor="nw")

    # create output file for image
    out_file = out_dir / re.sub(r'[.].*', '.txt', str(file))
    if os.path.isfile(out_file):  # delete coordinate file if it exists
        os.remove(out_file)
    with open(out_file, 'w') as f:  # create new coordinate file (required to not get error when appending to file)
        f.write(f"Bounding box coordinates of file {file}\n\n")

    def print_coords(event):
        # print coordinates to file
        with open(out_file, 'a') as f:
            f.write(f"{event.x}, {event.y}\n")

        # count number of lines in file
        with open(out_file) as f:
            file_length = len([1 for _ in f])

        # if four coordinates found (i.e. a bounding box) print new line
        if file_length % 5 == 2:  # four coordinates and \n (5) == title line and \n (2)
            with open(out_file, 'a') as f:
                f.write('\n')

    def close_window():
        # count number of lines in file
        with open(out_file) as f:
            file_length = len([1 for _ in f])

        # if four coordinates found (i.e. a bounding box) print new line
        if file_length % 5 != 2:  # four coordinates and one \n line == title line and one \n line
            print("Last set of coordinates incomplete. Please fix manually\n")

        # move onto next image
        w.quit()
        w.destroy()

    # buttons
    w.bind("<Button 1>", print_coords)
    button = Button(root, text='Click to quit', command=close_window)
    w.create_window(35, 35, anchor='nw', window=button)

    root.mainloop()


# files and folders
valid_extensions = ['.jpeg', '.jpg', '.png']  # image file extensions
files = [file for file in os.listdir(path / 'images')
         if re.search(r'[.].*', file).group() in valid_extensions]

# write coordinate files
for fimage in files:
    get_coords(fimage)
