import streamlit as st
import numpy as np
import pandas as pd 
import json
import hashlib
import io
from PIL import Image
import platform 
import socket

if st.session_state["username"] is None:
    quit()

# Load existing messages from JSON file
with open("msg.json", "r") as f:
    auth = json.load(f)

# Chat input
prompt = st.chat_input("Say something")
#image input


# Update JSON file with new messages
if prompt:
    auth["user" + str(hashlib.sha256(prompt.encode()).hexdigest())[:8]] = ["",str(prompt),[],[]]
    with open("msg.json", "w") as f:
        json.dump(auth, f)
username=st.session_state["username"]
# Display existing messages
for i in auth:
    score=1
    with st.chat_message("user"):
        st.write("Name\n")
        if auth[i][0]:
            image_stream = io.BytesIO(auth[i][0].encode('latin1'))
            # Open the image using PIL
            image = Image.open(image_stream)
            st.image(image, caption='', use_column_width=True)
        if auth[i][1]:
            st.write(auth[i][1])
        c1,c2=st.columns(2)
        if c1.button(f"👍 {len(set(auth[i][2]))}",key=i+"up"):
            auth[i][2].append(username)
            try:
                auth[i][3].remove(username)
            except:
                pass
            auth[i][2]=list(set(auth[i][2]))
        if c2.button(f"👎 {len(set(auth[i][3]))}",key=i+"d"):
            auth[i][3].append(username)
            try:
                auth[i][2].remove(username)
            except: 
                pass
            auth[i][3]=list(set(auth[i][3]))
    with open("msg.json", "w") as f:
        json.dump(auth, f)


