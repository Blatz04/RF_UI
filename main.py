import cv2 as cv
import tkinter as tk
import os
import numpy as np
from tkinter import filedialog, colorchooser
from PIL import Image, ImageTk

'''Functions'''

def enable(childList):
    for child in childList:
        child.configure(state='normal')
    frame2_apply_fc.configure(state='disable')

def OpenExplorer():
    global folder_path
    folder_path = filedialog.askdirectory(initialdir = "/",
										title = "Select Folder Directory")
    frame1_input_box.delete('1.0', tk.END)
    frame1_input_box.insert(tk.END, folder_path)

def load_sample_path():
    global sample_img_path
    if frame1_input_box.get('1.0','end-1c') == "":
        return tk.messagebox.showwarning(title="Folder/Path incorrect", message="Please enter folder path cointaining the image")
    if not os.path.exists(frame1_input_box.get('1.0','end-1c')):
        return tk.messagebox.showwarning(title="Folder/Path didn't exist", message="Please enter folder path cointaining the image")
    for i in (i for i in os.listdir(folder_path) if i.endswith(formats)):
        sample_img_path = os.path.join(folder_path, i)
        sample_img_path = sample_img_path.replace("\\", "/")
        frame1_sample_box.delete('1.0', tk.END)
        frame1_sample_box.insert(tk.END, sample_img_path)
        return
    return tk.messagebox.showwarning(title="No images found", message="Directory didn't contain any supported images")

def load_sample():
    global id, img, sample_img
    if not os.path.exists(frame1_sample_box.get('1.0','end-1c')):
        return tk.messagebox.showwarning(title="Folder/Path didn't exist", message="Please enter folder path cointaining the image")
    frame1_input_box.delete('1.0', tk.END)
    frame1_input_box.insert(tk.END, os.path.dirname(frame1_sample_box.get('1.0','end-1c')))
    sample_img = cv.imread(frame1_sample_box.get('1.0','end-1c'))
    img = cv.resize(sample_img, canvas, interpolation=cv.INTER_CUBIC)
    img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
    enable(frame2.winfo_children())
    ori_img(img)
    err_dil_img(img)
    current_img(img)
    fc_img(img)
    
def ori_img(img):
    im = Image.fromarray(img)
    imTk = ImageTk.PhotoImage(image=im)
    blank.configure(image=imTk)
    blank.image = imTk
    blank.grid(column=1,row=3,pady=10)

def current_img(img):
    im = Image.fromarray(img)
    imTk = ImageTk.PhotoImage(image=im)
    current_blank.configure(image=imTk)
    current_blank.image = imTk
    current_blank.grid(column=1,row=6,pady=10)

def fc_img(img):
    im = Image.fromarray(img)
    imTk = ImageTk.PhotoImage(image=im)
    fc_blank.configure(image=imTk)
    fc_blank.image = imTk
    fc_blank.grid(column=1,row=0,pady=10,columnspan=3)

def fc_filter():
    global fc
    brown_lo=np.array([color_low[0][0],color_low[0][1],color_low[0][2]])
    brown_hi=np.array([color_hi[0][0],color_hi[0][1],color_hi[0][2]])
    fc=cv.inRange(img,brown_lo,brown_hi)
    current_img(fc)
    fc_img(fc)
    enable(frame3.winfo_children())

def color_pick():
    color = colorchooser.askcolor(title="Pick Color")
    return color

def hi_change():
    global color_hi, color_hi_status
    color_hi = color_pick()
    frame2_hi_color.configure(bg=color_hi[1])
    color_hi_status = 1
    try:
        if color_low_status == 1:
            frame2_apply_fc.configure(state='normal')
    except NameError:
        pass
        
def low_change():
    global color_low, color_low_status
    color_low = color_pick()
    frame2_low_color.configure(bg=color_low[1])
    color_low_status = 1
    try:
        if color_hi_status == 1:
            frame2_apply_fc.configure(state='normal')
    except NameError:
        pass
        
def err_dil_img(img):
    im = Image.fromarray(img)
    imTk = ImageTk.PhotoImage(image=im)
    err_dil_blank.configure(image=imTk)
    err_dil_blank.image = imTk
    err_dil_blank.grid(column=1,row=4,padx=(0,28),pady=10,columnspan=3)

def err_dil_updateValue(event):
    reso = (1,1)
    n = frame3_err_dil_scale.get()
    erroded = cv.erode(fc, reso, iterations=n)
    dilated = cv.dilate(erroded, reso, iterations=n+2)
    err_dil_img(dilated)
    current_img(dilated)
    
def err_dil_apply():
    pass

'''UI Settings'''

ref_ui = tk.Tk()

ref_ui.title("Reflective Filter")
ref_ui.iconbitmap("C_dim.ico")
ref_ui.geometry("1024x640")
#ref_ui.resizable(width=False, height=False)

'''Left Part'''
left_part = tk.Frame(ref_ui)
left_part.pack(side="left", anchor='ne')

'''Right Part'''
right_part = tk.Frame(ref_ui)
right_part.pack(side="top", anchor='w')

'''Frame1'''
frame1 = tk.Frame(left_part)
frame1.grid(column=0)

'''Labels'''
frame1_label_folder = tk.Label(frame1, text="Folder Path")
frame1_label_folder.grid(column=0,row=0,padx=(0,10))
frame1_label_sample = tk.Label(frame1, text="Sample Image Path", )
frame1_label_sample.grid(column=0,row=1,padx=(0,10))
frame1_label_ori = tk.Label(frame1, text="Original Image", font='bold')
frame1_label_ori.grid(column=1,row=4)
blank = tk.Label(frame1, bg='black')
#frame1_label_border = tk.Label(frame1, bg='#AAAAAA', width=0, height=40)
#frame1_label_border.grid(column=4,row=0, rowspan=15)
frame1_label_info = tk.Label(frame1, text=
'You can directly put the Sample Image Path.The folder of the image will be assumed as the main folder containing the rest of the image', justify="left", wraplength=100)
frame1_label_info.grid(column=2,row=3,columnspan=2)

'''Buttons'''
frame1_pick_folder = tk.Button(frame1, text="Pick folder", width=15, height=2, command=OpenExplorer)
frame1_pick_folder.grid(column=3,row=0,padx=10)
frame1_load_img = tk.Button(frame1, text="Load one sample \n from the folder", width=15, height=2, command=load_sample_path)
frame1_load_img.grid(column=3,row=1,padx=10)
frame1_load_sample = tk.Button(frame1, text="Load Sample Image", width=15, height=2, command=load_sample)
frame1_load_sample.grid(column=0,row=3)

'''Text Box'''
frame1_input_box = tk.Text(frame1, width=35, height=1)
frame1_input_box.grid(column=1,row=0)
frame1_sample_box = tk.Text(frame1, width=35, height=1)
frame1_sample_box.grid(column=1,row=1)
frame1_sample_box.insert(tk.END, "H:/Document/VS Code/RF_UI/DSC09578.JPG")

'''Frame1_2'''

'''Labels'''
frame1_label_grey = tk.Label(frame1, text="Current Result", font='bold')
frame1_label_grey.grid(column=1,row=7)
current_blank = tk.Label(frame1, bg='black')

'''Frame2'''
frame2 = tk.Frame(right_part)
frame2.grid(column=0,row=0,sticky='w')

'''Labels'''
frame2_label_grey = tk.Label(frame2, text="Color Filtered Image", font='bold')
frame2_label_grey.grid(column=1,row=1,columnspan=3,pady=10)
fc_blank = tk.Label(frame2, bg='black')
frame2_hi_color = tk.Label(frame2, bg=None, width=4, height=2)
frame2_hi_color.grid(column=1,row=2)
frame2_low_color = tk.Label(frame2, bg=None, width=4, height=2)
frame2_low_color.grid(column=3,row=2)
frame2_fc_info = tk.Label(frame2, text=
'Pick range of color to remove correspond to the reflection. White is Higest and Dark is Lowest. Color is treated as RGB color scheme, so carefull to not flip the maximum and minimum picked color', justify="left", wraplength=100)
frame2_fc_info.grid(column=5,row=0)

'''Buttons'''
frame2_hi_pick = tk.Button(frame2, text='Pick Maximum Color', wraplength=100, height=2, command=hi_change)
frame2_hi_pick.grid(column=0,row=2)
frame2_low_pick = tk.Button(frame2, text='Pick Minimum Color', wraplength=100, height=2, command=low_change)
frame2_low_pick.grid(column=4,row=2)
frame2_apply_fc = tk.Button(frame2, text='Apply', command=fc_filter)
frame2_apply_fc.grid(column=2,row=3)

for child in frame2.winfo_children():
    child.configure(state='disable')

'''Frame3'''
frame3 = tk.Frame(right_part)
frame3.grid(column=0,row=1, sticky='w')

'''Labels'''
frame3_label_grey = tk.Label(frame3, text="Erroded and Dilated Image", font='bold')
frame3_label_grey.grid(column=1,row=5,columnspan=3)
frame3_label_err_dil = tk.Label(frame3, text="Erroded and Dilated  Intensity", justify='center', wraplength=80)
frame3_label_err_dil.grid(column=0,row=6)
err_dil_blank = tk.Label(frame3, bg='black')

'''Scales'''
frame3_err_dil_scale = tk.Scale(frame3, from_=0, to_=25, length=150, orient="horizontal")
frame3_err_dil_scale.bind("<ButtonRelease-1>", err_dil_updateValue)
frame3_err_dil_scale.grid(column=1,row=6,columnspan=3)

'''Buttons'''
frame3_apply_fc = tk.Button(frame3, text='Apply', command=err_dil_apply)
frame3_apply_fc.grid(column=1,row=7,columnspan=3)

for child in frame3.winfo_children():
    child.configure(state='disable')

'''Etc.'''
canvas = [150,150]
formats = (".JPG", ".jpg", ".PNG", ".png")
sample_img = np.zeros(canvas, dtype='uint8')
ori_img(sample_img)
err_dil_img(sample_img)
current_img(sample_img)
fc_img(sample_img)

ref_ui.mainloop()