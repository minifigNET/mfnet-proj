import streamlit as st
import base64

st.set_page_config(
            page_title="MinifigNET",
            page_icon="🐍",
            layout="centered", # wide
            initial_sidebar_state="auto") # collapsed


@st.cache(allow_output_mutation=True)
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_png_as_page_bg(png_file):
    bin_str = get_base64_of_bin_file(png_file)
    page_bg_img = '''
    <style>
    body {
    background-image: url("data:image/png;base64,%s");
    background-size: cover;
    }
    </style>
    ''' % bin_str

    st.markdown(page_bg_img, unsafe_allow_html=True)
    return

# set_png_as_page_bg('')

#Link to database and search function

st.title('MinifigNET')
st.write('Can’t remember the names of your LEGO minifigs? Now there’s an app for that!')



st.title('Upload a photo of your minifig here')
uploaded_file = st.file_uploader("Upload your file here...", type=['png', 'jpeg', 'jpg'])

if uploaded_file is not None:
    st.image(uploaded_file)

st.title('Minifig name')

user_text = st.text_input('Do you know the name of this minifig? If so, please let us know:')
st.write(f'You entered: {user_text}')

# Query the database based on user input
