from function import *
from upload import *

# Create two columns using Streamlit's layout
col1, col2 = st.columns(2)

# Column 1: File selection, input parameters, and filename setup
with col1:
    # Select input image file using the file_selector function
    filename = file_selector('seg')
    st.write(f'You choose `{filename}`')

    # Extract the folder path and image format for saving
    folder_path = filename.split("/")[0] + "/"
    format_img = "." + filename.split('.')[-1]
    name = filename.split("/")[1].split("_")[0]

    # Read the image and convert from BGR to RGB
    image = cv2.imread(filename)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Set up columns for input parameter controls (number of objects and segmentation)
    Atxt, Aslider = st.columns([0.2, 0.8])
    with Atxt:
        # Set number of objects to segment (between 2 and 9)
        value_txt = st.number_input('N Objects', min_value=2, max_value=9, value=3, 
                                    key='numeric', on_change=update_slider)
    with Aslider:
        # Set the slider for selecting the number of segmented objects
        region = st.slider('Select number of segmented objects',
                           min_value=2, max_value=9, value=value_txt, step=1, 
                           key='slider', on_change=update_numin)
    value = region - 1  # Calculate the number of regions to segment (excluding the background)

    # Define the filename for saving the processed image
    save_name = name + "_seg" + str(value)
    saved = st.text_input("Enter save filename", save_name)
    if saved != save_name:
        save_name = saved + '_0'
    save_filename = folder_path + save_name + format_img

    # Add a button for downloading the processed image
    down, gray_tog = st.columns([0.55, 0.45])
    with down:
        download = st.button("Download your image")
    with gray_tog:
        # Add toggle for grayscale preview
        toggle = st.toggle("Gray Preview")

# Column 2: Image preview and processing
with col2:
    name, color1 = st.columns([0.4, 0.6])
    with name:
        st.write("Preview Image")
    
    if toggle:
        # Show grayscale preview if the toggle is enabled
        h, w = image.shape[:2]
        gray = convert_RGB2Gray(image)  # Convert the image to grayscale
        col_pos = streamlit_image_coordinates(Image.fromarray(gray, 'L'),
                      key="pil", use_column_width="always", click_and_drag=False)
        cpos = [col_pos["y"] / col_pos["height"] * h, 
                col_pos["x"] / col_pos["width"] * w] 
        cpos = np.round(np.array(cpos)).astype(np.int16)
        color = gray[cpos[0], cpos[1]]  # Get the grayscale value at the clicked position
        with color1:
            st.write(f"Grayscale value = {color}")
    else:
        # Show the original image if the grayscale preview is off
        st.image(image)

# Display color legend for each segmented region
display_color()

if image is not None:
    # Create columns for threshold inputs (one per object)
    thres = st.columns(value)
    threshold = np.zeros(value)
    tmp, done = 0, False
    step = 255 // (value + 1)  # Set threshold increment step

    # Collect threshold values for segmentation
    for i in range(value):
        with thres[i]:
            txt = st.number_input(f'Threshold {i+1}', 
                                  min_value=0, max_value=255, value=tmp + step)
            threshold[i] = txt
            tmp = txt + 1  # Update the previous threshold value
            if i == value - 1:
                done = True

    # Perform object segmentation if all thresholds are set
    if done:
        img1 = ObjSeg(image, threshold)
        st.image(img1)  # Display segmented image
    
    # Download the segmented image if the button is clicked
    if download:
        cv2.imwrite(save_filename, cv2.cvtColor(img1, cv2.COLOR_RGB2BGR))
        st.success(f'Download successfully `{save_filename}`', icon=":material/check_circle:")
