from tkinter import *
from PIL import Image, ImageTk
from pathlib import Path
import os


class ImageCoordinates:
    def __init__(self, input_folder='images', output_folder='coordinates'):
        # initialise
        self.root = Tk()
        self.line = None

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
        self.corner = None

        # add image to canvas
        image_file = self.in_dir / file
        open_image = Image.open(image_file)
        open_image = open_image.resize((1000, 1000))  # resize image
        img = ImageTk.PhotoImage(open_image)
        self.w.create_image(0, 0, image=img, anchor="nw")

        # output file for image
        self.out_file = self.out_dir / re.sub(r'[.].*', '.txt', str(file))
        with open(self.out_file, 'w') as _:  # clear contents of out_file
            pass

        def close_window():
            # count number of lines in file
            with open(self.out_file) as f:
                file_length = len([1 for _ in f])

            # move onto next image
            self.w.quit()
            self.w.destroy()

        # buttons
        self.w.bind("<Button 1>", self.print_coordinates)
        self.w.bind("<Motion>", self.draw_line)
        button = Button(self.root, text='Next image', command=close_window)
        self.w.create_window(35, 35, anchor='nw', window=button)

        self.root.mainloop()

    def print_coordinates(self, event):
        if self.corner is None:
            self.corner = [event.x, event.y]  # save first corner

            # draw reference dot
            x1, y1 = (event.x - 1), (event.y - 1)
            x2, y2 = (event.x + 1), (event.y + 1)
            self.dot = self.w.create_oval(x1, y1, x2, y2, fill='black', outline='green', width=10)

        else:
            # draw bounding box
            self.w.create_rectangle(self.corner[0], self.corner[1], event.x, event.y, width=2, outline='red')
            self.w.delete(self.dot)  # delete reference dot

            # print coordinates to file
            with open(self.out_file, 'a') as f:
                f.write(f"{self.corner[0]}, {self.corner[1]}\n"
                        f"{self.corner[0]}, {event.y}\n"
                        f"{event.x}, {self.corner[1]}\n"
                        f"{event.x}, {event.y}\n\n")
                
            self.corner = None

    def draw_line(self, event):
        if self.line is not None:
            self.w.delete(self.line)
        self.line = self.w.create_line(self.corner[0], self.corner[1], event.x, event.y, dash=2, width=2, fill='red')

    def run_thru_files(self):
        """run through all images in input directory"""
        for fimage in self.files:
            self.root.title(f"Image file: {fimage}")
            self.get_coordinates(fimage)


if __name__ == '__main__':
    write_coordinates = ImageCoordinates()
    write_coordinates.run_thru_files()
