import os
import concurrent.futures
from masking import convert
from PIL import Image

def result_sample(img, bg_path='sample.jpg', save_bg_mask=False):
    return convert(img, bg_path, save_bg_mask)

def process_one(img, save_img_path, save_bg_path):
    converted = convert(img, save_bg_path, True)
    Image.fromarray(converted).save(save_img_path)

def iterating(img_list, bg_img_filenames, ori_path, out_path):
    if not os.path.exists(out_path):
            os.mkdir(out_path)
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        # Submit tasks for each image to be processed
        futures = []
        for i in range(len(img_list)):
            print(f"Currently processing: {img_list[i]}")
            img_path = os.path.join(ori_path, img_list[i])
            img_path = img_path.replace("\\", "/")
            save_bg_path = os.path.join(out_path, bg_img_filenames[i])
            save_bg_path = save_bg_path.replace("\\", "/")
            save_img_path = os.path.join(out_path, img_list[i])
            save_img_path = save_img_path.replace("\\", "/")
            img = Image.open(img_path)
            img = img.resize((img.size[0]//9,img.size[1]//9), resample=Image.Resampling.NEAREST)
            future = executor.submit(process_one, img, save_img_path, save_bg_path)
            futures.append(future)
        # Wait for all tasks to complete
        concurrent.futures.wait(futures)
    