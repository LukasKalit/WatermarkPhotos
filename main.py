from tkinter import *
import tkinter
from tkinter import ttk
from tkinter import filedialog

from PIL import Image
import os


import random

WATERMARK_NAME = "watermark.png"

def load_image(file_name):

    print(file_name)
    if len(filename) == 1:
        im = Image.open(file_name[0])
        return im
    else:
        list_of_im = []
        for i in filename:
            im = Image.open(i)
            list_of_im.append(im)
        return list_of_im
    
    print(im.format, im.size, im.mode)

def load_watermark(watermark_name):

    im = Image.open(watermark_name)
    return im
    print(im.format, im.size, im.mode)

def add_watermark(list_of_paths, watermark, position_text):

        # Convert watermark to RGBA mode if it's not already
    if watermark.mode != "RGBA":
        watermark = watermark.convert("RGBA")
    
    print(f"aaa{list_of_paths}aaa")
    if len(list_of_paths) != None:
        list_of_im = []
        for i in list_of_paths:
            im = Image.open(i)
            list_of_im.append(im)

    else:
        raise ValueError("Invalid paths to photos")


    watermark_width, watermark_height = watermark.size
    aspect_ratio = watermark_width / watermark_height

    for base_image in list_of_im:

        # Extract the original filename from the full path
        original_filename = os.path.splitext(os.path.basename(base_image.filename))[0]

        print(base_image.filename)
        # Construct the new filename with the "watermarked" suffix
        output_image_path = f"converted_photos/{original_filename}_watermarked.jpg"

        # Resize watermark to fit on the base image
        width, height = base_image.size
        new_width = int(width * 0.25)
        new_height = int(new_width / aspect_ratio)
        watermark_resized = watermark.resize((new_width, new_height))

        # Paste the watermark onto the base image
        if position_text == "center":
            label3.config(text="")
            print("position_center")
            position = ((width - new_width) // 2, (height - new_height) // 2)
        elif position_text == "bottomright":
            label3.config(text="")
            print("position_bottomright")
            position = (width - new_width, height - new_height)
        else:
            label3.config(text="Invalid position")
            raise ValueError("Invalid position")

        print(base_image, "1")
        print(output_image_path, "2")
        print( watermark, "3")
        print(position, "4")
        base_image.paste(watermark_resized, position, watermark_resized)

        # Save the final image
        print(f"wykonuje się nie wiem po co   {output_image_path}")
        try:
            base_image.save(output_image_path)
        except FileNotFoundError:
            current_directory = os.path.dirname(__file__)
            folder_name = 'converted_photos'
            folder_path = os.path.join(current_directory, folder_name)
            os.makedirs(folder_path)
            base_image.save(output_image_path)

def open_filedialog(label2):

    # Open File Dialog in Tkinter
    global filename
    filename =  filedialog.askopenfilenames(initialdir = "/",title = "Select file",filetypes = (("jpeg files","*.jpg"),("all files","*.*")))
    print(len(filename))
    print(filename)
    if filename != "":
        if len(filename) == 1:
            label2.config(text=filename)
        else:
            label2.config(text="multiple image loaded")
    else:
        label2.config(text="no file loaded")
        return
    return filename

def print_filename(filename):
    print(filename)


# Initialize Tkinter
root = Tk()
frm = ttk.Frame(root, padding=15)
frm.grid()

location = StringVar()


label1 = ttk.Label(frm, text='Where insert watermark?').grid(column=0, row=0)

center = ttk.Radiobutton(frm, text='Middle', variable=location, value='center').grid(column=0, row=1)
bottomright = ttk.Radiobutton(frm, text='Right-Bottom', variable=location, value='bottomright')
bottomright.grid(column=0, row=2)

label2 = ttk.Label(frm, text="no file selected")
label2.grid(column=0, row=3)

label3 = ttk.Label(frm, text="")
label3.grid(column=0, row=4)

button2 = ttk.Button(frm, text="Load file", command=lambda: open_filedialog(label2))
button2.grid(column=0, row=5)

ttk.Button(frm, text="Execute", command=lambda: add_watermark(filename, load_watermark(WATERMARK_NAME), position_text=location.get())).grid(column=0, row=6)
ttk.Button(frm, text="Quit", command=root.destroy).grid(column=0, row=7)


mask = tkinter.READABLE | tkinter.WRITABLE

root.mainloop()