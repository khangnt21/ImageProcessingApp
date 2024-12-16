import os
import cv2
import numpy as np
import pandas as pd
from PIL import Image
import matplotlib.pyplot as plt

import pyperclip  # Clipboard interaction
import streamlit as st  # Streamlit framework for building apps
from streamlit_cropper import st_cropper  # Streamlit image cropping tool
from streamlit_image_coordinates import streamlit_image_coordinates  # Streamlit image coordinates picker

# Define a color mapping dictionary for segmentation
color_mapping = {
    1: [68, 1, 84],
    2: [72, 40, 120],
    3: [62, 74, 137],
    4: [49, 104, 142],
    5: [38, 130, 142],
    6: [31, 158, 137],
    7: [53, 183, 121],
    8: [109, 205, 89],
    9: [180, 222, 44]
}

# Function to sync a slider and numeric input
# Used in Streamlit to dynamically update UI components
def update_slider():
    """
    Synchronizes a Streamlit slider with a numeric input field.
    """
    st.session_state.slider = st.session_state.numeric

def update_numin():
    """
    Synchronizes a numeric input field with a Streamlit slider.
    """
    st.session_state.numeric = st.session_state.slider

# Function to synchronize range sliders with numeric inputs in Streamlit
def update_slider2inp():
    """
    Synchronizes range slider inputs with numeric input fields for left and right thresholds.
    """
    st.session_state['slider'] = (
        st.session_state['left_threshold'],
        st.session_state['right_threshold']
    )

def update_numeric2inp():
    """
    Synchronizes numeric input fields for left and right thresholds with a range slider.
    """
    st.session_state['left_threshold'], st.session_state['right_threshold'] = (
        st.session_state['slider']
    )

# Converts an RGB color (list) to hex format
# Returns hex representations for full color and its individual components
def rgb2hex(color):
    """
    Converts an RGB color to its hexadecimal representation.

    Args:
        color (list): A list of three integers representing an RGB color [R, G, B].

    Returns:
        tuple: A tuple containing:
            - str: Hexadecimal code for the full color.
            - str: Hexadecimal code for the red component.
            - str: Hexadecimal code for the green component.
            - str: Hexadecimal code for the blue component.
    """
    r, g, b = color[0], color[1], color[2]
    return "#{:02x}{:02x}{:02x}".format(r, g, b), "#{:02x}0000".format(r), "#00{:02x}00".format(g), "#0000{:02x}".format(b)

# Function to load an image and convert it to the specified color mode
# Modes: gray, rgb, bgr, hsv, ycrcb, lab
def ColorConvert(img_path, mode='gray'):
    """
    Converts an image to the specified color mode.

    Args:
        img_path (str): Path to the input image file.
        mode (str): Desired color mode. Options: 'gray', 'rgb', 'bgr', 'hsv', 'ycrcb', 'lab'.

    Returns:
        tuple: A tuple containing:
            - numpy.ndarray: Original image in RGB format.
            - numpy.ndarray: Converted image in the specified color mode.
            - list: Channel descriptions for the converted image.
    """
    bgr = cv2.imread(img_path)  # Read image in BGR format
    rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)  # Convert to RGB
    
    if mode == 'gray':
        gray = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)  # Grayscale image
        chans = ["Gray", "Gray", "Gray", "Gray"]
        return rgb, np.repeat(gray[:, :, np.newaxis], 3, axis=2), chans
    elif mode == 'rgb':
        chans = ["RGB", "R - Red", "G - Green", "B - Blue"]
        return rgb, rgb, chans
    elif mode == 'bgr':
        chans = ["BGR", "B - Blue", "G - Green", "R - Red"]
        return rgb, bgr, chans
    elif mode == 'hsv':
        chans = ["HSV", "V - Value", "S - Saturation", "H - Hue"]
        hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)
        return rgb, hsv[:, :, 2::-1], chans
    elif mode == 'ycrcb':
        chans = ["YCrCb", "Y - Luminance", "Cr - Red Difference", "Cb - Blue Difference"]
        ycrcb = cv2.cvtColor(bgr, cv2.COLOR_BGR2YCrCb)
        return rgb, ycrcb, chans
    elif mode == 'lab':
        chans = ["LAB", "L - Lightness", "A - Green to Magenta", "B - Blue to Yellow"]
        lab = cv2.cvtColor(bgr, cv2.COLOR_BGR2LAB)
        return rgb, lab, chans
    else:
        raise ValueError("Invalid mode. Choose from 'rgb', 'bgr', 'gray', 'hsv', 'ycrcb', or 'lab'.")

# Function to select a file from a specified directory in Streamlit
def file_selector(task, folder_path="img/"):
    """
    Selects a file from a specified directory in Streamlit.

    Args:
        task (str): Unique key for the Streamlit widget.
        folder_path (str): Path to the folder containing files.

    Returns:
        str: Full path to the selected file.
    """
    filenames = os.listdir(folder_path)
    selected_filename = st.selectbox('Select a file', filenames, key=task)
    return os.path.join(folder_path, selected_filename)

# Function to convert an RGB image to grayscale
def convert_RGB2Gray(image):
    """
    Converts an RGB image to grayscale.

    Args:
        image (numpy.ndarray): Input RGB image.

    Returns:
        numpy.ndarray: Grayscale image.
    """
    return cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

# Function to detect edges in an image using Canny Edge Detection
# Applies Gaussian blur and then uses thresholds for edge detection
def EdgeDetect(image, thres):
    """
    Performs edge detection on an image using the Canny algorithm.

    Args:
        image (numpy.ndarray): Input image.
        thres (tuple): Threshold values for Canny edge detection (low, high).

    Returns:
        numpy.ndarray: Binary image with edges detected.
    """
    if image.shape[2] is not None:  # If image has color channels
        image = convert_RGB2Gray(image)  # Convert to grayscale
    blurred = cv2.GaussianBlur(image, (5, 5), 1)  # Apply Gaussian blur
    canny = cv2.Canny(blurred, thres[0], thres[1])  # Canny edge detection
    return canny

# Displays a color picker for each color in the color_mapping dictionary
# Used in Streamlit to allow users to pick colors dynamically
def display_color():
    """
    Displays color pickers in Streamlit for all colors in the color_mapping dictionary.

    Args:
        None

    Returns:
        None
    """
    hex_color_mapping = {
        key: '#{:02x}{:02x}{:02x}'.format(*value) 
        for key, value in color_mapping.items()
    }
    cols = st.columns(9)
    for i in range(9):
        with cols[i]:
            st.color_picker(f"Color {i+1}", hex_color_mapping.get(i+1))

# Function to perform object segmentation based on intensity thresholds
# Assigns unique IDs to objects and maps them to colors from the color_mapping dictionary
def ObjSeg(image, thres):
    """
    Segments objects in an image based on intensity thresholds and assigns colors.

    Args:
        image (numpy.ndarray): Input image.
        thres (list): List of intensity threshold values.

    Returns:
        numpy.ndarray: Segmented image with color-coded objects.
    """
    if image.shape[2] is not None:
        image = convert_RGB2Gray(image)  # Convert to grayscale
    ImageSeg = np.ones_like(image)
    for i, thres_val in enumerate(thres):
        ImageSeg[image > thres_val] = i + 2

    # Map segmentation to color values
    height, width = ImageSeg.shape
    color_matrix = np.zeros((height, width, 3), dtype=np.uint16)
    for i in range(height):
        for j in range(width):
            object_id = ImageSeg[i, j]
            if object_id in color_mapping:
                color_matrix[i, j, :] = color_mapping[object_id]
    return color_matrix

def get_transform_matrix(rotate_angle, scale_factor, center_point, trans_point):
    """
    Calculate the transformation matrix for scaling, rotation, and translation.

    Args:
        rotate_angle (float): Rotation angle in degrees.
        scale_factor (float): Scaling factor (e.g., 1.0 for no scaling, >1 for zoom in, <1 for zoom out).
        center_point (tuple): Coordinates of the center point of the transformation (x, y).
        trans_point (tuple): Coordinates of the translation target point (x, y).

    Returns:
        np.ndarray: A 3x3 transformation matrix combining scaling, rotation, and translation.
    """
    r, s, c, t = rotate_angle / 180 * np.pi, scale_factor, center_point, trans_point
    matrix = [
        [s * np.cos(r), s * np.sin(r), (1 - s * np.cos(r)) * c[0] - s * np.sin(r) * c[1]],
        [-s * np.sin(r), s * np.cos(r), s * np.sin(r) * c[0] + (1 - s * np.cos(r)) * c[1]],
        [0, 0, 1],
    ]
    translation_matrix = np.array(
        [
            [1, 0, t[0] - c[0]],
            [0, 1, t[1] - c[1]],
            [0, 0, 1],
        ],
        dtype=np.float32,
    )
    return np.array(translation_matrix @ matrix)


def ScaleRotate(image, scale_factor=1, rotate_angle=15, zoomout="Full image"):
    """
    Apply scaling, rotation, and optional zooming transformations to an image.

    Args:
        image (np.ndarray): Input image as a NumPy array (HxWxC or HxW for grayscale).
        scale_factor (float): Scaling factor (e.g., 1.0 for no scaling, >1 for zoom in, <1 for zoom out).
        rotate_angle (float): Rotation angle in degrees.
        zoomout (str): Specifies the output size. Options:
            - "Full image": Resizes output image to a larger canvas to fit full rotated image.
            - "By scale": Resizes the output based on the scaling factor.
            - "Original": Keeps the original image dimensions.

    Returns:
        np.ndarray: Transformed image with applied scaling, rotation, and optional zoom.
    """
    k = 3
    height, width = image.shape[:2]
    center = (width / 2, height / 2)
    size = k * np.sqrt(width**2 + height**2).astype(np.int16)
    if zoomout == "Full image":
        size1 = size
        size2 = size
    elif zoomout == "By scale":
        size1 = int(scale_factor * height)
        size2 = int(scale_factor * width)
    elif zoomout == "Original":
        size1 = height
        size2 = width
    transform_matrix = get_transform_matrix(rotate_angle, scale_factor, center, (size2 / 2, size1 / 2))
    cv2_wrap_matrix = transform_matrix[:2, :]
    transformed_image = cv2.warpAffine(src=image, M=cv2_wrap_matrix, dsize=(size2, size1))
    return transformed_image
