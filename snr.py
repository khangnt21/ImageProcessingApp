import streamlit as st
import cv2
import numpy as np
import matplotlib.pyplot as plt
from function import *
from upload import *

col1, col2 = st.columns(2)
with col1:
  filename = file_selector('snr')
  st.write('You choose `%s`' % filename)
  image = cv2.imread(filename)

with col2:
  st.write("Preview Image")
  st.image(image, channels="BGR")

# def get_transform_matrix(rotate_angle, scale_factor, center_point):
#   # Implement Code Here
#   r, s, c  = rotate_angle/180*np.pi, scale_factor, center_point
#   matrix = [[s*np.cos(r), s*np.sin(r), (1-s*np.cos(r))*c[0]-s*np.sin(r)*c[1]],
#             [-s*np.sin(r), s*np.cos(r),s*np.sin(r)*c[0]+(1-s*np.cos(r))*c[1]],
#             [0, 0, 1]]
#   return np.array(matrix) 

# def ScaleRotate(image, scale_factor=1, rotate_angle=15):
#   height, width = image.shape[:2]
#   center = (width/2, height/2)
#   transform_matrix = get_transform_matrix(rotate_angle, scale_factor, center)
#   cv2_wrap_matrix = transform_matrix[:2, :]
#   rotated_image = cv2.warpAffine(src=image, M=cv2_wrap_matrix, dsize=(width, height))
#   return rotated_image

if image is not None:
  angle = st.slider('Select number of segmented regions', 0, 360, 180, 1)
  scale = st.slider('Select number of segmented regions', 0.5, 3.0, 1.0, 0.5)
  img1 = ScaleRotate(image, scale, angle)
  save_filename = filename.split('_')[0] + "_S" + str(scale) + "_R" + str(angle) + '.'+filename.split('.')[-1]
  if st.button("Download"):
    cv2.imwrite(save_filename, img1)
    st.success('Download successfully `%s`' % save_filename, icon=":material/check_circle:")
  st.image(img1, channels='BGR')

