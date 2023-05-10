import cv2 as cv
import tkinter as tk
import os
import numpy as np
from tkinter import filedialog, colorchooser, ttk
from PIL import Image, ImageTk
from skimage import measure

'''Functions'''

def enable(childList):
    for child in childList:
        child['state'] = 'normal'
    frame3_scale_erroded['state'] = 'disable'
    frame3_scale_dilated['state'] = 'disable'
    frame3_var1.set(value=0)
    frame3_var2.set(value=0)

def OpenExplorer():
    global folder_path
    folder_path = filedialog.askdirectory(initialdir = "/",
										title = "Select Folder Directory")
    frame1_entry.delete(0, ttk.END)
    frame1_entry.insert(tk.END, folder_path)

def load_sample_path():
    global sample_img_path
    if frame1_entry.get() == "":
        return ttk.messagebox.showwarning(title="Folder/Path incorrect", message="Please enter folder path cointaining the image")
    if not os.path.exists(frame1_entry.get()):
        return ttk.messagebox.showwarning(title="Folder/Path didn't exist", message="Please enter folder path cointaining the image")
    for i in (i for i in os.listdir(folder_path) if i.endswith(formats)):
        sample_img_path = os.path.join(folder_path, i)
        sample_img_path = sample_img_path.replace("\\", "/")
        frame1_sample_entry.delete(0, ttk.END)
        frame1_sample_entry.insert(tk.END, sample_img_path)
        return
    return ttk.messagebox.showwarning(title="No images found", message="Directory didn't contain any supported images")

def load_sample():
    global id, img, sample_img
    if not os.path.exists(frame1_sample_entry.get()):
        return ttk.messagebox.showwarning(title="Folder/Path didn't exist", message="Please enter folder path cointaining the image")
    frame1_entry.delete(0, ttk.END)
    frame1_entry.insert(tk.END, os.path.dirname(frame1_sample_entry.get()))
    sample_img = cv.imread(frame1_sample_entry.get())
    img = cv.resize(sample_img, canvas, interpolation=cv.INTER_CUBIC)
    img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
    enable(frame2.winfo_children())
    ori_img(img)
    err_dil_img(img)
    current_img(img)
    fc_img(img)

def color_pick():
    color = colorchooser.askcolor(title="Pick Color")
    return color
    
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
    err_dil_updateValue('<Return>')

def hi_change():
    global color_hi, color_hi_status
    color_hi = color_pick()
    frame2_hi_color.configure(background=color_hi[1])
    if all(color_hi):
        color_hi_status = 1
    else:
        color_hi_status = 0
    try:
        if color_low_status == 1 and color_hi_status == 1:
            fc_filter()
    except NameError:
        pass
        
def low_change():
    global color_low, color_low_status
    color_low = color_pick()
    frame2_low_color.configure(background=color_low[1])
    if all(color_low):
        color_low_status = 1
    else:
        color_low_status = 0
    try:
        if color_low_status == 1 and color_hi_status == 1:
            fc_filter()
    except NameError:
        pass
        
def err_dil_img(img):
    im = Image.fromarray(img)
    imTk = ImageTk.PhotoImage(image=im)
    err_dil_blank.configure(image=imTk)
    err_dil_blank.image = imTk
    err_dil_blank.grid(column=1,row=4,padx=(0,28),pady=10,columnspan=3)

def err_dil_updateValue(event):
    global labels, mask
    n = frame3_scale_erroded.get()
    m = frame3_scale_dilated.get()
    erroded = cv.erode(fc, None, iterations=n)
    dilated = cv.dilate(erroded, None, iterations=m)
    err_dil_img(dilated)
    current_img(dilated)
    labels = measure.label(dilated, connectivity=2, background=0)
    mask = np.zeros(dilated.shape, dtype="uint8")

def filarea_img(img):
    im = Image.fromarray(img)
    imTk = ImageTk.PhotoImage(image=im)
    filarea_blank.configure(image=imTk)
    filarea_blank.image = imTk
    filarea_blank.grid(column=0,row=0,pady=10,columnspan=4)

def filarea_updateValue(event):
    if frame3_var1.get():
        for label in np.unique(labels):
            if label == 0:
                continue
            labelMask = np.zeros(mask.shape, dtype="uint8")
            labelMask[labels == label] = 255
            numPixels = cv.countNonZero(labelMask)
            if numPixels > frame4_scale_filarea.get():
                mask = cv.add(mask, labelMask)
            filarea_img(mask)
            current_img(mask)
    if frame3_var2.get():
        for label in np.unique(labels):
            if label == 0:
                continue
            labelMask = np.zeros(mask.shape, dtype="uint8")
            labelMask[labels == label] = 255
            numPixels = cv.countNonZero(labelMask)
            if numPixels < frame4_scale_filarea.get():
                mask = cv.add(mask, labelMask)
        filarea_img(mask)
        current_img(mask)
    
# def inpaint_img(img):
#     im = Image.fromarray(img)
#     imTk = ImageTk.PhotoImage(image=im)
#     inpaint_blank.configure(image=imTk)
#     inpaint_blank.image = imTk
#     inpaint_blank.grid(column=0,row=0,pady=0,columnspan=1)
    
'''UI Settings'''

ref_ui = tk.Tk()

ref_ui.title("Reflective Filter")
ref_ui.iconbitmap("C_dim.ico")
ref_ui.geometry("1280x600")
#ref_ui.resizable(width=False, height=False)

ref_ui.tk.call("source", "Azure-ttk-theme-main/azure.tcl")
ref_ui.tk.call("set_theme", "dark")

'''Left Part'''
left_part = ttk.Frame(ref_ui)
left_part.pack(side="left", anchor='n')

'''Center Part'''
center_part = ttk.Frame(ref_ui)
center_part.pack(side="left", anchor='n')

'''Right Part'''
right_part = ttk.Frame(ref_ui)
right_part.pack(side="left", anchor='n')

'''Frame1'''
frame1 = ttk.Frame(left_part)
frame1.grid(column=0)

'''Labels'''
frame1_label_folder = ttk.Label(frame1, text="Folder Path")
frame1_label_folder.grid(column=0,row=0,padx=(0,10))
frame1_label_sample = ttk.Label(frame1, text="Sample Image Path", )
frame1_label_sample.grid(column=0,row=1,padx=(0,10))
frame1_label_ori = ttk.Label(frame1, text="Original Image", font='bold')
frame1_label_ori.grid(column=1,row=4)
blank = ttk.Label(frame1, background='black')
#frame1_label_border = ttk.Label(frame1, background='#AAAAAA', width=0, height=40)
#frame1_label_border.grid(column=4,row=0, rowspan=15)
frame1_label_info = ttk.Label(frame1, text=
'You can directly put the Sample Image Path.The folder of the image will be assumed as the main folder containing the rest of the image', justify="left", wraplength=100)
frame1_label_info.grid(column=2,row=3,columnspan=2)

'''Buttons'''
frame1_pick_folder = ttk.Button(frame1, text="Pick folder", width=15, command=OpenExplorer)
frame1_pick_folder.grid(column=3,row=0,padx=10)
frame1_load_img = ttk.Button(frame1, text="Load one sample \n from the folder", width=15, command=load_sample_path)
frame1_load_img.grid(column=3,row=1,padx=10)
frame1_load_sample = ttk.Button(frame1, text="Load Sample Image", width=15, command=load_sample)
frame1_load_sample.grid(column=0,row=3)

'''Entry'''
frame1_entry = ttk.Entry(frame1, width=35)
frame1_entry.grid(column=1,row=0)
frame1_sample_entry = ttk.Entry(frame1, width=35)
frame1_sample_entry.grid(column=1,row=1)
frame1_sample_entry.insert(tk.END, "H:/Document/VS Code/RF_UI/DSC09578.JPG")

'''Frame1_2'''

'''Labels'''
frame1_label_grey = ttk.Label(frame1, text="Current Result", font='bold')
frame1_label_grey.grid(column=1,row=7)
current_blank = ttk.Label(frame1, background='black')

'''Frame2'''
frame2 = ttk.Frame(center_part)
frame2.grid(column=0,row=0,sticky='w')

'''Labels'''
frame2_label_grey = ttk.Label(frame2, text="Color Filtered Image", font='bold')
frame2_label_grey.grid(column=1,row=1,columnspan=3,pady=10)
fc_blank = ttk.Label(frame2, background='black')
frame2_hi_color = ttk.Label(frame2, background=None, width=4, height=2)
frame2_hi_color.grid(column=1,row=2)
frame2_low_color = ttk.Label(frame2, background=None, width=4, height=2)
frame2_low_color.grid(column=3,row=2)
frame2_fc_info = ttk.Label(frame2, text=
'Pick range of color to remove correspond to the reflection. White is Higest and Dark is Lowest. Color is treated as RGB color scheme, so carefull to not flip the maximum and minimum picked color', justify="left", wraplength=100)
frame2_fc_info.grid(column=5,row=0)

'''Buttons'''
frame2_hi_pick = ttk.Button(frame2, text='Pick Maximum Color', wraplength=100, command=hi_change)
frame2_hi_pick.grid(column=0,row=2)
frame2_low_pick = ttk.Button(frame2, text='Pick Minimum Color', wraplength=100, command=low_change)
frame2_low_pick.grid(column=4,row=2)

for child in frame2.winfo_children():
    child['state'] = 'disable'

'''Frame3'''

def frame3_checked():
    if frame3_var1.get():
        frame3_scale_erroded['state'] = 'normal'
        frame3_scale_erroded.bind("<B1-Motion>", err_dil_updateValue)
    if frame3_var2.get():
        frame3_scale_dilated['state'] = 'normal'
        frame3_scale_dilated.bind("<B1-Motion>", err_dil_updateValue)
    if not frame3_var1.get():
        frame3_scale_erroded.set(value=0)
        err_dil_updateValue('<Return>')
        frame3_scale_erroded['state'] = 'disable'
        frame3_scale_erroded.unbind("<B1-Motion>")
    if not frame3_var2.get():
        frame3_scale_dilated.set(value=0)
        err_dil_updateValue('<Return>')
        frame3_scale_dilated['state'] = 'disable'    
        frame3_scale_dilated.unbind("<B1-Motion>") 

frame3 = ttk.Frame(center_part)
frame3.grid(column=0,row=1, sticky='w')

'''Vars'''
frame3_var1 = ttk.BooleanVar(value=0)
frame3_var2 = ttk.BooleanVar(value=0)

'''Labels'''
frame3_label_grey = ttk.Label(frame3, text="Erroded/Dilated Image", font='bold')
frame3_label_grey.grid(column=1,row=5,columnspan=3)
err_dil_blank = ttk.Label(frame3, background='black')

'''Scales'''
frame3_scale_erroded = ttk.Scale(frame3, from_=0, to_=25, length=150, orient="horizontal")
frame3_scale_erroded.grid(column=1,row=6,columnspan=3)
frame3_scale_dilated = ttk.Scale(frame3, from_=0, to_=25, length=150, orient="horizontal")
frame3_scale_dilated.grid(column=1,row=7,columnspan=3)

'''Checkboxes'''
frame3_checkbox_erroded = ttk.Checkbutton(frame3, text="Erroded", variable=frame3_var1, command=frame3_checked)
frame3_checkbox_erroded.grid(column=0,row=6)
frame3_checkbox_dilated = ttk.Checkbutton(frame3, text="Dilated", variable=frame3_var2, command=frame3_checked)
frame3_checkbox_dilated.grid(column=0,row=7)

for child in frame3.winfo_children():
    child["state"] = 'disable'

'''Frame4'''

def frame4_checked():
    if frame4_var1.get() and frame4_var2.get():
        frame4_var1.set(value=0)
        frame4_var2.set(value=0)
    if frame4_var1.get() | frame4_var2.get():
        frame4_scale_filarea['state'] = 'normal'
        frame4_scale_filarea.bind("<B1-Motion>", filarea_updateValue)
    if not frame4_var1.get() and not frame4_var2.get():
        frame4_scale_filarea.set(value=0)
        filarea_updateValue('<Return>')
        frame4_scale_filarea['state'] = 'disable'
        frame4_scale_filarea.unbind("<B1-Motion>")
        
frame4 = ttk.Frame(right_part)
frame4.grid(column=0,row=0, sticky='w')

'''Vars'''
frame4_var1 = ttk.BooleanVar(value=0)
frame4_var2 = ttk.BooleanVar(value=0)

'''Labels'''
frame4_label_grey = ttk.Label(frame4, text="Filter Area", font='bold')
frame4_label_grey.grid(column=0,row=1,columnspan=4)
filarea_blank = ttk.Label(frame4, background='black')

'''Scales'''
frame4_scale_filarea = ttk.Scale(frame4, from_=0, to_=1000, length=250, orient="horizontal")
frame4_scale_filarea.grid(column=0,row=3,columnspan=4)
frame4_scale_filarea['state'] = 'disable'

'''Checkboxes'''
frame4_checkbox_large = ttk.Checkbutton(frame4, text="Remove Large", variable=frame4_var1, command=frame4_checked)
frame4_checkbox_large.grid(column=0,row=2, sticky='w')
frame4_checkbox_small = ttk.Checkbutton(frame4, text="Remove Small", variable=frame4_var2, command=frame4_checked)
frame4_checkbox_small.grid(column=2,row=2, columnspan=2, sticky='e')

# '''Frame4'''
# frame4 = ttk.Frame(right_part)
# frame4.grid(column=0,row=0, sticky='w')

# '''Vars'''
# #frame3_var1 = ttk.BooleanVar(value=0)

# '''Labels'''
# frame4_label_grey = ttk.Label(frame4, text="Inpaint", font='bold')
# frame4_label_grey.grid(column=1,row=5,columnspan=3)
# inpaint_blank = ttk.Label(frame4, background='black')

# '''Scales'''
# #frame4_scale_erroded = ttk.Scale(frame4, from_=0, to_=25, length=150, orient="horizontal")
# #frame4_scale_erroded.grid(column=1,row=6,columnspan=3)

# '''Checkboxes'''
# #frame4_checkbox_erroded = ttk.Checkbutton(frame4, text="Erroded", variable=frame3_var1, command=frame3_checked)
# #frame4_checkbox_erroded.grid(column=0,row=6)

'''Etc.'''
canvas = [150,150]
formats = (".JPG", ".jpg", ".PNG", ".png")
sample_img = np.zeros(canvas, dtype='uint8')
ori_img(sample_img)
err_dil_img(sample_img)
current_img(sample_img)
fc_img(sample_img)
filarea_img(sample_img)
# inpaint_img(sample_img)

ref_ui.mainloop()