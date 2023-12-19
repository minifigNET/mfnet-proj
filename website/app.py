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

# TODO - decide whether we should remove this code, we can return it later when we are allowing people to contribute?

st.markdown('## Can you help us to learn more?')
st.write("You know the name of your minifig, but we don't have it in our database?")
st.write("If so, please help us out!")

st.text("")
st.text("")



class_options = [

    ('No: 43 - Marvel Collectible Minifigure Series 1 (Set Number: 71039)', ['Goliath', 'She-Hulk', 'Echo', 'Kate Bishop', 'Hawkeye',
                                                                            'Moon Knight', 'Mr. Knight', 'Storm', 'Beast',
                                                                            'Wolverine', 'Agatha Harkness', 'The Werewolf']),
    ('No: 42 - Disney 100 Minifigure Series (Set Number: 71038)', ['Pocahontas', 'Aurora', 'Mulan', 'Tiana', 'The Queen',
                                                                    'Queen of Hearts', 'Dr Facilier', 'Cruella de Vil & Dalmatian puppy',
                                                                    'Sorcerers Apprentice Mickey', 'Pinocchio', 'Jimmy Cricket',
                                                                    'Michael', 'Dante', 'Ernesto de la Cruz', 'Stitch 626',
                                                                    'Oswald the Lucky Rabbit', 'Robin Hood', 'Prince John', 'Baymax']),
    ('No: 41 - Series 24 (Set Number: 71037)', ['T-Rex Fan Costume', 'Rococo Aristocrat', 'Robot Warrior', 'Potter',
                                                'Newspaper Kid', 'Orc', 'Soccer Referee', 'Falconer', 'Conservationist',
                                                'Carrot Mascot', 'Brown Astronaut and Spacebaby', 'Rockin Horse Rider']),
    ('No: 40 - Series 23 (Set Number: 71034)', ['Green Dragon Costume', 'Knight of the Yellow Castle'
                                                 'Cardboard Robot', 'Popcorn Costume', 'Nutcracker', 'Sugar Fairy', 'Ferry Captain',
                                                 'Turkey Costume', 'Wolf Costume', 'Snowman', 'Reindeer Costume', 'Holiday Elf']),
    ('No: 39 - Muppets Series (Set Number: 71033)', ['Statler', 'Waldorf', 'Dr. Bunsen Honeydew', 'Beaker', 'Animal', 'Miss Piggy',
                                                     'Kermit the Frog', 'Rowlf the Dog', 'The Swedish Chef', 'Gonzo', 'Janice', 'Fozzie Bear']),
    ('No: 38 - Series 22 (Set Number: 71032)', ['Figure Skating Champion', 'Snow Guardian', 'Chili Costume Fan',
                                                'Racoon Costume Fan', 'Forest Elf', 'Night Protector', 'Space Creature',
                                                'Robot Repair Tech', 'Troubadour']),
    ('No: 37 - Marvel Collectible Minifigure Series 2 (Set Number: 71031)', ['Captain America', 'Winter Soldier', 'The Scarlet Witch',
                                                                            'The Vision', 'Monica Rambeau', 'Gamora', 'Zombie Hunter Spidey',
                                                                            'Zombie Captain America', 'Captain Carter', 'TChalla Star Lord',
                                                                            'Loki', 'Sylvie']),
    ('No: 36 - Looney Tunes Series (Set Number: 71030)', ['Bugs Bunny', 'Lola Bunny', 'Daffy Duck', 'Tweety Bird', 'Sylvester', 'Road Runner',
                                                          'Wile E. Coyote', 'Porky Pig', 'Petunia Pig', 'Speedy Gonzales', 'Tasmanian Devil',
                                                          'Marvin the Martian']),
    ('No: 35 - Series 21 (Set Number: 71029)', ['Centaur Warrior', 'Shipwreck Survivor', 'Pug Costume Guy', 'Beekeeper',
                                                'Ladybug Girl', 'Violin Kid', 'Alien', 'Space Police Guy', 'Ancient Warrior',
                                                'Airplane Girl', 'Cabaret Singer', 'Paddle Surfer']),
    ('No: 34 - Harry Potter Series 2 (Set Number: 71028)', ['Harry Potter', 'Hermione Granger™', 'Ron Weasley™', 'Ginny Weasley',
                                                            'Fred Weasley','George Weasley', 'Luna Lovegood™', 'Moaning Myrtle', 'Griphook',
                                   'Headmaster Albus Dumbledore™', 'Professor Sprout', 'Neville Longbottom™',
                                  'Kingsley Shacklebolt', 'Bellatrix Lestrange', 'Lily Potter', 'James Potter']),
    ('No: 33 = Series 20 (Set Number: 71027)', ['Piñata boy', 'Pajama girl', 'Drone boy', '80s musician', 'Peapod costume girl', 'Sea rescuer', 'Viking',
                                'Pirate girl', 'Martial arts boy', 'Breakdancer', 'Llama costume girl', 'Brick costume guy', 'Athlete',
                                        'Space fan', 'Super warrior', 'Tournament knight']),
    ('No: 32 - DC Super Heroes Series (Set Number: 71026)', ['Batman', 'Superman', 'The Joker', 'Huntress', 'Metamorpho', 'Sinestro',
                                                             'Green Lantern', 'Mr. Miracle', 'Bat-Mite', 'Star Girl', 'Cheetah', 'Aquaman',
                                                    'Cyborg', 'BUMBLEBEE', 'The Flash', 'Wonder Woman']),
    ('No: 31 - Series 19 (Set Number: 71025)', ['Dog Sitter', 'Video Game Champ', 'Shower Guy', 'Rugby Player', 'Bear Costume Guy',
                                                'Pizza Costume Guy', 'Galactic Bounty Hunter', 'Monkey King', 'Programmer',
                                                'Gardener', 'Fire Fighter', 'Mountain Biker', 'Fright Knight', 'Mummy Queen',
                                                'Jungle Explorer', 'Fox Costume Girl']),
    ('No: 30 - Disney Series 2[ (Set Number: 71024)', ['Vintage Mickey', 'Vintage Minnie', 'Hercules', 'Jack Skellington',
                                                        'Scrooge McDuck', 'Huey, Dewey', 'Louie', 'Chip', 'Dale', 'Jasmine',
                                                        'Jafar', 'Hades', 'Elsa', 'Anna', 'Sally', 'Edna', 'Frozone'])
]

# selected_class = st.selectbox('What class does your minifig belong to?', [option[0] for option in class_options])


# for option, characters in class_options:
#     if selected_class == option:
#         selected_character = st.selectbox('What is the character name?', characters)
#         st.write(f'You selected {option}:', selected_character)
#         break

# st.text("")
# st.text("")

## NEW DROPDOWN INCLUDING API CALL

response = requests.get('http://127.0.0.1:8000/retrieve_metadata')

if response.status_code == 200:
    data = response.json()

    selected_data = st.selectbox('Select data:', data)

    st.write(f'You selected: {selected_data}')

if selected_data:
    data = {
            "class": selected_data[0]
        }

    response = requests.post('http://127.0.0.1:8000/add_img_train',
                                        params = data
                                        )
    if response.status_code == 200:
        st.markdown('### Added to database:')
        st.write("Tada! Thank you, we've added that image to the database. 😊")

    # else:
    #     st.markdown("**Oops**, something went wrong 😓 Please try again.")
    #     print(response.status_code, response.content)



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
