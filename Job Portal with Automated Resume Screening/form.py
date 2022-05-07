from cProfile import label
from docx2txt.docx2txt import process
import streamlit as st
import streamlit as st
import streamlit.components.v1 as stc
import sqlite3 as sql
import pandas as pd
import datetime

# File Processing Pkgs
import pandas as pd
import docx2txt
from PIL import Image
from PyPDF2 import PdfFileReader
import pdfplumber
import os
import webbrowser

job_desc_dir = "Data/JobDesc/"
job_description_names = os.listdir(job_desc_dir)
#print(job_description_names)



# DB Management
import sqlite3

conn = sqlite3.connect("form_data.db")
c = conn.cursor()
# DB  Functions
def create_userinfo():
	c.execute(
		"CREATE TABLE IF NOT EXISTS userinfo(name TEXT,age NUMBER,email TEXT,phone TEXT,jobs TEXT, FileName TEXT,resume TEXT, gender TEXT, openness NUMBER, neuroticism NUMBER, conscientiousness NUMBER, agreeableness NUMBER, extraversion NUMBER)"
	)


def add_userdata(name, age, email, phone, jobs, filename, resume,gender, openness, neuroticism, conscientiousness, agreeableness, extraversion):
	c.execute(
		"INSERT INTO userinfo(name,age,email,phone,jobs,FileName,resume, gender, openness, neuroticism, conscientiousness, agreeableness, extraversion) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)",
		(name, age, email, phone, jobs, filename,resume, gender ,openness, neuroticism, conscientiousness, agreeableness, extraversion),
	)
	conn.commit()



def main():
	st.title("Job Application")
	Jobs = pd.read_csv("CSV/JobDesc_data.csv")
		
	my_form = st.form(key="form1", clear_on_submit=True)
	my_form.subheader("Enter Your Details To Apply For The Job")
	name = my_form.text_input(label="Enter your name")
	age = my_form.text_input(label="Enter your Age")
	email = my_form.text_input(label="Enter your Email Id")
	phone = my_form.text_input(label="Enter your Contact Number",max_chars = 10)
	# gender = my_form.radio('Select your Gender:', ['Male', 'Female'])
	gender = my_form.text_input(label="Enter your gender ( 1 - Male, 0 - Female)", max_chars = 1)
	jobs = my_form.selectbox(
	label="Select the Job Domain",options=Jobs['name'])

	docx_file = my_form.file_uploader(label="Upload Your Resume Here", type=["docx"])
	my_form.markdown("---")
	my_form.subheader("Tell Us About Yourself")
	openness = my_form.slider('Do you enjoy new experiences (Openness) ?', 0, 10)
	neuroticism = my_form.slider('How often do you feel negativity (Neuroticism) ?', 0, 10)
	conscientiousness = my_form.slider('Would you do your work well and thoroughly (Conscientiousness) ? ', 0, 10)
	agreeableness = my_form.slider('How much would you like to work with your peers (Agreeableness) ? ', 0, 10)
	extraversion = my_form.slider('How outgoing and social interactive are you (Extraversion) ?', 0, 10)
	####### Saves Resume in Local Directory #######
	if docx_file is not None:

		with open(
			os.path.join("C:/Users/Gini/Mini Project/Final_ResumePPV2/Data/Resume", docx_file.name), "wb"
		) as f:
			f.write((docx_file).getbuffer())

	submit = my_form.form_submit_button(label="Submit your application")
	resume = text_resume(docx_file)
	
	if docx_file is not None:

		filename = docx_file.name

	if submit:
		create_userinfo()
		add_userdata(name, age, email, phone, jobs, filename, resume, gender, openness, neuroticism, conscientiousness, agreeableness, extraversion)
		st.success("You have successfully submitted the form")



	connection = sql.connect("form_data.db")
	df = pd.read_sql(sql="Select * FROM userinfo", con=connection)
	df.to_csv("CSV/Form_data.csv", index=False)


def text_resume(docx_file):
	if docx_file is not None:

		# Check File Type
		if docx_file.type == "text/plain":

			st.text(str(docx_file.read(), "utf-8"))  # empty
			raw_text = str(
				docx_file.read(), "utf-8"
			)  # works with st.text and st.write,used for further processing
			#print(raw_text)
			return raw_text

		elif docx_file.type == "application/pdf":

			try:
				with pdfplumber.open(docx_file) as pdf:
					page = pdf.pages[0]
					raw_text = page.extract_text()
				return raw_text
			except:
				st.write("None")

		elif (
			docx_file.type
			== "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
		):
			# Use the right file processor ( Docx,Docx2Text,etc)
			raw_text = docx2txt.process(docx_file)  # Parse in the uploadFile Class
			#print(raw_text)
			return raw_text


if __name__ == "__main__":
	main()
