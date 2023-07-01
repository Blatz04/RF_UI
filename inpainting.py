import cv2 as cv
import numpy as np
from PIL import Image
from scipy.ndimage import grey_dilation, gaussian_filter, convolve
from skimage import restoration

def do_inpaint(img, mask, radius, m, n):

    dilated_mask = grey_dilation(mask, size=(m, n))  # Adjust the size as needed

    img = np.array(img).astype(np.float32)

    # Convert the image to the appropriate format for OpenCV
    img_bgr = cv.cvtColor(img, cv.COLOR_RGB2BGR)

    # Convert the mask to a single-channel image (grayscale)
    mask_gray = (dilated_mask * 255).astype(np.uint8)
    
    # Ensure the image and mask have compatible data types and channel configurations
    img_bgr = img_bgr.astype(np.uint8)
    mask_gray = mask_gray.astype(np.uint8)
    
    # Apply patch-based inpainting
    inpainted_2 = cv.inpaint(img_bgr, mask_gray, radius, cv.INPAINT_TELEA)
    inpainted_2_rgb = cv.cvtColor(inpainted_2, cv.COLOR_BGR2RGB)
    
    return(inpainted_2_rgb)
