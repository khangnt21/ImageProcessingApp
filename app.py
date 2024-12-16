import streamlit as st # type: ignore


def aboutus():
  st.title("About us")
  st.header("Image Processing application")

  script = '''
    1. Upload Image  
      Upload your image and save it to folder `img`.
    2. Extract Color  
      Visualize image in other color spaces and get the color at any picked pixel.
    3. Edge Detection  
      Set the value for threshold inputs for Canny Edge Detection
    4. Object Segmentation  
      Segment the object regions based on the value thresholded on Gray-scale image.
    5. Image Transformation  
      Edit image using scale and rotation transform, and crop the selected region.
  '''
  st.markdown(script)
  st.header("Contributions")
  members = '''
    | No. | Name              | Student ID | Role          | Task                 |
    |-----|-------------------|------------|---------------|----------------------|
    | 1   | Nguyễn Thế Khang  | 21020692   | Team Leader   | Algorithm development|
    | 2   | Lê Mạnh Kha       | 21021599   | Member        | Report writing       |
    | 3   | Hoàng Nhật Minh   | 21020696   | Member        | Interface design     |
  '''
  st.markdown(members)

pg = st.navigation([
    st.Page(aboutus, title="About us", icon=":material/favorite:"),
    st.Page("upload.py", title="Upload Image", icon=":material/upload_file:"),
    st.Page("exc.py", title="Extract Color", icon=":material/layers:"),
    st.Page("edge.py", title="Edge Detection", icon=":material/draw:"),
    st.Page("seg.py", title="Object Segmentation", icon=":material/category:"),
    st.Page("edit.py", title="Edit Image", icon=":material/tune:")

])
pg.run()