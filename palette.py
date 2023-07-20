import numpy as np
import colorsys
import cv2
from PIL import Image
from colour import Color

def hsl_to_rgb(hsl_value):
    h, s, l = hsl_value
    r, g, b = colorsys.hls_to_rgb(h, l, s)
    return (int(r * 255), int(g * 255), int(b * 255))

def get_palette(pil_img, arg):
    # Copy the Image
    img = pil_img.copy()

    # Resize image to speed up processing
    img = img.resize((img.size[0]//arg.w_div,img.size[1]//arg.h_div), resample=Image.Resampling.NEAREST)

    # Reduce colors (uses k-means internally)
    paletted = img.quantize(colors=arg.colors_num, method=2)
    # paletted_rgb = paletted.convert("RGB")
    # paletted_array = np.array(paletted_rgb)
    # paletted_rgb.show()
    # Find the color that occurs most often
    palette = paletted.getpalette()

    color_counts = sorted(paletted.getcolors(), reverse=True)
    palette_index = color_counts[0][1]

    final_palette = []
    for i in range(arg.palette_num):
        palette_index = color_counts[i][1]
        palette_color = tuple(palette[palette_index*3:palette_index*3+3])
        final_palette.append(palette_color)

    return final_palette

def get_high_mid_low_rgb(palette, n=4, m=4):
    colors = []
    palette = np.divide(palette, 255.0) #convert
    num_palette = palette.shape[0]
    n_mid = 0.05 * n
    n_low = n_mid + (0.05 * m)
    for i in range(num_palette):
        high = Color(rgb=(palette[i][0],palette[i][1],palette[i][2]))
        mid = Color(rgb=(min((palette[i][0] + n_mid), 1), min((palette[i][1] + n_mid), 1), min((palette[i][2] + n_mid), 1)) )
        low = Color(rgb=(min((palette[i][0] + n_low), 1), min((palette[i][1] + n_low), 1), min((palette[i][2] + n_low), 1)) )
        high = np.multiply(high.rgb, 255)
        mid = np.multiply(mid.rgb, 255)
        low = np.multiply(low.rgb, 255)
        colors.append([high,mid,low])
    return colors

def get_low_mid_high_lightness(hsl_palette, max_l, arg):
    colors = []
    num_hsl_palette = len(hsl_palette)
    add_mid = max_l + arg.l_mid_offset
    add_high = max((add_mid + (max_l / 2)) + arg.l_max_offset, (add_mid+0.001))
    for i in range(num_hsl_palette):
        low = Color(hsl=(hsl_palette[i][0], hsl_palette[i][1], hsl_palette[i][2]))
        mid = Color(hsl=(hsl_palette[i][0], hsl_palette[i][1], min((hsl_palette[i][2] + add_mid), 1)))
        high = Color(hsl=(hsl_palette[i][0], hsl_palette[i][1], min((hsl_palette[i][2] + add_high), 1)))
        low = np.multiply(low.rgb,255)
        mid = np.multiply(mid.rgb,255)
        high = np.multiply(high.rgb,255)
        colors.append([low,mid,high])
    return colors

# def get_low_mid_high_lightness(hsl_palette, max_l, max_s, arg):
#     colors = []
#     num_hsl_palette = len(hsl_palette)
#     add_mid_l = max_l + arg.l_mid_offset
#     add_high_l = max((add_mid_l + (max_l / 2)) + arg.l_max_offset, (add_mid_l+0.001))
#     add_mid_s = max_s + 0.05
#     add_high_s = max((add_mid_s + (max_s / 2)), (add_mid_s+0.001))
#     for i in range(num_hsl_palette):
#         low = Color(hsl=(hsl_palette[i][0], hsl_palette[i][1], hsl_palette[i][2]))
#         mid = Color(hsl=(hsl_palette[i][0], min((hsl_palette[i][1] + add_mid_s), 1), min((hsl_palette[i][2] + add_mid_l), 1)))
#         high = Color(hsl=(hsl_palette[i][0], min((hsl_palette[i][1] + add_high_s), 1), min((hsl_palette[i][2] + add_high_l), 1)))
#         low = np.multiply(low.rgb,255)
#         mid = np.multiply(mid.rgb,255)
#         high = np.multiply(high.rgb,255)
#         colors.append([low,mid,high])
#     return colors

# def get_low_mid_high_lightness(hsl_palette, range_l, range_s, arg):
#     colors = []
#     num_hsl_palette = len(hsl_palette)
#     half_range_l = range_l / 2
#     half_range_s = range_s / 2
#     for i in range(num_hsl_palette):
#         low = Color(hsl=(hsl_palette[i][0], hsl_palette[i][1], hsl_palette[i][2]))
#         mid = Color(hsl=(hsl_palette[i][0], min((hsl_palette[i][1] + half_range_s), 1), min((hsl_palette[i][2] + half_range_l), 1)))
#         high = Color(hsl=(hsl_palette[i][0], min((hsl_palette[i][1] + range_s), 1), min((hsl_palette[i][2] + range_l), 1)))
#         low = np.multiply(low.rgb,255)
#         mid = np.multiply(mid.rgb,255)
#         high = np.multiply(high.rgb,255)
#         colors.append([low,mid,high])
#     return colors

def hsl_palette(palette):
    colors = []
    palette = np.divide(palette, 255.0) #normalize
    num_palette = palette.shape[0]
    for i in range(num_palette):
        hls = list((colorsys.rgb_to_hls(palette[i][0], palette[i][1], palette[i][2])))
        hsl = (hls[0], hls[2], hls[1]) #hls > hsl
        colors.append(hsl)
    return colors

def show_palette(palette, mode='RGB', color_width=20, color_height=20):
    palette_size = len(palette)
    palette_image = Image.new("RGB", (palette_size * color_width, color_height))
    for i in range(palette_size):
        for x in range(i * color_width, (i + 1) * color_width):
            for y in range(color_height):
                if mode == 'HSL':
                    palette_image.putpixel((x, y), hsl_to_rgb(palette[i]))
                    continue
                palette_image.putpixel((x, y), palette[i])
    return palette_image