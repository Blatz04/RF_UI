import os
import ui
import sys
#import time
import numpy as np
import concurrent.futures
from masking import convert
from PIL import Image
from rembg import new_session

def process_one(img, save_img_path, save_bg_path, curr_img, arg):
    # Start the timer
    #start_time = time.time()
    converted = img
    for i in range(arg.repeats):
        if i == 0:
            print(f"Currently processing: {curr_img} Repeat:{i}")
            converted = convert(converted, save_bg_path, True, i, arg)
        else:
            print(f"Currently processing: {curr_img} Repeat:{i}")
            converted = convert(Image.fromarray(converted), save_bg_path, True, i, arg)
    # Image.fromarray(converted).show()
    if arg.save_as_png:
        save_img_path = save_img_path.replace(".jpg", ".png")
        Image.fromarray(converted).save(save_img_path, "PNG")
    else:
        Image.fromarray(converted).save(save_img_path, "JPEG", quality=100)
    print(f"{curr_img} - Finished")
    # Calculate the elapsed time
    #elapsed_time = time.time() - start_time

    # Print the elapsed time
    #print(f"Elapsed time: {elapsed_time} seconds")

def get_half_cpu():
    half_thread = int(os.cpu_count()/4)
    return half_thread

def iterating(img_list, bg_img_filenames, ori_path, out_path, arg):
    if not os.path.exists(out_path):
            os.mkdir(out_path)
    bg_out_path = "rf_bg"
    bg_out_path = os.path.join(out_path, bg_out_path)
    bg_out_path = bg_out_path.replace("\\", "/")
    if not os.path.exists(bg_out_path):
            os.mkdir(bg_out_path)
    with concurrent.futures.ThreadPoolExecutor(max_workers=get_half_cpu()) as executor:
        # Submit tasks for each image to be processed
        futures = []
        for i in range(len(img_list)):
            img_path = os.path.join(ori_path, img_list[i])
            img_path = img_path.replace("\\", "/")
            save_bg_path = os.path.join(bg_out_path, bg_img_filenames[i])
            save_bg_path = save_bg_path.replace("\\", "/")
            save_img_path = os.path.join(out_path, img_list[i])
            save_img_path = save_img_path.replace("\\", "/")
            img = Image.open(img_path)
            img = img.resize((img.size[0]//arg.w_div,img.size[1]//arg.h_div), resample=Image.Resampling.LANCZOS)
            future = executor.submit(process_one, img, save_img_path, save_bg_path, img_list[i], arg)
            futures.append(future)
            
        # Wait for all tasks to complete and retrieve results
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
    print("Done!")

if __name__ == "__main__":
    model_path = os.path.join("H:\Document\VS Code\RF_UI", "model")
    #model_path = os.path.join(sys._MEIPASS, "model")
    os.environ["U2NET_HOME"] = model_path
    ui.run()