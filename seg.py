import streamlit as st
import cv2
import numpy as np
import matplotlib.pyplot as plt
from function import *
from upload import *

col1, col2 = st.columns(2)
with col1:
  filename = file_selector('seg')
  st.write('You choose `%s`' % filename)
  image = cv2.imread(filename)

with col2:
  st.write("Preview Image")
  st.image(image, channels="BGR")


if image is not None:
  value = st.slider('Select number of segmented regions', 2, 10, 3, 1)
  threshold = np.linspace(0, 255, value+2, dtype=int)[1:-2]
  img1 = ObjSeg(image, threshold)
  save_filename = filename.split('_')[0] + "_seg" + str(value) + '.'+filename.split('.')[-1]
  if st.button("Download"):
    cv2.imwrite(save_filename, img1)
    st.success('Download successfully `%s`' % save_filename, icon=":material/check_circle:")
    plt.imshow(img1)
  st.image(img1, channels='BGR')