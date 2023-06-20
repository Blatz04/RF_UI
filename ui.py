import tkinter as tk
import os
import numpy as np
import ctypes
from tkinter import filedialog, ttk
from PIL import Image, ImageTk
from main import result_sample, iterating
import random

user32 = ctypes.windll.user32
user32.SetProcessDPIAware()
Width = user32.GetSystemMetrics(0)
Height = user32.GetSystemMetrics(1)

def enable(childList):
    for child in childList:
        child['state'] = 'normal'

def toggle_theme():
    if var.get():
        ref_ui.tk.call("set_theme", "light")
    else:
        ref_ui.tk.call("set_theme", "dark")    

def disableChildren(parent):
    for child in parent.winfo_children():
        wtype = child.winfo_class()
        if wtype not in ('Frame','Labelframe','TFrame','TLabelframe', 'TToplevel'):
            child.configure(state='disable')
        else:
            disableChildren(child)

def enableChildren(parent):
    for child in parent.winfo_children():
        wtype = child.winfo_class()
        if wtype not in ('Frame','Labelframe','TFrame','TLabelframe'):
            child.configure(state='normal')
        else:
            enableChildren(child)
            
'''UI Settings'''

ref_ui = tk.Tk()

ref_ui.title("Reflective Filter")
ref_ui.iconbitmap("C_dim.ico")
ref_ui.geometry(f"{int(Width * 0.5)}x{int(Height * 0.85)}")
ref_ui.update()
ui_h = ref_ui.winfo_height()
ref_ui.resizable(width=False, height=False)

ref_ui.tk.call("source", "Azure-ttk-theme-main/azure.tcl")
ref_ui.tk.call("set_theme", "dark")

'''Frame1'''
frame1 = ttk.Frame(ref_ui)
frame1.pack()

curr_img_n = 0
curr_img = tk.IntVar(value=curr_img_n)
cancel_var = tk.BooleanVar(value=0)

def cancel_updateValue():
    cancel_var.set(value=1)

popup = tk.Toplevel(ref_ui)
popup.title("~")
popup.geometry("150x60")
popup.iconbitmap("C_dim.ico")
progress_bar = ttk.Progressbar(popup, variable=curr_img)
progress_bar.pack(pady=5)
cancel_button = ttk.Button(popup, text="Stop", command=cancel_updateValue)
cancel_button.pack()
popup.withdraw()

'''Frame1'''

def get_from_explorer():
    global folder_path, sample_img_path
    folder_path = filedialog.askdirectory(initialdir = "/",
										title = "Select Folder Directory")
    frame1_entry.delete(0, tk.END)
    frame1_entry.insert(tk.END, folder_path)

def check_folder_path():
    if frame1_entry.get() == "":
        if not os.path.exists(frame1_sample_entry.get()):
            return tk.messagebox.showinfo(title="Folder/Path didn't exist", message=f"Please provide a valid path to a Folder containing images or to an image file {formats}")
        elif not any(frame1_sample_entry.get().lower().endswith(format.lower()) for format in formats):
            return tk.messagebox.showinfo(title="Invalid Image Path", message=f"Please provide a valid path to an image file {formats}")
        frame1_entry.delete(0, tk.END)
        frame1_entry.insert(tk.END, os.path.dirname(frame1_sample_entry.get()))
    elif not os.path.isdir(frame1_entry.get()):
        return tk.messagebox.showinfo(title="Invalid Folder Path", message="Please provide a valid folder path")
    else:
        matching_files = [filename for filename in os.listdir(frame1_entry.get()) if any(filename.lower().endswith(format.lower()) for format in formats)]
        if matching_files:
            random_file = random.choice(matching_files)
            sample_img_path = os.path.join(frame1_entry.get(), random_file).replace("\\", "/")
            frame1_sample_entry.delete(0, tk.END)
            frame1_sample_entry.insert(tk.END, sample_img_path)
        else:
            # Handle the case when no matching files are found
            tk.messagebox.showinfo(title="No matching files", message=f"No files found in the folder with supported formats {formats}")

def load_sample():
    global img, sample_img, bg_filename, n_img
    n_img = 0
    if not check_folder_path():      
        for filename in os.listdir(frame1_entry.get()):
            if any(filename.lower().endswith(format.lower()) for format in formats):
                n_img += 1
        frame1_var1.set(value=f'Images: {n_img}')
        sample_img = Image.open(frame1_sample_entry.get())
        #sample_img = sample_img.resize((sample_img.size[0]//6,sample_img.size[1]//6), resample=Image.Resampling.NEAREST)
        # Split the full path into directory and filename
        image_directory, image_filename = os.path.split(frame1_sample_entry.get())
        # Split the filename into name and extension
        image_name, image_extension = os.path.splitext(image_filename)
        #bg_filename = f"{image_name}_extra{image_extension}"
        #print(bg_filename)
        img = sample_img.resize(canvas, resample=Image.Resampling.NEAREST)
        img = np.array(sample_img)
        frame1_entry_size_w['state'] = 'normal'
        frame1_entry_size_h['state'] = 'normal'
        frame1_entry_size_w.delete(0, tk.END)
        frame1_entry_size_h.delete(0, tk.END)
        frame1_entry_size_w.insert(tk.END, f"{img.shape[1]}")
        frame1_entry_size_h.insert(tk.END, f"{img.shape[0]}")
        frame1_entry_size_h['state'] = 'readonly'
        rz_img = resize_sample(sample_img)
        current_img(result_sample(rz_img))

def show_unresized():
    Image.fromarray(result_sample(sample_img)).show()

def resize_sample(img):
    img = img.resize(canvas, resample=Image.Resampling.NEAREST)
    return img

def get_all_info():
    img_list = []
    bg_img_filenames = []
    ori_path = frame1_entry.get()
    for filename in os.listdir(frame1_entry.get()):
            if any(filename.lower().endswith(format.lower()) for format in formats):
                img_list.append(filename)
                # Split the filename into name and extension
                image_name, image_extension = os.path.splitext(filename)
                bg_filename = f"{image_name}_bg_mask{image_extension}"
                bg_img_filenames.append(bg_filename)
    #print(img_list, bg_img_filenames)
    out_path = os.path.dirname(frame1_sample_entry.get()) + '/rf_' + os.path.basename(frame1_entry.get())
    yes_no =  tk.messagebox.askokcancel(title="Start Iterating Process?", message=f'''This will start to process every image in the folder, with the output path "{out_path}" (will create a directory if didn't exist).
Number of images: {len(img_list)} with Image Masks: {len(bg_img_filenames)}''')
    if yes_no:
        iterating(img_list, bg_img_filenames, ori_path, out_path)
    

def current_img(img):
    pil_img = Image.fromarray(np.uint8(img))
    im = ImageTk.PhotoImage(pil_img)
    current_blank.configure(image=im)
    current_blank.image = im
    current_blank.grid(column=1,row=2,pady=10)
    current_blank['state'] = 'normal'

'''Variables'''
frame1_var1 = tk.StringVar(value='Images: ~')
    
'''Labels'''
frame1_label_folder = ttk.Label(frame1, text="Input Folder Path")
frame1_label_folder.grid(column=0,row=0,sticky='e',padx=(0,20))
frame1_label_ipath = ttk.Label(frame1, text="or Image Path", )
frame1_label_ipath.grid(column=0,row=1,sticky='e',padx=(0,20))
frame1_label_curr = ttk.Label(frame1, text="Sample Result", font='bold')
frame1_label_curr.grid(column=1,row=3)
current_blank = ttk.Label(frame1, background='black')
frame1_label_size = ttk.Label(frame1, text='''Output Rescale
Based on Width''')
frame1_label_size.grid(column=3,row=3,pady=10)
frame1_label_size_e = ttk.Label(frame1, text='''Both unresized sample and output images will follow this dimensions''', wraplength=100)
frame1_label_size_e.grid(column=3,row=6,pady=10)
frame1_label_size_h = ttk.Label(frame1, text="H", font='bold')
frame1_label_size_h.grid(column=4,row=5,sticky='w')
frame1_label_size_w = ttk.Label(frame1, text="W", font='bold')
frame1_label_size_w.grid(column=4,row=4,sticky='w')
frame1_label_images = ttk.Label(frame1, textvariable=frame1_var1, font='bold')
frame1_label_images.grid(column=3,row=2)

'''Buttons'''
frame1_pick_folder = ttk.Button(frame1, text="Pick Folder", width=15, command=get_from_explorer)
frame1_pick_folder.grid(column=3,row=0,padx=10)
frame1_load_img = ttk.Button(frame1, text="Load One Sample\n      From Path", width=15, command=load_sample)
frame1_load_img.grid(column=3,row=1,padx=10)
frame1_start = ttk.Button(frame1, text="Start", command=get_all_info)
frame1_start.grid(column=1,row=4)
frame1_show_unresized = ttk.Button(frame1, text="Show Unresized\n       Sample", compound='center', command=show_unresized)
frame1_show_unresized.grid(column=0,row=2, sticky='w')

'''Entry'''
frame1_entry = ttk.Entry(frame1, width=25)
frame1_entry.grid(column=1,row=0,pady=10)
frame1_sample_entry = ttk.Entry(frame1, width=25)
frame1_sample_entry.grid(column=1,row=1)

def get_image_dimensions(event):
    basewidth = int(frame1_entry_size_w.get())
    wpercent = (basewidth/float(img.shape[1]))
    hsize = int((float(img.shape[0])*float(wpercent)))
    frame1_entry_size_h['state'] = 'normal'
    frame1_entry_size_h.delete(0, tk.END)
    frame1_entry_size_h.insert(tk.END, hsize)
    frame1_entry_size_h['state'] = 'readonly'
    
frame1_entry_size_h = ttk.Entry(frame1, width=10)
frame1_entry_size_h.grid(column=3,row=5)
frame1_entry_size_w = ttk.Entry(frame1, width=10)
frame1_entry_size_w.grid(column=3,row=4)
frame1_entry_size_w.bind('<Return>', get_image_dimensions)

'''Checkbuttons'''
var = tk.IntVar(value=0)
theme = ttk.Checkbutton(frame1, text="Theme", variable=var, offvalue=0, onvalue=1, command=toggle_theme, style='Switch.TCheckbutton')
theme.grid(column=0,row=10,pady=30,sticky='w')

current_blank['state'] = 'disable'
frame1_entry_size_h['state'] = 'disable'
frame1_entry_size_w['state'] = 'disable'

'''Etc.'''
canvas = [300,300]
formats = (".jpg", ".jpeg", ".png")
sample_img = np.zeros(canvas, dtype='uint8')
current_img(sample_img)
ref_ui.eval('tk::PlaceWindow . center')

ref_ui.mainloop()