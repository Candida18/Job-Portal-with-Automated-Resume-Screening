from dbm.dumb import _Database
from imaplib import _Authenticator
from multiprocessing import AuthenticationError
from operator import index
from soupsieve import select
import streamlit as st
import pandas as pd
import time
import requests
import streamlit_lottie
from streamlit_lottie import st_lottie
from streamlit_lottie import st_lottie_spinner
import plotly.graph_objects as go
import Images
import csv
import os
import form
#import streamlit_authenticator as stauth
#from link_button import link_button





# Security
#passlib,hashlib,bcrypt,scrypt
import hashlib


def main():

##############home#############


	Jds = pd.read_csv('CSV/JobDesc_data.csv')
	#jds = pd.read_csv('jobdesc.csv')
	st.markdown("<h1 style='text-align:center;'>Welcome to ScreenRes</h1>", unsafe_allow_html=True)
	def load_lottieurl(url: str):
		r = requests.get(url)
		if r.status_code !=200:
			return None
		return r.json()

	lottie_url_rscreen = "https://assets9.lottiefiles.com/packages/lf20_azmnf6vt.json"

	lottie_rscreen = load_lottieurl(lottie_url_rscreen )
	st_lottie(lottie_rscreen, key="homegif",height="350px")

	#image = Images.open("Images/firstimage.png")
	#image = open("Images/firstimage.png")
	#st.image(image,use_column_width=True)

		#############
	st.subheader('We are hiring for : ')

	index = [a for a in range (len(Jds['name']))] 
	fig = go.Figure(data=[go.Table(
		header=dict(values=["Job Code", "Job Post Name"],
				line_color="white",
				fill_color="#234f92",
				font_color="white",
				align='center', font=dict(color='white', size=16)),
		cells= dict(values=[index,Jds['name']],
				fill_color='#f4f4f4',
				line_color="#0d2840",
				font_color="#0d2840",
				height=25,
				align='center'))])
	fig.update_layout(width=700,height=400)
	st.write(fig)
		
	index=st.slider("Which Jobs Positions' details would you  like to see?:",0,len(Jds['name'])-1,1)
	option_yn = st.selectbox("Show the Job Description ?", options=['YES', 'NO'])
	if option_yn == 'YES':
		st.markdown("---")
		st.markdown("### Job Description: ")
		fig= go.Figure(data=[go.Table(
			header=dict(values=["Job Description"],
					line_color="white",
					fill_color="#234f92",
					font_color="white",
					align='center', font=dict(color='white', size=16)),
			cells= dict(values=[Jds['Job_Desc'][index]],
					fill_color='#f4f4f4',
					line_color="#0d2840",
					font_color="#0d2840",
					height=25,
					align='left'))])
		fig.update_layout(width=800,height=500)
		st.write(fig)
		st.markdown("---")

	if(st.button("Apply now")):
		os.system("streamlit run form.py --server.port 9000")
		#form.main()
#############################################################################

if __name__ == '__main__':
	main()
