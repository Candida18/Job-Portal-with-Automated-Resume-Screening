from operator import index
from pydoc import doc
from itsdangerous import encoding
from pandas._config.config import options
import Cleaner
import textract as tx
import pandas as pd
import os
import tf_idf
import streamlit as st

resume_dir = "Data/Resume/"
job_desc_dir = "Data/JobDesc/"
resume_name = os.listdir(resume_dir)
resume_names=[]
for i in resume_name:
    i.strip(".docx")
    resume_names.append(i)
job_description_names = os.listdir(job_desc_dir)

document = []

'''
def read_resumes(list_of_resumes, resume_directory):
    placeholder = []
    for res in list_of_resumes:
        temp = []
        temp.append(res)
        if(res.endswith(".doc")):
            text = tx.process(resume_directory + res,encoding="ascii",extension='doc')
        elif(res.endswith(".docx")):
            text = tx.process(resume_directory + res,encoding="ascii",extension='docx')
        elif(res.endswith(".pdf")):
            text = tx.process(resume_directory + res,encoding="ascii",extension='pdf')
        text = str(text, "utf-8")
        temp.append(text)
        placeholder.append(temp)
    return placeholder
'''

def read_resumes(list_of_resumes, resume_directory):
    placeholder = []
    for res in list_of_resumes:
        temp = []
        temp.append(res)
        text = tx.process(resume_directory + res, encoding="ascii")
        text = str(text, "utf-8")
        temp.append(text)
        placeholder.append(temp)
    return placeholder

document = read_resumes(resume_names, resume_dir)


def get_cleaned_words(document):
    for i in range(len(document)):
        raw = Cleaner.Cleaner(document[i][1])
        document[i].append(" ".join(raw[0]))
        document[i].append(" ".join(raw[1]))
        document[i].append(" ".join(raw[2]))
        sentence = tf_idf.do_tfidf(document[i][3].split(" "))
        document[i].append(sentence)
    return document


Doc = get_cleaned_words(document)

Database = pd.DataFrame(
    document,
    columns=[
        "FileName",
        "Context",
        "Cleaned",
        "Selective",
        "Selective_Reduced",
        "TF_Based",
    ],
)

Database.to_csv("CSV/Resume_Data.csv", index=False)

# Database.to_json("Resume_Data.json", index=False)


def read_jobdescriptions(job_description_names, job_desc_dir):
    placeholder = []
    for tes in job_description_names:
        temp = []
        temp.append(tes)
        text = tx.process(job_desc_dir + tes, encoding="ascii")
        text = str(text, "utf-8")
        temp.append(text)
        placeholder.append(temp)
    return placeholder


job_document = read_jobdescriptions(job_description_names, job_desc_dir)

Jd = get_cleaned_words(job_document)

jd_db = pd.DataFrame(
    Jd,
    columns=[ 
        "Name",
        "Context",
        "Cleaned",
        "Selective",
        "Selective_Reduced",
        "TF_Based",
    ],
)

jd_db.to_csv("CSV/Job_Data.csv", index=False)
