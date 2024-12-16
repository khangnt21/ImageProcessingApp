from function import *
from upload import *

# Creating two columns using Streamlit's layout
col1, col2 = st.columns(2)

# Column 1: File selection and image processing options
with col1:
    # File selector: User selects an image from the folder
    filename = file_selector('edge')
    st.write(f'You choose `{filename}`')
    
    # Color mode selection: User can choose from different color modes
    mode = st.radio(
        label="Color Mode",
        horizontal=True,
        options=["RGB", "BGR", "HSV", "YCrCb", "LAB", "Gray"]
    )
    
    # Load the image and convert it to the selected color mode
    rgb_img, mode_img, chans = ColorConvert(filename, mode.lower())
    h, w = rgb_img.shape[:2]  # Image height and width
    
    # Display instructions for the user
    text = '''
    1. Drag an area on *Preview Image* to zoom it out
    
    2. Click to the target position for color extraction
    
    3. Click copy icon to copy hexa code'''
    st.markdown(text)
    st.text_input("Enter your hexa color")

# If the image is loaded successfully, display it and the corresponding color channels
if rgb_img is not None:
    st.write("Preview Image")
    
    # Image coordinates: Allow the user to click and drag to select an area of interest
    position = streamlit_image_coordinates(filename, key="local4", use_column_width="always", click_and_drag=True)
    
    st.write("Color Channels Visualization")
    
    # Split the color-mode image into its individual channels
    C1, C2, C3 = cv2.split(mode_img)
    
    # Display the original color-mode image and its individual channels
    c0, c1 = st.columns(2)
    with c0:
        st.write(f"{chans[0]} Channel")
        st.image(mode_img)  # Display the full color-mode image
    with c1:
        st.write(f"{chans[1]} Channel")
        st.image(C1)  # Display the first color channel
    
    c2, c3 = st.columns(2)
    with c2:
        st.write(f"{chans[2]} Channel")
        st.image(C2)  # Display the second color channel
    with c3:
        st.write(f"{chans[3]} Channel")
        st.image(C3)  # Display the third color channel

# Column 2: Zoom and color extraction functionality
with col2:
    if position is not None:
        # Crop and Display the zoomed-out image based on selected position
        pos = [
            position["y1"] / position["height"] * h, 
            position["y2"] / position["height"] * h,
            position["x1"] / position["width"] * w, 
            position["x2"] / position["width"] * w
        ]
        pos = np.round(np.array(pos)).astype(np.int16)
        crop_img = rgb_img[pos[0]:pos[1], pos[2]:pos[3], :]
        crop_h, crop_w = crop_img.shape[:2]
        st.write("Zoom out image")

        # Extract the color at the selected position within the zoomed-out image
        col_pos = streamlit_image_coordinates(
            Image.fromarray(crop_img, 'RGB'), key="pil", use_column_width="always", click_and_drag=False
        )
        cpos = [col_pos["y"] / col_pos["height"] * crop_h, col_pos["x"] / col_pos["width"] * crop_w]
        cpos = np.round(np.array(cpos)).astype(np.int16)
        color = crop_img[cpos[0], cpos[1], :]

        # Display the extracted color in RGB and Hex format
        df = pd.DataFrame({
            'Red': [color[0]],
            'Green': [color[1]],
            'Blue': [color[2]]
        })
        hex, rx, gx, bx = rgb2hex(color)

        # Display the extracted color and the hex codes
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

        # Display the extracted color values in a table and provide a copy option for the hex code
        copyy, write = st.columns([0.38, 0.62])
        with write:
            st.write(df)
        with copyy:
            hexcolor = st.code(f'{hex}', language="python")  # Display hex code as Python code
