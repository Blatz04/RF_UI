import colorsys
import numpy as np
import cv2
from skimage.restoration import inpaint
from skimage import measure, color
from PIL import Image, ImageDraw

def reduce_saturation_and_lightness(image, mask, n, arg):
    # Iterate over each pixel in the mask
    for y in range(image.shape[0]):
        for x in range(image.shape[1]):
            if mask[y, x]:
                # Get the RGBA values for the pixel
                r, g, b = image[y, x]

                # Convert RGB to HSL
                h, l, s = colorsys.rgb_to_hls(r / 255, g / 255, b / 255)

                # Reduce the lightness value by a certain factor
                l -= arg.reduction_factor

                # Reduce the saturation value by a certain factor
                s -= arg.reduction_factor

                # Clamp the lightness and saturation values between 0 and 1
                l = np.clip(l, 0, 1)
                s = np.clip(s, 0, 1)

                # Convert HSL to RGB
                new_r, new_g, new_b = colorsys.hls_to_rgb(h, l, s)

                # Update the RGB values in the image
                image[y, x] = np.array([new_r * 255, new_g * 255, new_b * 255], dtype=np.uint8)
    
    # Visualize the edited image
    # Image.fromarray(image).show()
    # Image.fromarray(image).save(f"H:/Document/VS Code/RF_UI/uh/edited_image_{n}.jpg", quality=100)
    
    # Convert the grayscale mask to a NumPy array
    mask_array = np.array(mask)
    
    # Create an empty image to draw the contour on
    contour_image = Image.new('L', (mask.shape[1], mask.shape[0]))
    draw = ImageDraw.Draw(contour_image)

    # Find the contours in the mask
    contours = measure.find_contours(mask_array, 0)

    # Draw the contours on the contour image
    for contour in contours:
        contour = np.flip(contour, axis=1)  # Reverse x and y coordinates
        draw.line(contour.ravel().tolist(), fill=255, width=arg.contour_width)

    # Visualize the contour image
    #print(arg.contour_width)
    # contour_image.show()
    # contour_image.save(f"H:/Document/VS Code/RF_UI/uh/contour_{n}.jpg", quality=100)
    
    #Convert to numpy array
    contour_mask = np.array(contour_image)

    #Inpaint Biharmonic
    image = inpaint.inpaint_biharmonic(image.astype(np.float32), contour_mask.astype(np.uint8), channel_axis=-1, split_into_regions=False) if not arg.skip_contour else image
    # Image.fromarray(image.astype(np.uint8)).show()
    # Image.fromarray(image.astype(np.uint8)).save(f"H:/Document/VS Code/RF_UI/uh/inpaint_{n}.jpg", quality=100)
    return image.astype(np.uint8)