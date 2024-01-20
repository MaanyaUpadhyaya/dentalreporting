import numpy as np
import cv2
import os
from PIL import Image

from PIL import ImageDraw, Image

def draw_line(image, p1, p2):
    draw = ImageDraw.Draw(image)
    draw.line([p1, p2], fill='green', width=3)
    return image

def add_text(image,pt,text_to_display):
    I1 = ImageDraw.Draw(image)
    I1.text(pt, text_to_display, fill="green")
    return image

def apply_window(pixel_array, window_center, window_width):
    window_min = window_center - window_width / 2
    window_max = window_center + window_width / 2
    pixel_array = np.clip(pixel_array, window_min, window_max)
    pixel_array = (pixel_array - window_min) / (window_max - window_min)
    pixel_array = np.clip(pixel_array, 0.0, 1.0)
    return pixel_array

def get_windowed_pixels(ds):
    window_center = ds.WindowCenter
    window_width = ds.WindowWidth
    pixel_array = ds.pixel_array
    windowed_pixel_array = apply_window(pixel_array, window_center, window_width)
    windowed_pixel_array = (windowed_pixel_array * 255).astype(np.uint8)
    return windowed_pixel_array

def convert_pixel_to_image(pixel_array):
    cv2.imwrite("temp.jpg", pixel_array)
    image = Image.open("temp.jpg")
    image = image.convert('RGB')
    return image

def find_panoramic_view_image(selected_folder):
    for folder_name in ["images", "other images"]:
        folder_path = os.path.join(selected_folder, folder_name)
        if os.path.exists(folder_path):
            for root, _, files in os.walk(folder_path):
                for file_name in files:
                    if file_name.lower() == "panaromic view.jpg" or file_name.lower() == "panoramic view.png" or file_name.lower() == "panaroma.png" or file_name.lower() == "panaroma.jpg":
                        image_path = os.path.join(root, file_name)
                        image = Image.open(image_path)
                        if image:
                            return image                       
    return None
