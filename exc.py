from function import *
from upload import *

col1, col2 = st.columns(2)
with col1:
  filename = file_selector('edge')
  st.write('You choose `%s`' % filename)
  mode = st.radio(label="Color Mode", horizontal=True,
                  options=["RGB", "BGR","HSV", "YCrCb", "LAB", "Gray"])
  rgb_img, mode_img, chans = ColorConvert(filename, mode.lower())
  h, w = rgb_img.shape[:2]
  text = '''1. Drag an area on *Preview Image* to zoom it out
  2. Click to the target position for color extraction
  3. Click copy icon to copy hexa code'''
  st.markdown(text)

if rgb_img is not None:
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

with col2:
  # st.write(position)
  # Crop and Display the zoom out image
  if position is not None:
    pos = [position["y1"]/position["height"]*h, position["y2"]/position["height"]*h,
          position["x1"]/position["width"]*w, position["x2"]/position["width"]*w] 
    pos = np.round(np.array(pos)).astype(np.int16)
    crop_img = rgb_img[pos[0]:pos[1], pos[2]:pos[3], :]
    crop_h, crop_w = crop_img.shape[:2]
    st.write("Zoom out image")
    # st.image(crop_img, use_column_width="always")

    # Extract color at selected position 
    col_pos = streamlit_image_coordinates(Image.fromarray(crop_img, 'RGB'), key="pil",
              use_column_width="always", click_and_drag=False)
    cpos = [col_pos["y"]/col_pos["height"]*crop_h, 
          col_pos["x"]/col_pos["width"]*crop_w] 
    cpos = np.round(np.array(cpos)).astype(np.int16)
    color = crop_img[cpos[0], cpos[1], :]

    df = pd.DataFrame({
      'Red': [color[0]],
      'Green': [color[1]],
      'Blue': [color[2]]
    })
    hex, rx, gx, bx = rgb2hex(color)
    
    # Display extracted color
    hexx, rgb, r, g, b = st.columns([0.4, 0.15, 0.15, 0.15, 0.15])
    with hexx:
      st.write("Hexa code")
    with rgb:
      rgb_color = st.color_picker(label="RGB", value=hex)
    with r:
      r_color = st.color_picker(label="Red", value=rx)
    with g:
      g_color = st.color_picker(label="Green", value=gx)
    with b:
      b_color = st.color_picker(label="Blue", value=bx)

    copyy, write = st.columns([0.38, 0.62])
    with write:
      st.write(df)
    with copyy:
      hexcolor = st.code('%s' % hex, language="python")
