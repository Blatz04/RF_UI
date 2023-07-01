import os
import random
import ctypes
import argparse
import numpy as np
import tkinter as tk
from tkinter import filedialog, ttk
from PIL import Image
from main import iterating
    
def run():
    user32 = ctypes.windll.user32
    user32.SetProcessDPIAware()
    Width = user32.GetSystemMetrics(0)
    Height = user32.GetSystemMetrics(1)

    def connectivity_type(value):
        value = int(value)
        if value not in [1, 2]:
            raise argparse.ArgumentTypeError("Connectivity must be 1 or 2")
        return value

    def positive_integer_type(value):
        value = int(value)
        if value <= 0:
            raise argparse.ArgumentTypeError("Must be a positive integer (> 0)")
        return value
    
    def non_negative_integer_type(value):
        value = int(value)
        if value < 0:
            raise argparse.ArgumentTypeError("Must be a non-negative integer (>= 0)")
        return value
    
    def update_arg():
        global arg
        input_string = frame2_entry.get()

        # Split the input string into individual arguments
        arguments_list = input_string.split()

        # Create an argument parser
        parser = argparse.ArgumentParser()
        
        # Add the arguments that correspond to the attributes of the arg object
        parser.add_argument('-a', '--w_div', type=positive_integer_type, default=1, help='value for the image width to be divided with')
        parser.add_argument('-b', '--h_div', type=positive_integer_type, default=1, help='value for the image height to be divided with')
        parser.add_argument('-c', '--connectivity', type=connectivity_type, default=2, help='Connectivity, set to 1 or 2')
        parser.add_argument('-p', '--min_pix', type=non_negative_integer_type, default=5, help='filter small pixels')
        parser.add_argument('-x', '--palette_num', type=positive_integer_type, default=2, help='how many palette to create')
        parser.add_argument('-g', '--grey_lim', type=non_negative_integer_type, default=50, help='filter gray pixels from rembg mask')
        parser.add_argument('-y', '--light_mid', type=positive_integer_type, default=3, help='mid range for light pixels')
        parser.add_argument('-z', '--light_max', type=positive_integer_type, default=7, help='max range for light pixels')
        parser.add_argument('-r', '--inpaint_rad', type=non_negative_integer_type, default=1, help='inpaint radius')
        parser.add_argument('-m', '--dil_m', type=non_negative_integer_type, default=0, help='dilate masks, value of m (mxn)')
        parser.add_argument('-n', '--dil_n', type=non_negative_integer_type, default=0, help='dilate masks, value of n (mxn)')

        try:
            # Parse the input arguments
            arg = parser.parse_args(arguments_list)
            return True
            
        except SystemExit:
            parser.print_help()
            # Optionally, you can exit the program here if desired
            # or handle the error in a different way
            return False
    
    def toggle_theme():
        if var.get():
            ref_ui.tk.call("set_theme", "light")
        else:
            ref_ui.tk.call("set_theme", "dark")    

    '''UI Settings'''

    ref_ui = tk.Tk()

    ref_ui.title("Reflective Filter")
    ref_ui.iconbitmap("C_dim.ico")
    ref_ui.geometry(f"{int(Width * 0.4)}x{int(Height * 0.35)}")
    ref_ui.update()
    ref_ui.resizable(width=False, height=False)

    ref_ui.tk.call("source", "Azure-ttk-theme-main/azure.tcl")
    ref_ui.tk.call("set_theme", "dark")

    '''Frame1'''
    frame1 = ttk.Frame(ref_ui)
    frame1.pack()
    
    '''Frame2'''
    frame2 = ttk.Frame(ref_ui)
    frame2.pack(anchor='center', side='bottom', pady=5)

    '''Frame1'''

    def get_from_explorer():
        global folder_path, random_img_path
        folder_path = filedialog.askdirectory(initialdir = "/",
                                            title = "Select Folder Directory")
        frame1_entry.delete(0, tk.END)
        frame1_entry.insert(tk.END, folder_path)

    def check_folder_path():
        if frame1_entry.get() == "":
            if not os.path.exists(frame1_random_entry.get()):
                return tk.messagebox.showinfo(title="Folder/Path didn't exist", message=f"Please provide a valid path to a Folder containing images or to an image file {formats}")
            elif not any(frame1_random_entry.get().lower().endswith(format.lower()) for format in formats):
                return tk.messagebox.showinfo(title="Invalid Image Path", message=f"Please provide a valid path to an image file {formats}")
            frame1_entry.delete(0, tk.END)
            frame1_entry.insert(tk.END, os.path.dirname(frame1_random_entry.get()))
        elif not os.path.isdir(frame1_entry.get()):
            return tk.messagebox.showinfo(title="Invalid Folder Path", message="Please provide a valid folder path")
        else:
            matching_files = [filename for filename in os.listdir(frame1_entry.get()) if any(filename.lower().endswith(format.lower()) for format in formats)]
            if matching_files:
                random_file = random.choice(matching_files)
                random_img_path = os.path.join(frame1_entry.get(), random_file).replace("\\", "/")
                frame1_random_entry.delete(0, tk.END)
                frame1_random_entry.insert(tk.END, random_img_path)
            else:
                # Handle the case when no matching files are found
                tk.messagebox.showinfo(title="No matching files", message=f"No files found in the folder with supported formats {formats}")

    def load_random():
        global img, random_img, bg_filename, n_img
        n_img = 0
        if not check_folder_path():      
            for filename in os.listdir(frame1_entry.get()):
                if any(filename.lower().endswith(format.lower()) for format in formats):
                    n_img += 1
            frame1_var1.set(value=f'Images: {n_img}')
            random_img = Image.open(frame1_random_entry.get())
            random_img = random_img.copy()

            # Split the full path into directory and filename
            image_directory, image_filename = os.path.split(frame1_random_entry.get())
            # Split the filename into name and extension
            image_name, image_extension = os.path.splitext(image_filename)

            frame1_entry_size_w['state'] = 'normal'
            frame1_entry_size_h['state'] = 'normal'
            frame1_entry_size_w.delete(0, tk.END)
            frame1_entry_size_h.delete(0, tk.END)
            frame1_entry_size_w.insert(tk.END, f"{np.array(random_img).shape[1]}")
            frame1_entry_size_h.insert(tk.END, f"{np.array(random_img).shape[0]}")
            frame1_entry_size_w['state'] = 'readonly'
            frame1_entry_size_h['state'] = 'readonly'
            frame1_start['state'] = 'normal'

    def get_all_info():
        if not update_arg():
            return tk.messagebox.showinfo(title="Invalid Input Arguments", message=f"Invalid input arguments, see printed out help or leave empty for default")
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

        out_path = os.path.dirname(frame1_random_entry.get()) + '/rf_' + os.path.basename(frame1_entry.get())
        yes_no =  tk.messagebox.askokcancel(title="Start Iterating Process?", message=f'''This will start to process every image in the folder, with the output path "{out_path}" (will create a directory if didn't exist).
    Number of images: {len(img_list)} with Image Masks: {len(bg_img_filenames)}''')
        if yes_no:
            iterating(img_list, bg_img_filenames, ori_path, out_path, arg)

    '''Variables'''
    frame1_var1 = tk.StringVar(value='Images: ~')
        
    '''Labels'''
    frame1_label_folder = ttk.Label(frame1, text="Input Folder Path")
    frame1_label_folder.grid(column=0,row=0,sticky='e',padx=(0,20))
    frame1_label_ipath = ttk.Label(frame1, text="or Image Path", )
    frame1_label_ipath.grid(column=0,row=1,sticky='e',padx=(0,20))
    frame1_label_size_h = ttk.Label(frame1, text="H", font='bold')
    frame1_label_size_h.grid(column=4,row=5,sticky='w')
    frame1_label_size_w = ttk.Label(frame1, text="W", font='bold')
    frame1_label_size_w.grid(column=4,row=4,sticky='w')
    frame1_label_images = ttk.Label(frame1, textvariable=frame1_var1, font='bold')
    frame1_label_images.grid(column=1,row=2, sticky='n', pady=10)

    '''Buttons'''
    frame1_pick_folder = ttk.Button(frame1, text="Pick Folder", width=15, command=get_from_explorer)
    frame1_pick_folder.grid(column=3,row=0,padx=10)
    frame1_load_img = ttk.Button(frame1, text="Load From Path", width=15, command=load_random)
    frame1_load_img.grid(column=3,row=1,padx=10)
    frame1_start = ttk.Button(frame1, text="Start", command=get_all_info)
    frame1_start.grid(column=1,row=4)

    '''Entry'''
    frame1_entry = ttk.Entry(frame1, width=25)
    frame1_entry.grid(column=1,row=0,pady=10)
    frame1_random_entry = ttk.Entry(frame1, width=25)
    frame1_random_entry.grid(column=1,row=1)

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

    '''Frame2'''
    var = tk.IntVar(value=0)
    theme = ttk.Checkbutton(frame2, text="Theme", variable=var, offvalue=0, onvalue=1, command=toggle_theme, style='Switch.TCheckbutton')
    theme.pack(side='left',padx=10)
    
    frame2_info = ttk.Label(frame2, text="Input Arguments Here >")
    frame2_info.pack(side='left')

    frame2_entry = ttk.Entry(frame2, width=20)
    frame2_entry.pack(side='left',padx=5,pady=(0,5))
    
    frame1_entry_size_h['state'] = 'disable'
    frame1_entry_size_w['state'] = 'disable'
    frame1_start['state'] = 'disable'

    '''Etc.'''
    formats = (".jpg", ".jpeg", ".png")
    ref_ui.eval('tk::PlaceWindow . center')

    ref_ui.mainloop()