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
  st.image(image)

if image is not None:
  angle = st.slider('Select number of segmented regions', 0, 360, 180, 1)
  scale = st.slider('Select number of segmented regions', 0.5, 3.0, 1.0, 0.5)
  img1 = ScaleRotate(image, scale, angle)
  save_filename = filename.split('_')[0] + "_S" + str(scale) + "_R" + str(angle) + '.'+filename.split('.')[-1]
  if st.button("Download"):
    cv2.imwrite(save_filename, img1)
    st.success('Download successfully `%s`' % save_filename, icon=":material/check_circle:")
  st.image(img1)

