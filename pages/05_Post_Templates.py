import streamlit as st 
import json 

with open("inter.json","r") as f: 
    data=json.load(f)
name=str(len(data))
img=st.file_uploader("Template",type=["jpg", "jpeg", "png"])

des=st.text_area("Description of your template:")

if st.button("Publish"):
    
    data[name]={"id": "", "name": des, "url": "", "width": 1200, "height": 1200, "box_count": 2, "captions": 1236000, "image": ""}
    data[name]["image"]=img.getvalue().decode('latin1')
with open("inter.json","w") as f:
    json.dump(data,f)