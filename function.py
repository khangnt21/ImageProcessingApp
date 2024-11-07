import streamlit as st # type: ignore
import cv2
import numpy as np
import matplotlib.pyplot as plt
import os


def update_slider():
  st.session_state.slider = st.session_state.numeric
def update_numin():
  st.session_state.numeric = st.session_state.slider  

def update_slider2inp():
  st.session_state['slider'] = (st.session_state['left_threshold'],
                                   st.session_state['right_threshold'])
def update_numeric2inp():
  st.session_state['left_threshold'], st.session_state['right_threshold'] = \
    st.session_state['slider']
  
def rgb2hex(color):
  r,g,b = color[0], color[1], color[2]  
  return "#{:02x}{:02x}{:02x}".format(r,g,b)

def ColorConvert(img_path, mode='gray'):
  bgr = cv2.imread(img_path)
  rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
  if mode == 'gray':
    gray = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    chans = ["Gray", "Gray", "Gray", "Gray"]
    return rgb, np.repeat(gray[:,:,np.newaxis], 3, axis=2),chans
  elif mode == 'rgb':
    chans = ["RGB", "R - Red", "G - Green", "B - Blue"]
    return rgb, rgb, chans
  elif mode == 'bgr':
    chans = ["BGR", "B - Blue", "G - Green", "R - Red"]
    return rgb, bgr, chans
  elif mode == 'hsv':
    chans = ["HSV", "V - Value", "S - Saturation", "H - Hue"]
    hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)
    return rgb, hsv[:,:,2::-1], chans
  elif mode == 'ycrcb':
    chans = ["YCrCb", "Y - Luminace", "Cr - Red Difference", "Cb - Blue Difference"]
    ycrcb = cv2.cvtColor(bgr, cv2.COLOR_BGR2YCrCb)
    return rgb, ycrcb, chans
  elif mode == 'lab':
    chans = ["LAB", "L - Lightness", "A - Green to Magenta", "B - Blue to Yellow"]
    lab = cv2.cvtColor(bgr, cv2.COLOR_BGR2LAB)
    return rgb, lab, chans
  else:
    raise ValueError("Invalid mode. \
                     Choose from 'rgb', 'bgr', 'gray', 'hsv', 'ycrcb', or 'lab'.")

def file_selector(task, folder_path="img/"):
    filenames = os.listdir(folder_path)
    selected_filename = st.selectbox('Select a file', filenames, key=task)
    return os.path.join(folder_path, selected_filename)

def convert_RGB2Gray(image):
  return cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

def EdgeDetect(image, thres):
  if image.shape[2] is not None:
    image = convert_RGB2Gray(image)
  blurred = cv2.GaussianBlur(image, (5, 5), 1)
  canny = cv2.Canny(blurred, thres[0], thres[1])
  return canny

def ObjSeg(image, thres):
  color_mapping = {
    1: [68, 1, 84],
    2: [72, 40, 120],
    3: [62, 74, 137],
    4: [49, 104, 142],
    5: [38, 130, 142],
    6: [31, 158, 137],
    7: [53, 183, 121],
    8: [109, 205, 89],
    9: [180, 222, 44],
    10: [253, 231, 37]
  }
  if image.shape[2] is not None:
    image = convert_RGB2Gray(image)
  ImageSeg = np.ones_like(image)
  for i, thres in enumerate(thres):
    ImageSeg[image > thres] = i+2

  height, width = ImageSeg.shape
  color_matrix = np.zeros((height, width, 3), dtype=np.uint16)
  for i in range(height):
    for j in range(width):
        object_id = ImageSeg[i, j]
        if object_id in color_mapping:
            color_matrix[i, j, :] = color_mapping[object_id]
  return color_matrix

def get_transform_matrix(rotate_angle, scale_factor, center_point, trans_point):
  # Implement Code Here
  r, s, c, t = rotate_angle/180*np.pi, scale_factor, center_point, trans_point
  matrix = [[s*np.cos(r), s*np.sin(r), (1-s*np.cos(r))*c[0]-s*np.sin(r)*c[1]],
            [-s*np.sin(r), s*np.cos(r),s*np.sin(r)*c[0]+(1-s*np.cos(r))*c[1]],
            [0, 0, 1]]
  translation_matrix = np.array([
      [1, 0, t[0]-c[0]],
      [0, 1, t[1]-c[1]],
      [0, 0, 1]], dtype=np.float32)
  return np.array(translation_matrix@matrix) 

def ScaleRotate(image, scale_factor=1, rotate_angle=15, zoomout='Full image'):
  k = 3
  height, width = image.shape[:2]
  center = (width/2, height/2)
  size = k*np.sqrt(width**2+height**2).astype(np.int16)
  if zoomout == "Full image":
    size1 = size;
    size2 = size;
  elif zoomout == "By scale":
    size1 = int(scale_factor*height)
    size2 = int(scale_factor*width)
  elif zoomout == "Original":
    size1 = height
    size2 = width
  transform_matrix = get_transform_matrix(rotate_angle, scale_factor, 
                                          center, (size2/2,size1/2))
  cv2_wrap_matrix = transform_matrix[:2, :]
  transformed_image = cv2.warpAffine(src=image, M=cv2_wrap_matrix, dsize=(size2, size1))
  return transformed_image
