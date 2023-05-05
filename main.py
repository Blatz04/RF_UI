import cv2 as cv
import tkinter as tk
import os
import numpy as np
from tkinter import filedialog
from PIL import Image, ImageTk

def OpenExplorer():
    global folder_path
    folder_path = filedialog.askdirectory(initialdir = "/",
										title = "Select Folder Directory")
    input_box.delete('1.0', tk.END)
    input_box.insert(tk.END, folder_path)

def load_sample_path():
    global sample_img_path
    if input_box.get('1.0','end-1c') == "":
        return tk.messagebox.showwarning(title="Folder/Path incorrect", message="Please enter folder path cointaining the image")
    if not os.path.exists(input_box.get('1.0','end-1c')):
        return tk.messagebox.showwarning(title="Folder/Path didn't exist", message="Please enter folder path cointaining the image")
    for i in (i for i in os.listdir(folder_path) if i.endswith(formats)):
        sample_img_path = os.path.join(folder_path, i)
        sample_img_path = sample_img_path.replace("\\", "/")
        sample_box.delete('1.0', tk.END)
        sample_box.insert(tk.END, sample_img_path)
        return
    return tk.messagebox.showwarning(title="No images found", message="Directory didn't contain any supported images")

def load_sample():
    global id, img, sample_img
    if not os.path.exists(sample_box.get('1.0','end-1c')):
        return tk.messagebox.showwarning(title="Folder/Path didn't exist", message="Please enter folder path cointaining the image")
    input_box.delete('1.0', tk.END)
    input_box.insert(tk.END, os.path.dirname(sample_box.get('1.0','end-1c')))
    sample_img = cv.imread(sample_box.get('1.0','end-1c'))
    img = cv.resize(sample_img, canvas, interpolation=cv.INTER_CUBIC)
    img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
    display_img(img,blank)
    id = 0
    #H:/Document/VS Code/RF_UI/DSC09578.JPG

def display_img(img,blank):
    im = Image.fromarray(img)
    imTk = ImageTk.PhotoImage(image=im)
    blank.configure(image=imTk)
    blank.image = imTk
    blank.grid(column=1,row=3)

# def updateValue(event):
#     print(scale.get())
#     reso = (scale.get(), scale.get())
#     img = cv.resize(sample_img, canvas, interpolation=cv.INTER_CUBIC)
#     img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
#     gaussian = cv.GaussianBlur(img, reso, 0)
#     display_img(gaussian, blank)

def stages():
    match id:
        case 0:
            print("stage 0")
        case _:
            return tk.messagebox.showwarning(title="Stage 0", message="Please load sample image first")
ref_ui = tk.Tk()

ref_ui.title("Reflective Filter")
ref_ui.iconbitmap("C_dim.ico")
ref_ui.geometry("540x420")
ref_ui.resizable(width=False, height=False)

label_folder = tk.Label(ref_ui, text="Folder Path")
label_folder.grid(column=0,row=0)
label_sample = tk.Label(ref_ui, text="Sample Image Path")
label_sample.grid(column=0,row=1)
label_info = tk.Label(ref_ui, text=
'''You can directly
put the Sample Image
Path.
The folder of the image
will be assumed as
the main folder
containing
the rest of the
image
''', justify="left")
label_info.grid(column=3,row=3)
label_stage = tk.Label(ref_ui, text="Current Step: 0, Load sample image as a reference")
label_stage.grid(column=1,row=4)

# label_blur = tk.Label(ref_ui, text="Blur Intensity")
# label_blur.grid(column=0,row=5)
# label_blur.grid_forget()


pick_folder = tk.Button(ref_ui, text="Pick folder", width=15, height=2, command=OpenExplorer)
pick_folder.grid(column=3,row=0)
load = tk.Button(ref_ui, text="Load one sample \n from the folder", width=15, height=2, command=load_sample_path)
load.grid(column=3,row=1)
load_sample = tk.Button(ref_ui, text="Load Sample Image", width=15, height=2, command=load_sample)
load_sample.grid(column=0,row=3)
next_step = tk.Button(ref_ui, text="Go to the next step", width=15, height=2, command=stages)
next_step.grid(column=0,row=4)

input_box = tk.Text(ref_ui, width=35, height=1)
input_box.grid(column=1,row=0)
sample_box = tk.Text(ref_ui, width=35, height=1)
sample_box.grid(column=1,row=1)

# scale = tk.Scale(ref_ui, from_=1, to_=99, resolution=2, length=200, orient="horizontal")
# scale.bind("<ButtonRelease-1>", updateValue)
# scale.grid(column=1,row=5)
# scale.grid_forget()

canvas = [250,250]
formats = (".JPG", ".jpg", ".PNG", ".png")
sample_img = np.zeros(canvas, dtype='uint8')
blank = tk.Label(ref_ui, bg='black')
display_img(sample_img,blank)

ref_ui.mainloop()