######
# Notes
######

# TO OPEN THE FILE ONLINE: streamlit run app.py
# or now: https://minifignet.streamlit.app

########
# Imports
########
import streamlit as st
from PIL import Image
import requests
import html

#####################
# Set up the page style
#####################

st.set_page_config(
    page_title="MinifigNET",
    page_icon="https://cdn-icons-png.flaticon.com/512/1674/1674274.png",
    layout="centered")


st.write("""
    <style>
        h1 {
            color: red;
            font-size: 96px !important;
        }
        h2 {
            color: red;
        }
    </style>""", unsafe_allow_html=True)


#####################
# Header
#####################

st.title('MinifigNET ![](https://lh3.googleusercontent.com/u/2/drive-viewer/AEYmBYR3Q5FtiJs9Eo-azS4c1phN_j0FsKqwYQbE7u259ys-0dkmPINtwIaJwfZN1YezGMfppva0383ja1ncwtaBC223GYDWqw=w2940-h1538 "Ho ho ho!")')

st.markdown(
    '##### Can’t remember the names of your LEGO minifigs? Now there’s an app for that!')

st.text("")
st.text("")
st.text("")

#####################
# Resizing + cropping function
#####################


def resize_224(picture):
    img = Image.open(picture)
    width, height = img.size
    aspect = width / height

    if aspect > 1:
        new_width = height
        start_x = (width - height) / 2
        img = img.crop((start_x, 0, start_x + new_width, height))
    else:
        new_height = width
        start_y = (height - width) / 2
        img = img.crop((0, start_y, width, start_y + new_height))

    return img.resize((224, 224))


#####################
# Let the user take a photo from the app
# (more info on camera input here:
# https://docs.streamlit.io/library/api-reference/widgets/st.camera_input)
#####################
st.markdown('## Take a photo of your minifig ...')
st.write('and we\'ll tell you what it\'s called!')

if st.button("📸 Open camera"):
    if "upload" in st.session_state:
        del st.session_state.upload
    st.camera_input("ℹ️ Please try to take a clear photo, against a white background, and centre your subject 🎯", key="capture")


#############################################
# Let the user upload a photo of their minifig
#############################################
st.markdown('## ... or upload one if you prefer')

st.file_uploader("Select a photo (preferably with the subject in the centre):",
                 type=['png', 'jpeg', 'jpg'], key="upload")

#####################################################
# check the image against the model, return the answer
#####################################################
prediction = None
photo = st.session_state.capture if "capture" in st.session_state \
    else st.session_state.upload if "upload" in st.session_state and st.session_state.upload \
    else None

if photo:
    st.markdown("## Now let's analyze your photo")
    photo = resize_224(photo)
    st.image(photo)

    with st.spinner("Analyzing..."):
        # Get bytes from the file buffer
        img_bytes = photo.convert("RGB").tobytes()

        # Make request to API
        response = requests.post(f'{st.secrets.API_URL}/predict',
                                 files={'img': img_bytes,
                                        })

        if response.status_code == 200:
            print("✅ Image analyzed successfully.")
            # prediction = {
            #     'probability': 0.99,
            #     'minifigure_name': "SANTA",
            #     'set_id': "99999",
            #     'set_name': "CHRISTMAS SET",
            #     'class_id': 99
            # }
            prediction = response.json()
            st.markdown('### This minifig is called:')
            st.write(f'{prediction["minifigure_name"]} ({prediction["probability"]:2.0%} sure). Tada! 😊')

        else:
            st.markdown("**Oops**, something went wrong 😓 Please try again.")
            print(response.status_code, response.content)


st.text("")
st.text("")


####################################
# ask for input to build our database
####################################
if prediction or st.session_state.get("selected_key", None):

    st.markdown('## Can you help us to learn more?')
    st.write("Our prediction was wrong but you know the name of your minifig?")
    st.write("If so, please help us out!")

    st.text("")
    st.text("")

    response = requests.get(f'{st.secrets.API_URL}/retrieve_metadata')

    if response.status_code == 200:
        data = response.json()

        selected_key = st.selectbox('Select data:', data.keys(), key="selected_key")
    else:
        st.markdown("**Oops**, something went wrong 😓 Please try again.")

    if st.button('Confirm') and selected_key:
        data = {
            "class_id": data[st.session_state.selected_key]
        }

        response = requests.post(f'{st.secrets.API_URL}/add_img_train',
                                 params=data
                                 )
        if response.status_code == 200:
            st.markdown('### Added to database:')
            st.write("Tada! Thank you, we've added that image to the database. 😊")
        else:
            st.markdown("**Oops**, something went wrong 😓 Please try again.")

    def sanitize_input(input_str):
        sanitized_str = html.escape(input_str)
        return sanitized_str

    st.write("Can't find your minifig in the dropdown menus? Please send us at least 8 photos from different angles and all the details you have. Name, series, set number - any information is helpful!")

    user_text = st.text_input("Name:")
    minifig_name = sanitize_input(user_text)
    user_text = st.text_input("Series:")
    minifig_series = sanitize_input(user_text)
    user_text = st.text_input("Set Number:")
    minifig_set = sanitize_input(user_text)

    st.file_uploader("Select a photo (preferably with the subject in the centre):", type=[
        'png', 'jpeg', 'jpg'], accept_multiple_files=True, key='class_upload')
    photo_classes = st.session_state.class_upload if "class_upload" in st.session_state and st.session_state.class_upload \
        else None

    if photo_classes and minifig_series and minifig_name and minifig_name:
        if len(photo_classes) > 7:
            photos = [resize_224(photo).convert("RGB").tobytes() for photo in photo_classes]
            data = {
                "lego_ids": minifig_set,
                "lego_names": minifig_series,
                "minifigure_name": minifig_name
            }
            files = [("imgs", (f"photo{i}", photo)) for i, photo in enumerate(photos)]
            # st.write(files)
            response = requests.post(f'{st.secrets.API_URL}/add_class',
                                     params=data,
                                     files=files
                                     )
            if response.status_code == 200:
                st.markdown('### Added to database:')
                st.write('Tada! 😊')
                photo_classes.clear()
            else:
                st.markdown("**Oops**, something went wrong 😓 Please try again.")
                print(response.status_code, response.content)

        else:
            st.write('Please add more photos')

    st.write(
        f'Thank you! You entered: {user_text}. We will add this to our database.')


#########################################
# code for adding any image copyright info
#########################################

st.text("")
st.text("")
st.text("")
