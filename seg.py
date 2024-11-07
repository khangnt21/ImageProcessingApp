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
  folder_path = filename.split("/")[0]+"/"
  format_img = "."+filename.split('.')[-1]
  name = filename.split("/")[1].split("_")[0]

  # Image read
  image = cv2.imread(filename)
  image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
  
  # Select parameter inputs
  Atxt, Aslider = st.columns([0.2, 0.8])
  with Atxt:
    value_txt = st.number_input('N Objects',  min_value=2, max_value=9, 
                                value = 3, key = 'numeric', on_change = update_slider)
  with Aslider:
    region = st.slider('Select number of segmented objects',
                       min_value=2, max_value=9, value = value_txt, step=1, 
                       key = 'slider', on_change = update_numin)
  value = region-1

  # Enter saved filename
  save_name = name + "_seg" + str(value)
  saved = st.text_input("Enter save filename", save_name)
  if saved != save_name:
    save_name = saved + '_0'
  save_filename = folder_path+save_name+format_img

  # Download button
  down, gray_tog = st.columns([0.55, 0.45])
  with down:
    download = st.button("Download your image")
  with gray_tog:
    toggle = st.toggle("Gray Preview")
with col2:
  st.write("Preview Image")
  if toggle:
    st.image(convert_RGB2Gray(image))
  else:
    st.image(image)

# Display color legend for each segmented region?


if image is not None:
  thres = st.columns(value)
  threshold = np.zeros(value)
  tmp, done = 0, False
  step = 255//(value+1)
  for i in range(value):
    with thres[i]:
      txt = st.number_input(f'Threshold {i+1}', 
            min_value=0, max_value=255, value = tmp+step)
      threshold[i] = txt
      tmp = txt+1
      if i == value-1:
        done = True
  if done == True:
    img1 = ObjSeg(image, threshold)
    st.image(img1)
  if download:
    cv2.imwrite(save_filename, cv2.cvtColor(img1, cv2.COLOR_RGB2BGR))
    st.success('Download successfully `%s`' % save_filename,
                icon=":material/check_circle:")
  