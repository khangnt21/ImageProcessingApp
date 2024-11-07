import streamlit as st # type: ignore
import cv2
import numpy as np
import matplotlib.pyplot as plt
from function import *

st.header("Upload your image to process!")
img_file = st.file_uploader(label='Upload a file', type=['png', 'jpg'])
if img_file is not None:
  st.success("App: Successfully upload", icon=':material/check_circle:')
  file_bytes = np.asarray(bytearray(img_file.read()), dtype=np.uint8)
  image = cv2.imdecode(file_bytes, 1)
  image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
  st.image(image)
  filename = "img/" + img_file.name.split('.')[0] + '_0.' +  img_file.name.split('.')[-1]
  cv2.imwrite(filename, cv2.cvtColor(image, cv2.COLOR_RGB2BGR))
  # cv2.imwrite(filename, image)
  st.write(image.shape)

filename = file_selector("img/")
st.write('You choose `%s`' % filename)
image = cv2.imread(filename)
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
st.write("Preview Image")
st.image(image)


