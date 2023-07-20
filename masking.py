import numpy as np
import cv2 as cv
import colorsys
from cv2 import inRange, bitwise_or, bitwise_and
from palette import get_palette, get_low_mid_high_lightness, hsl_palette, show_palette
from PIL import Image
from rembg.bg import remove
from rembg.session_factory import new_session
from skimage import measure
from inpainting import reduce_saturation_and_lightness
from frr import FastReflectionRemoval

def get_background_mask(img):
    #session = new_session("isnet-general-use")
    return remove(img, only_mask=True)

def rem_bg(img):
    session = new_session("isnet-general-use")
    return remove(img, session=session, bgcolor=(0, 0, 0, 0))

def is_alpha_mask(mask):

    if len(mask.shape) >= 3 and mask.shape[2] == 4:
        return True
    else:
        return False

def color_filter(img, color):
    cf_low=np.array([color[1][2],color[1][1],color[1][0]]) #rgb > bgr
    cf_high=np.array([color[2][2],color[2][1],color[2][0]]) #rgb > bgr
    cf=inRange(img[:, :, :3],cf_low,cf_high)
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

def combine_masks(masks, arg):
    # Create an empty confidence map
    confidence_map = np.zeros_like(masks[0], dtype=np.float32)

    # Accumulate confidence values from each mask
    for mask in masks:
        if np.sum(mask) > 0:
            confidence_map += mask.astype(np.float32)
            
    # Threshold the confidence map to obtain the final binary mask
    threshold = np.max(confidence_map) * arg.mask_confidence  # Adjust the threshold as needed
    final_mask = (confidence_map > threshold).astype(np.uint8) * 255
    return final_mask

def frr(img, arg):
    # Convert the image to float32 and normalize the pixel values
    image_normalized = np.array(img).astype(np.float32) / 255.0
    # instantiate the algoroithm class
    alg = FastReflectionRemoval(h = arg.fast_reflection)
    # run the algorithm and get result of shape (H, W, C)
    dereflected_img = alg.remove_reflection(image_normalized)
    # Convert the output array to the correct data type
    dereflected_img = (dereflected_img * 255).astype(np.uint8)
    #dereflected_img = cv.cvtColor(dereflected_img, cv.COLOR_BGR2RGB)
    #Image.fromarray(dereflected_img).show()
    return dereflected_img

def convert(img, bg_path, save_bg_mask, n, arg):
    img_ori = img.copy()
    # img_ori.save("H:/Document/VS Code/RF_UI/uh/ori.png") if n == 0 else None
    
    #img.show() #show image
    img = frr(img, arg)
    # Image.fromarray(img).save("H:/Document/VS Code/RF_UI/uh/img_frr.png")  if n == 0 else None
    img_bg_rem = rem_bg(img).copy()
    # img_bg_rem.show() #show removed background
    # Image.fromarray(img_bg_rem).save(f"H:/Document/VS Code/RF_UI/uh/img_bg_rem_{n}.png")
    bg_mask = Image.fromarray(img_bg_rem).split()[3]  # Extract the alpha channel (index 3)
    bg_mask = np.array(bg_mask)
    if save_bg_mask:
        Image.fromarray(bg_mask).save(bg_path)
        
    # Extract the alpha channel
    alpha_channel = img_bg_rem[:, :, 3]

    # Create a mask for the pixels within the desired opacity range
    #print(arg.alpha_range)
    mask = np.logical_and(alpha_channel >= arg.alpha_range[0], alpha_channel <= arg.alpha_range[1])

    # Apply the mask to the RGBA image
    filtered_image = np.zeros_like(img_bg_rem)
    filtered_image[mask] = img_bg_rem[mask]

    # Show the resulting filtered image
    # Image.fromarray(filtered_image.astype(np.uint8)).show()
    
    img_bg_rem = filtered_image
    
    # Convert the filtered image into a binary mask
    binary_bg_mask = np.where(img_bg_rem[:, :, 3] > 0, 255, 0).astype(np.uint8)
    
    img_bg_rem = Image.fromarray(img_bg_rem)
    #bg_mask.show()
    # Convert the alpha channel to a grayscale mask
    #alpha_mask = np.array(alpha_channel)
    palette = get_palette(img_bg_rem, arg)
    #show_palette(palette).show() #show palette    
    # show_palette(palette).save(f"H:/Document/VS Code/RF_UI/uh/pallete_{n}.jpg", quality=100)
    #bg_mask = get_background_mask(img)
    #bg_mask.show()
    
    # binary_bg_mask = np.where(bg_mask > arg.grey_lim, 255, 0).astype(np.uint8)
    #bg_mask = np.array(bg_mask)
    # Filter the values outside the desired range
    #binary_bg_mask = np.where((bg_mask >= arg.grey_range[0]) & (bg_mask <= arg.grey_range[1]), 255, 0).astype(np.uint8)
    Image.fromarray(binary_bg_mask).show()  if arg.show_filtered_bg_mask else None #show removed background mask grey filtered
    # Image.fromarray(binary_bg_mask).save(f"H:/Document/VS Code/RF_UI/uh/binary_bg_mask_{n}.jpg", quality=100)

    #img_bg_rem = np.array(img_bg_rem)
    #img = np.array(img)
    palette = hsl_palette(palette)
    numpy_palette = np.array(palette)
    
    max_l = numpy_palette[:,2].max()
    # avg_l = numpy_palette[:,2].mean()
    # range_l = max_l - avg_l
    # max_s = numpy_palette[:,1].max()
    # avg_s = numpy_palette[:,1].mean()
    # range_s = max_s - avg_s
    # palette = get_low_mid_high_lightness(palette, range_l, range_s, arg)
    # palette = get_low_mid_high_lightness(palette, max_l, max_s, arg)
    palette = get_low_mid_high_lightness(palette, max_l, arg)

    masks = []
    for i in range(len(palette)):
        mask = color_filter(img, palette[i])
        #Image.fromarray(mask).show()
        masks.append(mask)

    # Convert the masks to NumPy arrays
    #numpy_masks = [np.array(mask) for mask in masks]
    #combine_masks(masks)
    # # Combine the masks using bitwise OR operation
    # combined_mask = numpy_masks[0]  # Start with the first mask
    # for mask in numpy_masks[1:]:
    #     combined_mask = bitwise_or(combined_mask, mask)

    confidence_mask = combine_masks(masks, arg)
    #Image.fromarray(confidence_mask).show() #show confidence mask
    # Image.fromarray(confidence_mask).save(f"H:/Document/VS Code/RF_UI/uh/confidence_mask_{n}.jpg", quality=100)
    and_mask = bitwise_and(confidence_mask, binary_bg_mask)
    filtered = filter_small_area(and_mask, arg)
    Image.fromarray(filtered).show() if arg.show_final_mask else None #show final mask
    # Image.fromarray(filtered).save(f"H:/Document/VS Code/RF_UI/uh/filtered_{n}.jpg", quality=100)

    return reduce_saturation_and_lightness(img, filtered, n, arg)