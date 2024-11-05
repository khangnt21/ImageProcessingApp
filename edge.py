import streamlit as st
import cv2
import numpy as np
import matplotlib.pyplot as plt
from function import *
from upload import *

col1, col2 = st.columns(2)
with col1:
  filename = file_selector('edge')
  st.write('You choose `%s`' % filename)
  image = cv2.imread(filename)
with col2:
  st.write("Preview Image")
  st.image(image)

if image is not None:
  threshold = st.slider('Select your left & right threshold for Canny', 0, 255, (100, 200))
  img1 = EdgeDetect(image, threshold)
  thres= "-".join(f"{num}" for num in threshold)
  save_filename = filename.split('_')[0] + "_edge" + thres + '.'+filename.split('.')[-1] 
  if st.button("Download"):
    cv2.imwrite(save_filename, img1)
    st.success('Download successfully `%s`' % save_filename, icon=":material/check_circle:")
  st.image(img1)