import streamlit as st
import cv2
import numpy as np
import matplotlib.pyplot as plt

# from upload import *


def aboutus():
  st.title("About us")
  st.header("Image Transformation app")

pg = st.navigation([
    st.Page(aboutus, title="About us", icon=":material/favorite:"),
    st.Page("upload.py", title="Upload Image", icon=":material/upload_file:"),
    st.Page("exc.py", title="Extract Color", icon=":material/layers:"),
    st.Page("edge.py", title="Edge Detection", icon=":material/draw:"),
    st.Page("seg.py", title="Object Segmentation", icon=":material/category:"),
    st.Page("snr.py", title="Rotation & Scale", icon=":material/frame_reload:"),
    st.Page("function.py", title="Update", icon=":material/edit:"),
])
pg.run()