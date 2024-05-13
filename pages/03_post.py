import streamlit as st 
from PIL import Image
import io
import json 
import hashlib
import time 

if st.session_state["username"] is None:
    quit()

img=st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
if img is not None:
    image_bytes=img.getvalue()
    image_stream = io.BytesIO(image_bytes)

    # Open the image using PIL
    image = Image.open(image_stream)
    st.image(image, caption='Uploaded Image', use_column_width=True)

with open('msg.json','r') as f: 
    data=json.load(f)
promt=st.text_area("Description:")
if st.button("Submit"):
    user="user3"+str(hashlib.sha256(image_bytes).hexdigest())+str(time.time_ns)
    data[user]=[image_bytes.decode('latin1'),str(promt),[],[]]
# Create a BytesIO object
with open('msg.json','w') as f:
    json.dump(data,f)

