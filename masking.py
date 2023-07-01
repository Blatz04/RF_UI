import numpy as np
import cv2 as cv
from cv2 import inRange, bitwise_or, bitwise_and
from palette import get_palette, get_high_mid_low_lightness, hsl_palette, show_palette
from PIL import Image
from rembg import remove, new_session
from skimage import measure
from inpainting import do_inpaint

def get_background_mask(img):
    session = new_session("u2netp")
    return remove(img, session=session, only_mask=True)

def is_alpha_mask(mask):

    if len(mask.shape) >= 3 and mask.shape[2] == 4:
        return True
    else:
        return False

def color_filter(img, color):
    cf_low=np.array([color[1][2],color[1][1],color[1][0]]) #rgb > bgr
    cf_high=np.array([color[2][2],color[2][1],color[2][0]]) #rgb > bgr
    cf=inRange(img[:, :, :3],cf_low,cf_high)
    #cf=inRange(img[:, :, :3],cf_low,cf_high)
    # cf = merge((bitwise_and(img[:, :, 0], cf),
    #                 bitwise_and(img[:, :, 1], cf),
    #                 bitwise_and(img[:, :, 2], cf),
    #                 img[:, :, 3]))
    #cf = Image.fromarray(cf)
    #cf.show()
    return cf

def filter_small_area(mask, arg):
    labels = measure.label(mask, connectivity=arg.connectivity)
    props = measure.regionprops(labels)
    mask_large_clusters = np.zeros_like(labels, dtype=bool)
    for prop in props:
        if prop.area >= arg.min_pix:
            mask_large_clusters[labels == prop.label] = True
    labels_filtered = (labels * mask_large_clusters) > 0
    return labels_filtered

def convert(img, bg_path, save_bg_mask, arg):
    #img = Image.open(r"DSC06342.JPG")
    #img = Image.open(r"DSC09577.JPG")
    #img = img.resize((img.size[0]//6,img.size[1]//6), resample=Image.Resampling.NEAREST)
    palette = get_palette(img, arg.palette_num)
    bg_mask = get_background_mask(img)
    bg_mask = np.array(bg_mask)
    binary_bg_mask = np.where(bg_mask > arg.grey_lim, 255, 0).astype(np.uint8)
    if save_bg_mask:
        save_binary_bg_mask = np.where(bg_mask > 0, 255, 0).astype(np.uint8)
        Image.fromarray(save_binary_bg_mask).save(bg_path)
        #bg_mask.save(bg_path)
    #pillow_img = Image.fromarray(binary_bg_mask)
    #pillow_img.save("binary_bg_mask.jpg")
    img = np.array(img)
    palette = hsl_palette(palette)
    #print(palette)
    #show_palette(palette, 'HSL')
    #palette = get_high_mid_low_rgb(palette, 10)
    palette = get_high_mid_low_lightness(palette, arg.light_mid, arg.light_max)

    masks = []
    for i in range(len(palette)):
        #print(i)
        mask = color_filter(img, palette[i])
        masks.append(mask)

    # Convert the masks to NumPy arrays
    numpy_masks = [np.array(mask) for mask in masks]

    # Combine the masks using bitwise OR operation
    combined_mask = numpy_masks[0]  # Start with the first mask
    for mask in numpy_masks[1:]:
        combined_mask = bitwise_or(combined_mask, mask)

    and_mask = bitwise_and(combined_mask, binary_bg_mask)
    binary_mask = np.where(and_mask > 254, 255, 0).astype(np.uint8)
    #pillow_img = Image.fromarray(binary_mask)
    #pillow_img.save("binary_bg_mask2.jpg")
    # pillow_img.show()

    #mask = mask.resize((mask.size[0]//2,mask.size[1]//2), resample=Image.Resampling.NEAREST)
    #mask = np.array(mask)
    filtered = filter_small_area(and_mask, arg)

    #pillow_img = Image.fromarray(filtered)
    #pillow_img.save("tes.JPG")
    #pillow_img.show()
    #pillow_img = Image.fromarray(img)
    #pillow_img = pillow_img.convert('RGBA')
    #pillow_img.save("tes_img.png")
    #pillow_img.show()
    #pillow_img = Image.fromarray(filtered)
    #pillow_img = pillow_img.convert('RGB')
    #pillow_img.save("tes_mask.png")
    #pillow_img.show()
    
    return do_inpaint(img, filtered, arg.inpaint_rad, arg.dil_m, arg.dil_n)
    # Display the image using Matplotlib
    # plt.imshow(uh, cmap='gray')
    # plt.axis('off')  # Turn off the axis
    # plt.gca().set_frame_on(False)  # Turn off the frame
    # plt.show()