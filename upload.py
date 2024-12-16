from function import *

# Display header to guide the user
st.header("Upload your image to process!")

# File uploader widget to allow image upload (png or jpg)
img_file = st.file_uploader(label='Upload a file', type=['png', 'jpg'])

# Check if the user has uploaded an image
if img_file is not None:
    # Notify the user of successful upload
    st.success("App: Successfully upload", icon=':material/check_circle:')
    
    # Convert the uploaded file into a numpy array
    file_bytes = np.asarray(bytearray(img_file.read()), dtype=np.uint8)
    
    # Decode the image from the byte array
    image = cv2.imdecode(file_bytes, 1)
    
    # Convert the image from BGR to RGB (OpenCV uses BGR by default)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    # Display the uploaded image
    st.image(image)
    
    # Generate a filename for saving the image (based on original name)
    filename = "img/" + img_file.name.split('.')[0] + '_0.' +  img_file.name.split('.')[-1]
    
    # Save the uploaded image to disk
    cv2.imwrite(filename, cv2.cvtColor(image, cv2.COLOR_RGB2BGR))
    
    # Show the shape of the image (height, width, and number of channels)
    st.write(image.shape)

# Select an image from the "img/" directory using the file_selector function
filename = file_selector("img/")
st.write(f'You choose `{filename}`')

# Read the selected image using OpenCV
image = cv2.imread(filename)

# Convert the image from BGR to RGB for proper display
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# Display the preview of the selected image
st.write("Preview Image")
st.image(image)
