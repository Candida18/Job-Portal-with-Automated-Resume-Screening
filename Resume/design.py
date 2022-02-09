from PIL import Image
import streamlit as st
import fileReader
import os
from operator import index
from pandas._config.config import options
import Cleaner
import textract as tx
import pandas as pd
import os
import tf_idf
import streamlit as st

st.markdown("<h1 style='text-align: center;font-size:350%'>RESUME SCREENING</h1><br>", unsafe_allow_html=True)
resume_dir = "Data/Resumes/"
job_desc_dir = "Data/JobDesc/"
resume_names = os.listdir(resume_dir)
job_description_names = os.listdir(job_desc_dir)

text = fileReader.read_resumes(resume_names, resume_dir)
st.write(text)
image = Image.open("Images/firstimage.png")
st.image(image,use_column_width=True)

