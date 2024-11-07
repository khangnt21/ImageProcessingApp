import streamlit as st # type: ignore
import cv2
import numpy as np
import matplotlib.pyplot as plt
from function import *
from upload import *

col1, col2 = st.columns(2)
with col1:
  # Select input file
  filename = file_selector('seg')
  st.write('You choose `%s`' % filename)

  # Extract path
  folder_path = filename.split("/")[0] + "/"
  format_img = "." + filename.split('.')[-1]
  name = filename.split("/")[1].split("_")[0]

  # Image read
  image = cv2.imread(filename)
  image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
  
  # Select parameter inputs
  Lthres_0, Rthres = 100, 200
  threshold = st.slider('Select your left & right threshold for Canny', 
                        min_value=0, max_value=255, value=(Lthres_0, Rthres), 
                        key = 'slider', on_change=update_numeric2inp)
  
  lthres, rthres = st.columns(2)
  with lthres:
    # Numeric input for the left threshold
    left_threshold = st.number_input('Left Threshold', 
                    min_value=0, max_value=255, value=Lthres_0,
                    key='left_threshold', on_change=update_slider2inp)
  with rthres:
    # Numeric input for the right threshold
    right_threshold = st.number_input('Right Threshold', 
                    min_value=left_threshold, max_value=255, value=threshold[1], 
                    key='right_threshold', on_change=update_slider2inp)
    
  # Enter saved filename
  thres= "-".join(f"{num}" for num in threshold)
  save_name = name + "_edge" + thres
  saved = st.text_input("Enter save filename", save_name)
  if saved != save_name:
    save_name = saved + '_0'
  save_filename = folder_path + save_name + format_img

  # Download button
  download = st.button("Download your image")
  
with col2:
  st.write("Preview Image")
  st.image(image)

if image is not None:
  img1 = EdgeDetect(image, threshold)
  if download:
    cv2.imwrite(save_filename, cv2.cvtColor(img1, cv2.COLOR_RGB2BGR))
    st.success('Download successfully `%s`' % save_filename,
                icon=":material/check_circle:")
  st.image(img1)