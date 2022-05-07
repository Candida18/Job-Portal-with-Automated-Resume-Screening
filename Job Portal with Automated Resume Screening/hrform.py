from docx2txt.docx2txt import process
import streamlit as st
import streamlit as st
import streamlit.components.v1 as stc
import sqlite3 as sql
import pandas as pd

# File Processing Pkgs
import pandas as pd
import docx2txt
from PIL import Image
from PyPDF2 import PdfFileReader
import pdfplumber
import os
import webbrowser


st.title("Post A Job")


# DB Management
import sqlite3

conn = sqlite3.connect("jobdesc_data.db")
c = conn.cursor()
# DB  Functions
def create_jobdesc():
    c.execute(
        "CREATE TABLE IF NOT EXISTS jobdesc(name TEXT,date NUMBER,Job_Desc TEXT)"
    )


def add_userdata(name, date, Job_Desc):
    c.execute(
        "INSERT INTO jobdesc(name, date, Job_Desc) VALUES (?,?,?)",
        (name, date, Job_Desc),
    )
    conn.commit()


def main():

    my_form = st.form(key="form1", clear_on_submit=True)
    name = my_form.text_input(label="Enter your Job Title")
    docx_file = my_form.file_uploader(
        label="Upload The Job Description Here", type=["docx"])
    date = my_form.date_input("Select Deadline for Applying")
    

    ####### Saves Resume in Local Directory #######
    if docx_file is not None:

        # Saving upload
        with open(
            os.path.join( "Data/JobDesc/", docx_file.name), "wb"
        ) as f:
            f.write((docx_file).getbuffer())

            #st.success("File Saved")

    ###

    submit = my_form.form_submit_button(label="Submit this form")
    Job_Desc = text_resume(docx_file)

    ###### View Resume ######

    # if st.button("Open browser"):
    #     webbrowser.open_new_tab(
    #         "C:/Users/noron/ResumeStreamlit3/Dir/{}".format(docx_file.name)
    #     )

    if submit:
        create_jobdesc()
        add_userdata(name, date, Job_Desc)
        st.success("You have successfully submitted the form")

    connection = sql.connect("jobdesc_data.db")
    df = pd.read_sql(sql="Select * FROM jobdesc", con=connection)
    df.to_csv("CSV/JobDesc_data.csv", index=False)


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
            
            return raw_text


if __name__ == "__main__":
    main()
