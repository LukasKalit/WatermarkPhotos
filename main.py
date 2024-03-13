from tkinter import *
import tkinter
from tkinter import ttk
from tkinter import filedialog

from PIL import Image
import os


WATERMARK_NAME = "watermark.png"
size_scalar = float(0.2)
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
    

def load_watermark(watermark_name):

    im = Image.open(watermark_name)
    return im

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


        # Resize watermark to fit on the base image
        width, height = base_image.size
        if width > height:
            new_width = int(width * size_scalar)
            new_height = int(new_width / aspect_ratio)
            watermark_resized = watermark.resize((new_width, new_height))
        else:
            new_width = int(width * size_scalar * (1.8))
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

        elif position_text == "bottomcenter":
            label3.config(text="")
            print("position_bottomcenter")
            position = ((width - new_width) // 2, height - new_height)

        elif position_text == "bottomleft":
            label3.config(text="")
            print("position_bottomleft")
            position = (0, height - new_height)

        else:
            label3.config(text="Invalid position")
            raise ValueError("Invalid position")

        base_image.paste(watermark_resized, position, watermark_resized)

        # Extract the original filename from the full path
        original_filename = os.path.splitext(os.path.basename(base_image.filename))[0]

        print(base_image.filename)
        # Construct the new filename with the "watermarked" suffix
        output_image_path = os.path.join("converted_photos", f"{original_filename}_watermarked.jpg")



        # Save the final image
        output_directory = os.path.dirname(output_image_path)
        os.makedirs(output_directory, exist_ok=True)
        current_directory = os.path.dirname(__file__)
        current_directory = os.path.join(current_directory,"..", output_image_path)
        try:
            base_image.save(current_directory)
        except FileNotFoundError:
            current_directory = os.path.dirname(__file__)
            current_directory = os.path.join(current_directory, output_image_path)
            base_image.save(current_directory)



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

def on_slider_change(value):
    global size_scalar
    label4.config(text=f"Size of watermark: {int(float(value))}%")
    size_scalar = int(float(value))/100


# Initialize Tkinter
root = Tk()
frm = ttk.Frame(root, padding=15)
frm.grid()

location = StringVar()


label1 = ttk.Label(frm, text='Where insert watermark?').grid(column=0, row=0)

center = ttk.Radiobutton(frm, text='Middle', variable=location, value='center').grid(column=0, row=1)
bottomright = ttk.Radiobutton(frm, text='Bottom-Right', variable=location, value='bottomright').grid(column=0, row=2)
bottomcenter = ttk.Radiobutton(frm, text='Bottom-Center', variable=location, value='bottomcenter').grid(column=1, row=1)
bottomleft = ttk.Radiobutton(frm, text='Bottom-Left', variable=location, value='bottomleft').grid(column=1, row=2)


label2 = ttk.Label(frm, text="no file selected")
label2.grid(column=0, row=3)

label3 = ttk.Label(frm, text="")
label3.grid(column=0, row=4)

label4 = ttk.Label(frm, text=f"Size of watermark: 20%")
label4.grid(column=1, row=3)

slider = ttk.Scale(frm, from_=1, to=50, orient=tkinter.HORIZONTAL, command=on_slider_change, value=20)
slider.grid(row=4, column=1, padx=10)

button2 = ttk.Button(frm, text="Load file", command=lambda: open_filedialog(label2))
button2.grid(column=0, row=5)

ttk.Button(frm, text="Execute", command=lambda: add_watermark(filename, load_watermark(WATERMARK_NAME), position_text=location.get())).grid(column=0, row=6)
ttk.Button(frm, text="Quit", command=root.destroy).grid(column=0, row=7)


mask = tkinter.READABLE | tkinter.WRITABLE

root.mainloop()