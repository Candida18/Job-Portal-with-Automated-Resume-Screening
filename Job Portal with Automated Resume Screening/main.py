import streamlit as st
from PIL import Image
import os
menu = ["Home","Post a Job","View Statistics"]
choice = st.sidebar.selectbox("Menu",menu)

if choice=="Home":
    st.markdown("<h1 style='text-align: center;font-size:350%'>RESUME SCREENING</h1><br>", unsafe_allow_html=True)
    image = Image.open("Images/firstimage.png")
    st.image(image,use_column_width=True)
    
elif choice == "View Statistics":
    os.system("streamlit run app.py --server.port 9001")

elif choice == "Post a Job":
    os.system("streamlit run hrform.py --server.port 9002")
