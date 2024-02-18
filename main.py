from tkinter import *
import tkinter
from tkinter import ttk
from tkinter import filedialog

from PIL import Image

WATERMARK_NAME = "watermark.png"

def load_image(file_name):

    print(file_name)
    im = Image.open(file_name)
    return im
    print(im.format, im.size, im.mode)

def load_watermark(watermark_name):

    im = Image.open(watermark_name)
    return im
    print(im.format, im.size, im.mode)

def add_watermark(base_image, output_image_path, watermark, position):

        # Convert watermark to RGBA mode if it's not already
    if watermark.mode != "RGBA":
        watermark = watermark.convert("RGBA")


    # Resize watermark to fit on the base image
    width, height = base_image.size
    watermark_width, watermark_height = watermark.size
    aspect_ratio = watermark_width / watermark_height
    new_width = int(width * 0.25)
    new_height = int(new_width / aspect_ratio)
    watermark = watermark.resize((new_width, new_height))

    # Paste the watermark onto the base image
    if position == "center":
        position = ((width - new_width) // 2, (height - new_height) // 2)
    elif position == "bottomright":
        position = (width - new_width, height - new_height)
    else:
        print(position)
        raise ValueError("Invalid position")
    
    print(base_image, "1")
    print(output_image_path, "2")
    print( watermark, "3")
    print(position, "4")
    base_image.paste(watermark, position, watermark)

    # Save the final image
    base_image.save(output_image_path)

def open_filedialog():

    # Open File Dialog in Tkinter
    global filename
    filename =  filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("jpeg files","*.jpg"),("all files","*.*")))

    print (filename)
    return filename


# Initialize Tkinter
root = Tk()
frm = ttk.Frame(root, padding=15)
frm.grid()

location = StringVar()
filename = "asdasd"

label_title = ttk.Label(frm, text='Where insert watermark?').grid(column=0, row=0)

center = ttk.Radiobutton(frm, text='Middle', variable=location, value='center').grid(column=0, row=1)
bottomright = ttk.Radiobutton(frm, text='Right-Bottom', variable=location, value='bottomright').grid(column=0, row=2)

label_file = ttk.Label(frm, text=filename).grid(column=0, row=3)
ttk.Button(frm, text="Load file", command=open_filedialog).grid(column=0, row=4)
ttk.Button(frm, text="Execute", command=lambda: add_watermark(load_image(filename), "output_image_with_watermark.jpg", load_watermark(WATERMARK_NAME), position=location.get())).grid(column=0, row=5)
ttk.Button(frm, text="Quit", command=root.destroy).grid(column=0, row=6)

mask = tkinter.READABLE | tkinter.WRITABLE

root.mainloop()