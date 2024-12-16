from function import *
from upload import *

# Create two columns using Streamlit's layout
col1, col2 = st.columns(2)

# Column 1: File selection and input parameters
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

    # Set default threshold values for Canny edge detection
    Lthres_0, Rthres_0 = 100, 200
    threshold = st.slider('Select your left & right threshold for Canny', 
                          min_value=0, max_value=255, value=(Lthres_0, Rthres_0), 
                          key='slider', on_change=update_numeric2inp)
    
    # Set up numeric inputs for left and right threshold
    lthres, rthres = st.columns(2)
    with lthres:
        left_threshold = st.number_input('Left Threshold', 
                                        min_value=0, max_value=255, value=Lthres_0,
                                        key='left_threshold', on_change=update_slider2inp)
    with rthres:
        right_threshold = st.number_input('Right Threshold', 
                                          min_value=left_threshold, max_value=255, value=threshold[1], 
                                          key='right_threshold', on_change=update_slider2inp)
    
    # Define the filename for saving the processed image
    thres = "-".join(f"{num}" for num in threshold)
    save_name = name + "_edge" + thres
    saved = st.text_input("Enter save filename", save_name)
    if saved != save_name:
        save_name = saved + '_0'
    save_filename = folder_path + save_name + format_img

    # Add a button for downloading the processed image
    download = st.button("Download your image")

# Column 2: Display image preview
with col2:
    st.write("Preview Image")
    st.image(image)

# Process the image if it's loaded
if image is not None:
    # Apply Canny edge detection with the specified thresholds
    img1 = EdgeDetect(image, threshold)

    # Save the processed image if the download button is clicked
    if download:
        cv2.imwrite(save_filename, cv2.cvtColor(img1, cv2.COLOR_RGB2BGR))
        st.success(f'Download successfully `{save_filename}`', icon=":material/check_circle:")

    # Display the edge-detected image
    st.write("Edge Detected Result")
    st.image(img1)
