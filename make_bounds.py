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
        self.w = Canvas(self.root, width=1000, height=1000)
        self.w.pack()
        self.clicks = 0

        # add image to canvas
        image_file = self.in_dir / file
        open_image = Image.open(image_file)
        open_image = open_image.resize((1000, 1000))  # resize image
        img = ImageTk.PhotoImage(open_image)
        self.w.create_image(0, 0, image=img, anchor="nw")

        # output file for image
        self.out_file = self.out_dir / re.sub(r'[.].*', '.txt', str(file))
        with open(self.out_file, 'w') as f:  # clear contents of out_file
            f.write('\n')  # required for printing next new lines later

        def close_window():
            # count number of lines in file
            with open(self.out_file) as f:
                file_length = len([1 for _ in f])

            # if four coordinates found (i.e. a bounding box) print new line
            if self.clicks % 5 != 0:  # four coordinates and one \n line
                print(f"Last set of coordinates incomplete of file: {file}.\nFix coordinate file manually.\n")

            # move onto next image
            self.w.quit()
            self.w.destroy()

        # buttons
        self.w.bind("<Button 1>", self.print_coordinates)
        button = Button(self.root, text='Click to quit', command=close_window)
        self.w.create_window(35, 35, anchor='nw', window=button)

        self.root.mainloop()

    def print_coordinates(self, event):
        # increase number of clicks
        self.clicks += 1

        # print coordinates to file
        with open(self.out_file, 'a') as f:
            f.write(f"{event.x}, {event.y}\n")
            if self.clicks == 4:
                f.write('\n')

        # draw bounding box
        if self.clicks == 1:
            self.first_coord = [event.x, event.y]  # beginning corner of box
        else:
            self.w.create_line(self.prev_events[0], self.prev_events[1], event.x, event.y, fill="red", width=2)  # connect corners

        if self.clicks == 4:
            self.w.create_line(event.x, event.y, self.first_coord[0], self.first_coord[1], fill="red", width=2)  # connect first and last corners
            self.clicks = 0  # reset click counter

        self.prev_events = [event.x, event.y]  # save coordinates for next run

    def run_thru_files(self):
        """run through all images in input directory"""
        for fimage in self.files:
            self.root.title(f"Image file: {fimage}")
            self.get_coordinates(fimage)


if __name__ == '__main__':
    write_coordinates = ImageCoordinates()
    write_coordinates.run_thru_files()
