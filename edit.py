from PIL import Image
from streamlit_cropper import st_cropper
from function import *
from upload import *

col1, col2 = st.columns([0.5, 0.5])
with col1:
  # Select input file
  filename = file_selector('seg')
  st.write('You choose `%s`' % filename)

  # Extract path
  folder_path = filename.split("/")[0]+"/"
  format_img = "."+filename.split('.')[-1]
  name = filename.split("/")[1].split("_")[0]

  # Image read
  image = cv2.imread(filename)
  image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
  
  # Select parameter inputs
  Atxt, Aslider = st.columns([0.2, 0.8])
  with Atxt:
    angle_txt = st.number_input('Angle', 0, 360, value = 90, 
                                key = 'numeric', on_change = update_slider)
  with Aslider:
    angle = st.slider('Select rotated angle', 0, 360, angle_txt,
                       1, key = 'slider', on_change= update_numin)
  scale = st.slider('Select scale level', 0.5, 3.0, 2.0, 0.5)

  color, ratio = st.columns([0.2, 0.8])
  with color:
    box_color = st.color_picker(label="Box Color", 
                                value='#0000FF')
  with ratio:
    aspect_choice = st.radio(label="Aspect Ratio", 
                            options=["21:9", "18:9","16:9", "4:3", "3:2", "1:1", "Free"], 
                            horizontal=True)
    
  zoomout = st.radio(label="Output zoom", 
                            options=["Full image", "By scale","Original"], 
                            horizontal=True)
  aspect_dict = {
      "1:1": (1, 1),
      "21:9": (21, 9),
      "18:9": (18,9),
      "16:9": (16, 9),
      "4:3": (4, 3),
      "3:2": (3, 2),
      "Free": None
  }
  aspect_ratio = aspect_dict[aspect_choice]
  
  # Enter saved filename
  save_name = name.split('_')[0] + "_S" + str(int(scale*2)) + "_R" + str(angle)
  crop_idx = "_C" + aspect_choice
  if aspect_choice != "Free":
    crop_idx = "_C"+aspect_choice.split(":")[0]+"-"+aspect_choice.split(":")[1]
  save_name = save_name+crop_idx
  saved = st.text_input("Enter save filename", save_name)
  if saved != save_name:
    save_name = saved + '_0'
  save_filename = folder_path + save_name + format_img

  # Download button
  download = st.button("Download your image")
with col2:
  st.write("Preview Image")
  st.image(image)
flag = 0



if image is not None:
  img1 = ScaleRotate(image, scale, angle, zoomout)
  PIL_image = Image.fromarray(img1.astype('uint8'), 'RGB')
  cropped_img = st_cropper(PIL_image, realtime_update=1, 
                            box_color=box_color,
                            aspect_ratio=aspect_ratio)
  st.write("Preview Output")
  st.image(cropped_img)
  if download:
    cv2.imwrite(save_filename, cv2.cvtColor(img1, cv2.COLOR_RGB2BGR))
    st.success('Save image successfully `%s`' % save_filename, 
                icon=":material/check_circle:")


