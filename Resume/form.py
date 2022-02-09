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

job_desc_dir = "./Data/JobDesc/"
job_description_names = os.listdir(job_desc_dir)
print(job_description_names)



# DB Management
import sqlite3

conn = sqlite3.connect("form_data.db")
c = conn.cursor()
# DB  Functions
def create_userinfo():
	c.execute(
		"CREATE TABLE IF NOT EXISTS userinfo(name TEXT,dob DATE,email TEXT,phone TEXT,jobs TEXT,resume TEXT)"
	)


def add_userdata(name, dob, email, phone, jobs, resume):
	c.execute(
		"INSERT INTO userinfo(name,dob,email,phone,jobs,resume) VALUES (?,?,?,?,?,?)",
		(name, dob, email, phone, jobs, resume),
	)
	conn.commit()


def login_user(name, dob, email, phone, jobs, resume):
	c.execute(
		"SELECT * FROM userinfo WHERE name =? AND dob = ? AND email = ? AND phone = ? AND jobs = ? AND resume = ?",
		(name, dob, email, phone, jobs, resume),
	)
	data = c.fetchall()
	return data


def view_all_users():
	c.execute("SELECT * FROM userinfo")
	data = c.fetchall()
	return data


def main():
	st.title("Enter Your Details To Apply For The Job")
	Jobs = pd.read_csv("CSV/JobDesc_data.csv")
		
	my_form = st.form(key="form1", clear_on_submit=True)
	name = my_form.text_input(label="Enter your name")
	dob = my_form.date_input(label="Enter your DOB",min_value = datetime.date(1990, 1, 1))
	email = my_form.text_input(label="Enter your Email Id")
	phone = my_form.text_input(label="Enter your Contact Number",max_chars = 10)
	jobs = my_form.selectbox(
	label="Select the Job Domain",options=Jobs['name'])

	docx_file = my_form.file_uploader(label="Upload Your Resume Here", type=["docx"])

	####### Saves Resume in Local Directory #######
	if docx_file is not None:

		with open(
			os.path.join("./Resume/Data/Resume", docx_file.name), "wb"
		) as f:
			f.write((docx_file).getbuffer())

	submit = my_form.form_submit_button(label="Submit this form")
	resume = text_resume(docx_file)


	if submit:
		create_userinfo()
		add_userdata(name, dob, email, phone, jobs, resume)
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
			print(raw_text)
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
			print(raw_text)
			return raw_text


if __name__ == "__main__":
	main()
