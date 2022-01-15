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


# def read_pdf(file):
#     pdfReader = PdfFileReader(file)
#     count = pdfReader.numPages
#     all_page_text = ""
#     for i in range(count):
#         page = pdfReader.getPage(i)
#         all_page_text += page.extractText()

#     return all_page_text

# def read_pdf2(file):
#     with pdfplumber.open(file) as pdf:
#         page = pdf.pages[0]
#     return page.extract_text()


st.title("Enter Your Details To Apply For The Job")


# DB Management
import sqlite3

conn = sqlite3.connect("resume_data.db")
c = conn.cursor()
# DB  Functions
def create_userinfo():
    c.execute(
        "CREATE TABLE IF NOT EXISTS userinfo(name TEXT,number NUMBER,email TEXT,phone TEXT,jobs TEXT,location TEXT,resume TEXT)"
    )


def add_userdata(name, number, email, phone, jobs, location, resume):
    c.execute(
        "INSERT INTO userinfo(name,number,email,phone,jobs,location,resume) VALUES (?,?,?,?,?,?,?)",
        (name, number, email, phone, jobs, location, resume),
    )
    conn.commit()


def login_user(name, number, email, phone, jobs, location, resume):
    c.execute(
        "SELECT * FROM userinfo WHERE name =? AND number = ? AND email = ? AND phone = ? AND jobs = ? AND location = ? AND resume = ?",
        (name, number, email, phone, jobs, location, resume),
    )
    data = c.fetchall()
    return data


def view_all_users():
    c.execute("SELECT * FROM userinfo")
    data = c.fetchall()
    return data


def main():

    my_form = st.form(key="form1", clear_on_submit=True)
    name = my_form.text_input(label="Enter your name")
    number = my_form.text_input(label="Enter your age")
    email = my_form.text_input(label="Enter your Email Id")
    phone = my_form.text_input(label="Enter your Contact Number")
    jobs = my_form.text_input(label="Search Jobs In the Domain You Want")
    location = my_form.text_input(label="Location")
    docx_file = my_form.file_uploader(
        label="Upload Your Resume Here", type=["txt", "docx", "pdf"]
    )

    ####### Saves Resume in Local Directory #######
    if docx_file is not None:
        # TO See details
        # file_details = {
        #     "filename": docx_file.name,
        #     "filetype": docx_file.type,
        #     "filesize": docx_file.size,
        # }
        # st.write(file_details)

        # Saving upload
        with open(
            os.path.join("C:/Users/noron/ResumeStreamlit3/Dir", docx_file.name), "wb"
        ) as f:
            f.write((docx_file).getbuffer())

            #st.success("File Saved")

    ###

    submit = my_form.form_submit_button(label="Submit this form")
    resume = text_resume(docx_file)

    ###### View Resume ######

    # if st.button("Open browser"):
    #     webbrowser.open_new_tab(
    #         "C:/Users/noron/ResumeStreamlit3/Dir/{}".format(docx_file.name)
    #     )

    if submit:
        create_userinfo()
        add_userdata(name, number, email, phone, jobs, location, resume)
        st.success("You have successfully submitted the form")


    # if st.button("View Details"):
    # 			view_all_users()
    # 			st.write(name)
    # 			st.write(number)
    # 			st.write(email)
    # 			st.write(phone)
    # 			st.write(jobs)
    # 			st.write(location)
    # 			st.write(resume)

    connection = sql.connect("resume_data.db")
    df = pd.read_sql(sql="Select * FROM userinfo", con=connection)
    df.to_csv("Resume_data.csv", index=False)


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
