import cv2 as cv
import numpy as np
from scipy.ndimage import grey_dilation

# img = Image.open("DSC06342.JPG")
# mask = Image.open("tes.JPG")
# mask.show()
# img = img.resize((img.size[0]//2,img.size[1]//2), resample=Image.Resampling.LANCZOS)
# mask = np.array(mask).astype(np.float32)

def do_inpaint(img, mask, radius=1, n=3, m=3):
    #mask = mask.resize((mask.size[0]//6,mask.size[1]//6), resample=Image.Resampling.NEAREST)

    # # Apply convolution with the blur kernel
    # smoothed_mask = mask #convolve(mask, )

    dilated_mask = grey_dilation(mask, size=(n, m))  # Adjust the size as needed
    #dilated_mask_2 = grey_dilation(mask, size=(2, 2))  # Adjust the size as needed
    # #blurred_mask = gaussian_filter(mask, sigma=100.0)
    # smoothed_mask_img = Image.fromarray(smoothed_mask)
    # smoothed_mask_img.show()

    # img.show()
    # Image.fromarray(mask).show()
    # Image.fromarray(dilated_mask).show()

    img = np.array(img).astype(np.float32)
    #inpainted = inpaint.inpaint_biharmonic(img, dilated_mask, split_into_regions=False, channel_axis=-1)
    
    # Convert the image to the appropriate format for OpenCV
    img_bgr = cv.cvtColor(img, cv.COLOR_RGB2BGR)

    # Convert the mask to a single-channel image (grayscale)
    mask_gray = (dilated_mask * 255).astype(np.uint8)
    
    # Ensure the image and mask have compatible data types and channel configurations
    img_bgr = img_bgr.astype(np.uint8)
    mask_gray = mask_gray.astype(np.uint8)
    
    #inpainted = inpaint.inpaint_biharmonic(img, dilated_mask_2, split_into_regions=False, channel_axis=-1)
    
    # Apply patch-based inpainting
    inpainted_2 = cv.inpaint(img_bgr, mask_gray, radius, cv.INPAINT_TELEA)
    inpainted_2_rgb = cv.cvtColor(inpainted_2, cv.COLOR_BGR2RGB)
    
    # Convert inpainted array to PIL Image
    #Image.fromarray(np.uint8(inpainted)).show()
    #Image.fromarray(inpainted_2_rgb).show()
    return(inpainted_2_rgb)
