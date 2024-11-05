import streamlit as st
import cv2
import numpy as np
import matplotlib.pyplot as plt
import os


def file_selector(task, folder_path="img/"):
    filenames = os.listdir(folder_path)
    selected_filename = st.selectbox('Select a file', filenames, key=task)
    return os.path.join(folder_path, selected_filename)

def convert_RGB2Gray(image):
  return cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

def EdgeDetect(gray, thres):
  if gray.shape[2] is not None:
    gray = convert_RGB2Gray(gray)
  blurred = cv2.GaussianBlur(gray, (5, 5), 1)
  canny = cv2.Canny(blurred, thres[0], thres[1])
  return canny

def ObjSeg(gray, thres):
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
  if gray.shape[2] is not None:
    gray = convert_RGB2Gray(gray)
  ImageSeg = np.ones_like(gray)
  for i, thres in enumerate(thres):
    ImageSeg[gray > thres] = i+2

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

def ScaleRotate(image, scale_factor=1, rotate_angle=15):
  k = 3
  height, width = image.shape[:2]
  center = (width/2, height/2)
  size = k*np.sqrt(width**2+height**2).astype(np.int16)
  transform_matrix = get_transform_matrix(rotate_angle, scale_factor, center, (size/2,size/2))
  cv2_wrap_matrix = transform_matrix[:2, :]
  transformed_image = cv2.warpAffine(src=image, M=cv2_wrap_matrix, dsize=(size, size))
  return transformed_image
