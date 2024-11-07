from function import *
from upload import *
from PIL import Image
from streamlit_image_coordinates import streamlit_image_coordinates

col1, col2 = st.columns(2)
with col1:
  filename = file_selector('edge')
  st.write('You choose `%s`' % filename)
  mode = st.radio(label="Color Mode", horizontal=True,
                  options=["RGB", "BGR","HSV", "YCrCb", "LAB", "Gray"])
  rgb_img, mode_img, chans = ColorConvert(filename, mode.lower())


if image is not None:
  st.write("Preview Image")
  position = streamlit_image_coordinates(filename, key="local4",
            use_column_width="always", click_and_drag=True,)
  st.write("Color Channels Visualization")
  C1, C2, C3 = cv2.split(mode_img)
  c0, c1= st.columns(2)
  with c0:
    st.write(chans[0]+" Channel")
    st.image(mode_img)
  with c1:
    st.write(chans[1]+" Channel")
    st.image(C1)
  c2, c3 = st.columns(2)
  with c2:
    st.write(chans[2]+" Channel")
    st.image(C2)
  with c3:
    st.write(chans[3]+" Channel")
    st.image(C3)
def click_event(event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONDOWN:
        print(x, ' ', y)
with col2:
  st.write("Preview Image")
  st.write(position)
  st.image(rgb_img)
  cv2.setMouseCallback('rgb_img', click_event)
  # crop_img = rgb_img[position["y1"]-1:position["y1"]+1, position["x1"]-1:position["x1"]+1, :]
  # mean_pix = np.mean(crop_img, axis=(0,1)).astype(np.int16)
  # # print
  # expanded_array = np.full((20, 20, 3), mean_pix)

  # st.image(expanded_array)
  # print(crop_img)
  # print(mean_pix)
  # color = rgb_img[position["y1"], position["x1"], :]
  # st.write(color)
  # hex = rgb2hex(color)
  # print(color)
  # st.write(hex)
  box_color = st.color_picker(label="Box Color", 
                                value=hex)

