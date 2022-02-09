from dbm.dumb import _Database
from numpy import empty
from soupsieve import select
from sqlalchemy import null
import streamlit as st
import pandas as pd
import time
import requests
from streamlit_lottie import st_lottie
from streamlit_lottie import st_lottie_spinner
import plotly.graph_objects as go
from dbm.dumb import _Database
from imaplib import _Authenticator
from multiprocessing import AuthenticationError
from operator import index
from soupsieve import select


import time
import os


import csv


# Security
#passlib,hashlib,bcrypt,scrypt
import hashlib
job_desc_dir = "Data/JobDesc/"
job_description_names = os.listdir(job_desc_dir)

def app():
    st.title('Login')

    st.write("This is the `Login` page of the multi-page app.")

def make_hashes(password):
	return hashlib.sha256(str.encode(password)).hexdigest()

def check_hashes(password,hashed_text):
	if make_hashes(password) == hashed_text:
		return hashed_text
	return False
# DB Management
import sqlite3 
conn = sqlite3.connect('data.db')
c = conn.cursor()
# DB  Functions
def create_usertable():
	c.execute("CREATE TABLE IF NOT EXISTS userstable(name TEXT not null,username TEXT  not null,password TEXT not null)")


def add_userdata(name,username,password):
	c.execute('INSERT INTO userstable(Name,username,password) VALUES (?,?,?)',(name,username,password))
	conn.commit()

def login_user(username,password):
	c.execute('SELECT * FROM userstable WHERE username =? AND password = ?',(username,password))
	data = c.fetchall()
	return data

#def new_user_name(name,username):
#	c.execute('SELECT username FROM userstable Where name =? AND username=?', (name,username))
#	new__user_name =c.fetchall()
#	return new__user_name

def view_all_users():
	c.execute('SELECT * FROM userstable')
	data = c.fetchall()
	return data



def main():
	"""Simple Login App"""

	

	menu = ["Home","Login","SignUp"]
	choice = st.sidebar.selectbox("Menu",menu)

	if choice == "Home":
		
		Jobs = pd.read_csv('Resume_data_fordebug.csv')
		#jds = pd.read_csv('jobdesc.csv')
		st.markdown("<h1 style='text-align:center;'>Welcome to ScreenRes</h1>", unsafe_allow_html=True)
		def load_lottieurl(url: str):
			r = requests.get(url)
			if r.status_code !=200:
				return None
			return r.json()

		lottie_url_rscreen = "https://assets9.lottiefiles.com/packages/lf20_azmnf6vt.json"

		lottie_rscreen = load_lottieurl(lottie_url_rscreen )
		st_lottie(lottie_rscreen, key="homegif")

		st.title('Job hunting made easier:')


		st.text('Job Positions Available:')
		index=st.selectbox('Pick one', Jobs['name'])

		#print(index)

		option_yn = st.selectbox("Show the Job Description ?", options=['YES', 'NO'])
		if option_yn == 'YES':
			st.markdown("---")
			st.markdown("### Job Description :")
			fig = go.Figure(data=[go.Table(
        		header=dict(values=["Job Description"],
                   			 fill_color='#f0a500',
                    		align='center', font=dict(color='white', size=16)),
        		cells=dict(values=[Jobs['resume']],
                   			fill_color='#f4f4f4',
                   			align='left'))])

			fig.update_layout(width=800, height=500)
			st.write(fig)
			st.markdown("---")
####################################
		#	st.button("Apply now")

			if (st.button("Apply now")):
                st.title("Enter you details to aply for job")
                
                

              


	elif choice == "Login":
		
		st.title(" Login ")
		#username = st.sidebar.text_input("User Name")
		username = st.text_input("User Name")
		password = st.text_input("Password",type='password')
		if st.button("Login"):
			# if password == '12345':
			create_usertable()
			hashed_pswd = make_hashes(password)

			result = login_user(username,check_hashes(password,hashed_pswd))
			if result:

				st.success("Logged In as {}".format(username))

				task = st.selectbox("Task",["Add Post","Analytics","Profiles"])
				if task == "Add Post":
					st.subheader("Add Your Post")

				elif task == "Analytics":
					st.subheader("Analytics")
				elif task == "Profiles":
					st.subheader("User Profiles")
					user_result = view_all_users()
					clean_db = pd.DataFrame(user_result,columns=["Username","Password"])
					st.dataframe(clean_db)
			else:
				st.warning("Invalid credentials")





	elif choice == "SignUp":
		st.title(" SignUp ")
		st.subheader("Create New Account")
		new_name = st.text_input("Name")	
		#new_DOB = st.text_input("Birthdate")
		#new_age = st.text_input("Age")
		new_user = st.text_input("Username")
		new_password = st.text_input("Password",type='password')
#submit_button = st.form_submit_button(label = 'Submit', on_click = get_save)
# st.form_submit_button	
		if st.button(label='Signup'):
			create_usertable()
			add_userdata(new_name,new_user,make_hashes(new_password))
			#new_user_name(new_name,new_user)
			st.success("You have successfully created a valid Account")
			st.info("Go to Login Menu to login")
			st.success


if __name__ == '__main__':
	main()

	################signup################


	# elif choice == "SignUp":
	# 	st.title(" SignUp ")
	# 	st.subheader("Create New Account")
	# 	new_name = st.text_input("Name")			
	# 	new_user = st.text_input("Username")
	# 	new_password = st.text_input("Password",type='password')
	# 	if st.button(label='Signup'):
	# 		create_usertable()
	# 		add_userdata(new_name,new_user,make_hashes(new_password))
	# 		#new_user_name(new_name,new_user)
	# 		st.success("Welcome {} !".format(new_user))
	# 		st.success("You have successfully created a valid Account! ")
	# 		st.info("Login using your valid credentials")
	# 		#st.success