import cv2 as cv
import tkinter as tk
import os
import numpy as np
from tkinter import filedialog, colorchooser, ttk
from PIL import Image, ImageTk
from skimage import measure
from skimage.restoration import inpaint

'''Functions'''

def enable(childList):
    for child in childList:
        child['state'] = 'normal'
    frame3_scale_erroded['state'] = 'disable'
    frame3_scale_dilated['state'] = 'disable'
    frame3_var1.set(value=0)
    frame3_var2.set(value=0)
    frame4_scale_filarea['state'] = 'disable'
    frame5_scale_inpaint['state'] = 'disable'
    
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
ref_ui.update()
ui_h = ref_ui.winfo_height()
#ref_ui.resizable(width=False, height=False)

ref_ui.tk.call("source", "Azure-ttk-theme-main/azure.tcl")
ref_ui.tk.call("set_theme", "dark")

'''Left Part'''
left_part = ttk.Frame(ref_ui)
left_part.pack(side="left", anchor='n')

'''Border1'''
border1 = tk.Frame(ref_ui, bg='#AAAAAA', width=5, height=ui_h)
border1.pack(side='left',anchor='n')

'''Center Part'''
center_part = ttk.Frame(ref_ui)
center_part.pack(side="left", anchor='n')

'''Border2'''
border2 = tk.Frame(ref_ui, bg='#AAAAAA', width=5, height=ui_h)
border2.pack(side='left',anchor='n')

'''Right Part'''
right_part = ttk.Frame(ref_ui)
right_part.pack(side="left", anchor='n', padx=10)


'''Frame1'''

def OpenExplorer():
    global folder_path
    folder_path = filedialog.askdirectory(initialdir = "/",
										title = "Select Folder Directory")
    frame1_entry.delete(0, tk.END)
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
        frame1_sample_entry.delete(0, tk.END)
        frame1_sample_entry.insert(tk.END, sample_img_path)
        return
    return ttk.messagebox.showwarning(title="No images found", message="Directory didn't contain any supported images")

def load_sample():
    global id, img, sample_img
    if not os.path.exists(frame1_sample_entry.get()):
        return ttk.messagebox.showwarning(title="Folder/Path didn't exist", message="Please enter folder path cointaining the image")
    frame1_entry.delete(0, tk.END)
    frame1_entry.insert(tk.END, os.path.dirname(frame1_sample_entry.get()))
    sample_img = cv.imread(frame1_sample_entry.get())
    img = cv.resize(sample_img, canvas, interpolation=cv.INTER_CUBIC)
    img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
    enable(frame2.winfo_children())
    ori_img(img)
    err_dil_img(img)
    current_img(img)
    cf_image(img)
    filarea_img(img)
    inpaint_img(img)

def color_pick():
    color = colorchooser.askcolor(title="Pick Color")
    return color
    
def ori_img(img):
    im = Image.fromarray(img)
    imTk = ImageTk.PhotoImage(image=im)
    blank.configure(image=imTk)
    blank.image = imTk
    blank.grid(column=1,row=3,pady=10)

frame1 = ttk.Frame(left_part)
frame1.grid(column=0,padx=10)

'''Labels'''
frame1_label_folder = ttk.Label(frame1, text="Folder Path")
frame1_label_folder.grid(column=0,row=0,sticky='e',padx=(0,5))
frame1_label_sample = ttk.Label(frame1, text="Sample Image Path", )
frame1_label_sample.grid(column=0,row=1,sticky='e',padx=(0,5))
frame1_label_ori = ttk.Label(frame1, text="Original Image", font='bold')
frame1_label_ori.grid(column=1,row=4)
blank = ttk.Label(frame1, background='black')
#frame1_label_info = ttk.Label(frame1, text=
#'You can directly put the Sample Image Path.The folder of the image will be assumed as the main folder containing the rest of the image', justify="left", wraplength=130)
#frame1_label_info.grid(column=2,row=3,columnspan=2)

'''Buttons'''
frame1_pick_folder = ttk.Button(frame1, text="Pick Folder", width=15, command=OpenExplorer)
frame1_pick_folder.grid(column=3,row=0,padx=10)
frame1_load_img = ttk.Button(frame1, text="Load One Sample\n From The Folder", width=15, command=load_sample_path)
frame1_load_img.grid(column=3,row=1,padx=10)
frame1_load_sample = ttk.Button(frame1, text="Load Sample Image", compound='center',command=load_sample)
frame1_load_sample.grid(column=0,row=3)

'''Entry'''
frame1_entry = ttk.Entry(frame1, width=25)
frame1_entry.grid(column=1,row=0,pady=10)
frame1_sample_entry = ttk.Entry(frame1, width=25)
frame1_sample_entry.grid(column=1,row=1)
frame1_sample_entry.insert(tk.END, "H:/Document/VS Code/RF_UI/DSC09578.JPG")

'''Frame1_2'''

def current_img(img):
    try:
        im = Image.fromarray(img)
    except:
        im = Image.fromarray((img * 255).astype(np.uint8))
    imTk = ImageTk.PhotoImage(image=im)
    current_blank.configure(image=imTk)
    current_blank.image = imTk
    current_blank.grid(column=1,row=5,pady=10)

'''Labels'''
frame1_label_grey = ttk.Label(frame1, text="Current Result", font='bold')
frame1_label_grey.grid(column=1,row=6)
current_blank = ttk.Label(frame1, background='black')
frame1_iterate_all = ttk.Button(frame1, text="Iterate All", compound='center')
frame1_iterate_all.grid(column=0,row=5)

'''Frame2'''

def cf_image(img):
    im = Image.fromarray(img)
    imTk = ImageTk.PhotoImage(image=im)
    cf_blank.configure(image=imTk)
    cf_blank.image = imTk
    cf_blank.grid(column=1,row=1,padx=(0,10),pady=10,columnspan=3)

def cf_filter():
    global cf
    brown_lo=np.array([color_low[0][0],color_low[0][1],color_low[0][2]])
    brown_hi=np.array([color_hi[0][0],color_hi[0][1],color_hi[0][2]])
    cf=cv.inRange(img,brown_lo,brown_hi)
    current_img(cf)
    cf_image(cf)
    enable(frame3.winfo_children())
    enable(frame4.winfo_children())
    enable(frame5.winfo_children())
    err_dil_updateValue('<Return>')
    #filarea_updateValue('<Return>')
    #inpaint_updateValue('<Return>')
        
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
            cf_filter()
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
            cf_filter()
    except NameError:
        pass

frame2 = ttk.Frame(center_part)
frame2.grid(column=0,row=0,sticky='w',padx=5)

'''Labels'''
frame2_label_grey = ttk.Label(frame2, text="Color Filtered Image", font='bold')
frame2_label_grey.grid(column=1,row=2,pady=10,columnspan=3)
cf_blank = ttk.Label(frame2, background='black')
frame2_hi_color = tk.Label(frame2, background=None, width=5, height=2)
frame2_hi_color.grid(column=1,row=3)
frame2_low_color = tk.Label(frame2, background=None, width=5, height=2)
frame2_low_color.grid(column=3,row=3)
#frame2_cf_info = ttk.Label(frame2, text=
#'Pick range of color to remove correspond to the reflection. White is Higest and Dark is Lowest. Color is treated as RGB color scheme, so carefull to not flip the maximum and minimum picked color', justify="left", wraplength=380)
#frame2_cf_info.grid(column=0,row=0,columnspan=5)

'''Buttons'''
frame2_hi_pick = ttk.Button(frame2, text='Pick Maximum\n      Color', command=hi_change)
frame2_hi_pick.grid(column=0,row=3)
frame2_low_pick = ttk.Button(frame2, text='Pick Minimum\n      Color', command=low_change)
frame2_low_pick.grid(column=4,row=3)

for child in frame2.winfo_children():
    child['state'] = 'disable'

'''Frame3'''

def err_dil_img(img):
    im = Image.fromarray(img)
    imTk = ImageTk.PhotoImage(image=im)
    err_dil_blank.configure(image=imTk)
    err_dil_blank.image = imTk
    err_dil_blank.grid(column=1,row=4,padx=30,pady=10)

def err_dil_updateValue(event):
    global dilated
    n = frame3_var3.get()
    m = frame3_var4.get()
    erroded = cv.erode(cf, None, iterations=n)
    dilated = cv.dilate(erroded, None, iterations=m)
    err_dil_img(dilated)
    current_img(dilated)
    filarea_updateValue('<Return>')
    #inpaint_updateValue('<Return>')

def frame3_checked():
    if frame3_var1.get():
        frame3_scale_erroded['state'] = 'normal'
        frame3_scale_erroded.bind("<B1-Motion>", err_dil_updateValue)
    if frame3_var2.get():
        frame3_scale_dilated['state'] = 'normal'
        frame3_scale_dilated.bind("<B1-Motion>", err_dil_updateValue)
    if not frame3_var1.get():
        frame3_var3.set(value=0)
        err_dil_updateValue('<Return>')
        frame3_scale_erroded['state'] = 'disable'
        frame3_scale_erroded.unbind("<B1-Motion>")
    if not frame3_var2.get():
        frame3_var4.set(value=0)
        err_dil_updateValue('<Return>')
        frame3_scale_dilated['state'] = 'disable'    
        frame3_scale_dilated.unbind("<B1-Motion>") 

frame3 = ttk.Frame(center_part)
frame3.grid(column=0,row=1, sticky='w')

'''Vars'''
frame3_var1 = tk.BooleanVar(value=0)
frame3_var2 = tk.BooleanVar(value=0)
frame3_var3 = tk.IntVar()
frame3_var4 = tk.IntVar()

'''Labels'''
frame3_label_grey = ttk.Label(frame3, text="Erroded/Dilated Image", font='bold')
frame3_label_grey.grid(column=1,row=5)
err_dil_blank = ttk.Label(frame3, background='black')

'''Entry'''
frame3_entry_erroded = ttk.Entry(frame3, width=5, justify="center", textvariable=frame3_var3)
frame3_entry_erroded.grid(column=2,row=6)
frame3_entry_dilated = ttk.Entry(frame3, width=5, justify="center", textvariable=frame3_var4)
frame3_entry_dilated.grid(column=2,row=7)
    
def frame3_var3_updateValue(event):
    value = float(event)
    if int(value) != value:
        frame3_var3.set(round(value))

def frame3_var4_updateValue(event):
    value = float(event)
    if int(value) != value:
        frame3_var4.set(round(value))
        
'''Scales'''
frame3_scale_erroded = ttk.Scale(frame3, from_=0, to_=25, var=frame3_var3, command=frame3_var3_updateValue, length=150, orient="horizontal")
frame3_scale_erroded.grid(column=1,row=6)
frame3_scale_dilated = ttk.Scale(frame3, from_=0, to_=25, var=frame3_var4, command=frame3_var4_updateValue, length=150, orient="horizontal")
frame3_scale_dilated.grid(column=1,row=7)

'''Checkboxes'''
frame3_checkbox_erroded = ttk.Checkbutton(frame3, text="Erroded", variable=frame3_var1, command=frame3_checked)
frame3_checkbox_erroded.grid(column=0,row=6, sticky='w')
frame3_checkbox_dilated = ttk.Checkbutton(frame3, text="Dilated", variable=frame3_var2, command=frame3_checked)
frame3_checkbox_dilated.grid(column=0,row=7, sticky='w')

for child in frame3.winfo_children():
    child["state"] = 'disable'

'''Frame4'''

def filarea_img(img):
    im = Image.fromarray(img)
    imTk = ImageTk.PhotoImage(image=im)
    filarea_blank.configure(image=imTk)
    filarea_blank.image = imTk
    filarea_blank.grid(column=0,row=0,padx=60,pady=10,columnspan=4)

def filarea_updateValue(event):
    global filarea
    labels = measure.label(dilated, connectivity=1, background=0)
    mask = np.zeros(dilated.shape, dtype="uint8")
    filarea = dilated
    if frame4_var1.get() == 1:
        for label in np.unique(labels):
            if label == 0:
                continue
            labelMask = np.zeros(mask.shape, dtype="uint8")
            labelMask[labels == label] = 255
            numPixels = cv.countNonZero(labelMask)
            if numPixels < frame4_var2.get():
                mask = cv.add(mask, labelMask)
        filarea = mask
    if frame4_var1.get() == 2:
        for label in np.unique(labels):
            if label == 0:
                continue
            labelMask = np.zeros(mask.shape, dtype="uint8")
            labelMask[labels == label] = 255
            numPixels = cv.countNonZero(labelMask)
            print(frame4_var2.get())
            if numPixels > frame4_var2.get():
                mask = cv.add(mask, labelMask)
        filarea = mask
    filarea_img(filarea)
    current_img(filarea)
    inpaint_updateValue('<Return>', img)

def frame4_checked():
    global frame4_var3
    if frame4_var3 == frame4_var1.get():
        frame4_var1.set(value=0)
    if frame4_var1.get() == 1:
        frame4_var2.set(value=frame4_scale_filarea.cget('to'))
        frame4_scale_filarea['state'] = 'normal'
        frame4_scale_filarea.bind("<B1-Motion>", filarea_updateValue)
    if frame4_var1.get() == 2:
        frame4_var2.set(value=frame4_scale_filarea.cget('from'))
        frame4_scale_filarea['state'] = 'normal'
        frame4_scale_filarea.bind("<B1-Motion>", filarea_updateValue)
    if frame4_var1.get() == 0:
        frame4_var2.set(value=0)
        filarea_updateValue('<Return>')
        frame4_scale_filarea['state'] = 'disable'
        frame4_scale_filarea.unbind("<B1-Motion>")
    frame4_var3 = frame4_var1.get()
    filarea_updateValue('<Return>')
        
frame4 = ttk.Frame(right_part)
frame4.grid(column=0,row=0, sticky='w')

'''Vars'''
frame4_var1 = tk.IntVar(value=0)
frame4_var2 = tk.IntVar(value=0)
frame4_var3 = 0

'''Labels'''
frame4_label_grey = ttk.Label(frame4, text="Filter Area", font='bold')
frame4_label_grey.grid(column=0,row=1,columnspan=4,pady=10)
filarea_blank = ttk.Label(frame4, background='black')

'''Entry'''
frame4_entry = ttk.Entry(frame4, width=5, justify="center", textvariable=frame4_var2)
frame4_entry.grid(column=3,row=3, sticky='e')

'''Scales'''
frame4_scale_filarea = ttk.Scale(frame4, from_=0, to_=500, variable=frame4_var2, length=175, orient="horizontal")
frame4_scale_filarea.grid(column=0,row=3,columnspan=3)
frame4_scale_filarea['state'] = 'disable'

'''Radiobuttons'''
frame4_radio_large = ttk.Radiobutton(frame4, text="Remove Large", variable=frame4_var1, value=1, command=frame4_checked)
frame4_radio_large.grid(column=0,row=2, sticky='w')
frame4_radio_small = ttk.Radiobutton(frame4, text="Remove Small", variable=frame4_var1, value=2, command=frame4_checked)
frame4_radio_small.grid(column=2,row=2, columnspan=2, sticky='e')

for child in frame4.winfo_children():
    child["state"] = 'disable'

'''Frame5'''

def inpaint_img(img):
    try:
        im = Image.fromarray(img)
    except:
        im = Image.fromarray((img * 255).astype(np.uint8))
    imTk = ImageTk.PhotoImage(image=im)
    inpaint_blank.configure(image=imTk)
    inpaint_blank.image = imTk
    inpaint_blank.grid(column=0,row=0,columnspan=3)
        

def inpaint_updateValue(event, ori=None):
    if frame5_var1.get() == 0:
        #inpaint_img(ori)
        #current_img(ori)
        pass
    if frame5_var1.get() == 1:
        inpainted = cv.inpaint(img, filarea, frame5_var2.get(), cv.INPAINT_NS)
        inpaint_img(inpainted)
        current_img(inpainted)
    if frame5_var1.get() == 2:
        inpainted = cv.inpaint(img, filarea, frame5_var2.get(), cv.INPAINT_TELEA)
        inpaint_img(inpainted)
        current_img(inpainted)
    if frame5_var1.get() == 3:
        inpainted = inpaint.inpaint_biharmonic(img, filarea, channel_axis=-1)
        inpaint_img(inpainted)
        current_img(inpainted)

def frame5_checked():
    global frame5_var3
    if frame5_var3 == frame5_var1.get():
        frame5_var1.set(value=0)
    if frame5_var1.get() == 1:
        frame5_var2.set(value=frame5_scale_inpaint.cget('from'))
        frame5_scale_inpaint['state'] = 'normal'
        frame5_scale_inpaint.bind("<B1-Motion>", inpaint_updateValue)
    if frame5_var1.get() == 2:
        frame5_var2.set(value=frame5_scale_inpaint.cget('from'))
        frame5_scale_inpaint['state'] = 'normal'
        frame5_scale_inpaint.bind("<B1-Motion>", inpaint_updateValue)
    if frame5_var1.get() == 3:
        frame5_var2.set(value=frame5_scale_inpaint.cget('from'))
        frame5_scale_inpaint['state'] = 'disable'
        frame5_scale_inpaint.unbind("<B1-Motion>")
    if frame5_var1.get() == 0:
        frame5_var2.set(value=0)
        frame5_scale_inpaint['state'] = 'disable'
        frame5_scale_inpaint.unbind("<B1-Motion>")
    inpaint_updateValue('<Return>', img)
    frame5_var3 = frame5_var1.get()

frame5 = ttk.Frame(right_part)
frame5.grid(column=0,row=1, sticky='w')

'''Vars'''
frame5_var1 = tk.IntVar(value=0)
frame5_var2 = tk.IntVar(value=0)
frame5_var3 = 0

'''Labels'''
frame5_label_grey = ttk.Label(frame5, text="Inpaint", font='bold')
frame5_label_grey.grid(column=0,row=1,columnspan=3)
inpaint_blank = ttk.Label(frame5, background='black')

'''Entry'''
frame5_entry = ttk.Entry(frame5, width=5, justify="center", textvariable=frame5_var2)
frame5_entry.grid(column=2,row=3, sticky='e')

def frame5_var2_updateValue(event):
    value = float(event)
    if int(value) != value:
        frame5_var2.set(round(value))

'''Scales'''
frame5_scale_inpaint = ttk.Scale(frame5, from_=0, to_=100, variable=frame5_var2, command=frame5_var2_updateValue, length=175, orient="horizontal")
frame5_scale_inpaint.grid(column=0,row=3,columnspan=2)
frame5_scale_inpaint['state'] = 'disable'

'''Radiobuttons'''
frame5_radio_ns = ttk.Radiobutton(frame5, text="NS", variable=frame5_var1, value=1, command=frame5_checked)
frame5_radio_ns.grid(column=0,row=2)
frame5_radio_telea = ttk.Radiobutton(frame5, text="Telea", variable=frame5_var1, value=2, command=frame5_checked)
frame5_radio_telea.grid(column=1,row=2)
frame5_radio_biharmonic = ttk.Radiobutton(frame5, text="Biharmonic", variable=frame5_var1, value=3, command=frame5_checked)
frame5_radio_biharmonic.grid(column=2,row=2)

for child in frame5.winfo_children():
    child["state"] = 'disable'

'''Etc.'''
canvas = [150,150]
formats = (".JPG", ".jpg", ".PNG", ".png")
sample_img = np.zeros(canvas, dtype='uint8')
ori_img(sample_img)
err_dil_img(sample_img)
current_img(sample_img)
cf_image(sample_img)
filarea_img(sample_img)
inpaint_img(sample_img)

ref_ui.mainloop()