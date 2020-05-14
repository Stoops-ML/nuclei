from tkinter import *
from PIL import Image, ImageTk
from pathlib import Path
import os


class ImageCoordinates:
    def __init__(self, input_folder='images', output_folder='coordinates'):
        # initialise
        self.root = Tk()

        # folders
        self.in_dir = Path(__file__).parent / input_folder
        self.out_dir = Path(__file__).parent / output_folder
        self.out_dir.mkdir(exist_ok=True)

        # get all image files
        valid_extensions = ['.jpeg', '.jpg', '.png']  # image file extensions
        self.files = [file for file in os.listdir(self.in_dir)
                      if re.search(r'[.].*', file).group() in valid_extensions]

    def get_coordinates(self, file):
        """print to file user selected coordinates"""
        # set up tkinter canvas
        w = Canvas(self.root, width=1000, height=1000)
        w.pack()
    
        # add image to canvas
        image_file = self.in_dir / file
        open_image = Image.open(image_file)
        open_image = open_image.resize((1000, 1000))  # resize image
        img = ImageTk.PhotoImage(open_image)
        w.create_image(0, 0, image=img, anchor="nw")
    
        # output file for image
        out_file = self.out_dir / re.sub(r'[.].*', '.txt', str(file))
        with open(out_file, 'w') as f:  # clear contents of out_file
            f.write('\n')  # required for printing next new lines later

        def print_coordinates(event):
            # print coordinates to file
            with open(out_file, 'a') as f:
                f.write(f"{event.x}, {event.y}\n")
    
            # count number of lines in file
            with open(out_file) as f:
                file_length = len([1 for _ in f])
    
            # if four coordinates found (i.e. a bounding box) print new line
            if file_length % 5 == 0:  # four coordinates and \n (5)
                with open(out_file, 'a') as f:
                    f.write('\n')
    
        def close_window():
            # count number of lines in file
            with open(out_file) as f:
                file_length = len([1 for _ in f])
    
            # if four coordinates found (i.e. a bounding box) print new line
            if file_length % 5 != 0:  # four coordinates and one \n line
                print(f"Last set of coordinates incomplete of file: {file}.\nFix coordinate file manually.\n")
    
            # move onto next image
            w.quit()
            w.destroy()
    
        # buttons
        w.bind("<Button 1>", print_coordinates)
        button = Button(self.root, text='Click to quit', command=close_window)
        w.create_window(35, 35, anchor='nw', window=button)
    
        self.root.mainloop()

    def run_thru_files(self):
        """run through all images in input directory"""
        for fimage in self.files:
            self.root.title(f"Image file: {fimage}")
            self.get_coordinates(fimage)


if __name__ == '__main__':
    write_coordinates = ImageCoordinates()
    write_coordinates.run_thru_files()
