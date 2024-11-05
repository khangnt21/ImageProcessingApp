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