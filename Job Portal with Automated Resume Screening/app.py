
import scipy
import gensim
import gensim.corpora as corpora
from operator import index
from wordcloud import WordCloud
from pandas._config.config import options
import pandas as pd
import streamlit as st
import plotly.express as px
import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import Similar
from PIL import Image
import time
import webbrowser
import os
import numpy as np
from sklearn import datasets, linear_model 



#######################################################################################################


os.system('python fileReader.py')


st.markdown("<h1 style='text-align: center;font-size:350%'>RESUME SCREENING</h1><br>", unsafe_allow_html=True)


image = Image.open("Images/firstimage.png")
st.image(image,use_column_width=True)


st.title("Resume Screening")
# Reading the CSV files prepared by the fileReader.py
Resumes = pd.read_csv("CSV/Resume_Data.csv")
Jobs = pd.read_csv("CSV/Job_Data.csv")


job_names = []
for i in Jobs["Name"]:
    job_new = i.strip(".docx")
    job_names.append(job_new)

#######################################################################################################
                                        # PERSONALITY PREDICTION
#######################################################################################################


class train_model:
    
    def train(self):
        data =pd.read_csv('training_dataset.csv')
        array = data.values

        for i in range(len(array)):
            if array[i][0]=="Male":
                array[i][0]='1'
            else:
                array[i][0]='0'

        df=pd.DataFrame(array)


        maindf =df[[0,1,2,3,4,5,6]]
        mainarray=maindf.values

        temp=df[7]
        train_y =temp.values
        
        self.mul_lr = linear_model.LogisticRegression(multi_class='multinomial', solver='newton-cg',max_iter =1000)
        self.mul_lr.fit(mainarray, train_y)
        
    def test(self, test_data):
        try:
            test_predict=list()
            for i in test_data:
                test_predict.append(int(i))
            y_pred = self.mul_lr.predict([test_predict])
            return y_pred
        except:
            print("All Factors For Finding Personality Not Entered!")
Personality = pd.read_csv("CSV/Form_data.csv")

model = train_model()
model.train()


def prediction_result():
    "after applying a job"

    personality_list =[]
    for i in range(0,Resumes.shape[0]):
        personality_values = (Personality["gender"][i],Personality["age"][i],Personality["openness"][i],Personality["neuroticism"][i],Personality["conscientiousness"][i],Personality["agreeableness"][i],Personality["extraversion"][i])
        
        personality = model.test(personality_values)
        personality_list.append(personality)
        #personality_list.insert(0,personality)
        #st.header(personality)

    # print("\n############# Predicted Personality #############\n")

    return personality_list

Personality["Personality"] = prediction_result()



############################### JOB DESCRIPTION CODE ######################################
# Checking for Multiple Job Descriptions
# If more than one Job Descriptions are available, it asks user to select one as well.
if len(Jobs["Name"]) <= 1:
    st.write(
        "There is only 1 Job Description present. It will be used to create scores."
    )
else:
    st.write(
        "There are ",
        len(Jobs["Name"]),
        "Job Descriptions available. Please select one.",
    )


# Asking to Print the Job Description Names
if len(Jobs["Name"]) > 1:
    option_yn = st.selectbox("Show the Job Openings?", options=["YES", "NO"])
    if option_yn == "YES":
        index = [a for a in range(len(Jobs["Name"]))]
        fig = go.Figure(
            data=[
                go.Table(
                    header=dict(
                        values=["Job No.", "Job Desc. Name"],
                        line_color="white",
                        fill_color="#234f92",
                        font_color="white",
                    ),
                    cells=dict(
                        values=[index, job_names],
                        line_color="#0d2840",
                        fill_color="white",
                        font_color="#0d2840",
                        height=25,
                    ),
                )
            ]
        )

        fig.update_layout(width=700, height=600)
        st.write(fig)


# Asking to chose the Job Description
st.markdown("### Which Job to select ? :")
index = st.slider("", 0, len(Jobs["Name"]) - 1, 1)

option_yn = st.selectbox("Show the Job Description ?", options=["YES", "NO"])
if option_yn == "YES":
    st.markdown("---")
    st.markdown("### Job Description :")
    fig = go.Figure(
        data=[
            go.Table(
                header=dict(
                    values=["Job Description"],
                    line_color="white",
                    fill_color="#234f92",
                    align="center",
                    font=dict(color="white", size=16),
                ),
                cells=dict(
                    values=[Jobs["Context"][index]],
                    line_color="#0d2840",
                    fill_color="white",
                    font_color="#0d2840",
                    align="left",
                ),
            )
        ]
    )

    fig.update_layout(width=800, height=500)
    st.write(fig)
    st.markdown("---")


#################################### SCORE CALCULATION ################################
@st.cache()
def calculate_scores(resumes, job_description):
    scores = []
    for x in range(resumes.shape[0]):
        score = Similar.match(
            resumes["TF_Based"][x], job_description["TF_Based"][index]
        )
        scores.append(score)
    return scores


Resumes["Scores"] = calculate_scores(Resumes, Jobs)

#Resumes['Personality'] = prediction_result()
Resumes = pd.merge(Resumes,Personality)

Resumes.rename(columns = {'FileName':'Name'}, inplace = True)
job_match = Jobs["Name"][index].strip('.docx')

if job_match=='Web Developer':
    Resumes = (Resumes[Resumes['jobs'].str.contains('Web Developer')])
elif (job_match=='Data Scientist'):
    Resumes = (Resumes[Resumes['jobs'].str.contains('Data Scientist')])
elif (job_match=='HTML Developer'):
    Resumes = (Resumes[Resumes['jobs'].str.contains('HTML Developer ')])
elif (job_match=='IT Project Manager'):
    Resumes = (Resumes[Resumes['jobs'].str.contains('IT Project Manager')])
elif (job_match=='Senior Product Manager'):
    Resumes = (Resumes[Resumes['jobs'].str.contains('Senior Product Manager')])
elif (job_match=='Senior Software Developer'):
    Resumes = (Resumes[Resumes['jobs'].str.contains('Senior Software Developer ')])
elif (job_match=='Lead Technical Program Manager'):
    Resumes = (Resumes[Resumes['jobs'].str.contains('Lead Technical Program Manager')])
elif (job_match=='Global Industry Content Manager'):
    Resumes = (Resumes[Resumes['jobs'].str.contains('Global Industry Content Manager')])
elif (job_match=='Revenue Reporting Data Analyst'):
    Resumes = (Resumes[Resumes['jobs'].str.contains('Revenue Reporting Data Analyst')])
else:
    Resumes = Resumes[Resumes['jobs'] == job_match]

#Resumes = Resumes.loc[Resumes["jobs"] == (Jobs["Name"][index].strip(".docx"))]

Ranked_resumes = Resumes.sort_values(by=["Scores"], ascending=False).reset_index(
    drop=True
)
#

#

Ranked_resumes["Rank"] = pd.DataFrame(
    [i for i in range(1, len(Ranked_resumes["Scores"]) + 1)] )



###################################### SCORE TABLE PLOT ####################################
st.subheader("Top Ranked Resumes")

fig1 = go.Figure(
    data=[
        go.Table(
            header=dict(
                values=["Rank", "Name", "Scores", "Personality"],
                fill_color="#234f92",
                align="center",
                font=dict(color="white", size=16),
            ),
            cells=dict(
                values=[
                    Ranked_resumes.Rank,
                    Ranked_resumes.Name,
                    Ranked_resumes.Scores,
                    Ranked_resumes.Personality,
                    
                ] ,
                fill_color="#d6e0f0",
                align="left",
                font_color="#0d2840",
                height=25,
            ),
        )
    ]
)

fig1.update_layout(width=700, height=1000)
#fig1.update_layout(title="Top Ranked Resumes", width=700, height=1100)
st.write(fig1)

st.markdown("---")

fig2 = px.bar(
    Ranked_resumes,
    x=Ranked_resumes["Name"],
    y=Ranked_resumes["Scores"],
    color="Scores",
    color_continuous_scale="haline",
    title="Score and Rank Distribution",
)
# fig.update_layout(width=700, height=700)
st.write(fig2)


st.markdown("---")

############################################ TF-IDF Code ###################################


@st.cache()
def get_list_of_words(document):
    Document = []

    for a in document:
        raw = a.split(" ")
        Document.append(raw)

    return Document


document = get_list_of_words(Resumes["Cleaned"])

id2word = corpora.Dictionary(document)
corpus = [id2word.doc2bow(text) for text in document]


lda_model = gensim.models.ldamodel.LdaModel(
    corpus=corpus,
    id2word=id2word,
    num_topics=6,
    random_state=100,
    update_every=3,
    chunksize=100,
    passes=50,
    alpha="auto",
    per_word_topics=True,
)

################################### LDA CODE ##############################################


@st.cache  # Trying to improve performance by reducing the rerun computations
def format_topics_sentences(ldamodel, corpus):
    sent_topics_df = []
    for i, row_list in enumerate(ldamodel[corpus]):
        row = row_list[0] if ldamodel.per_word_topics else row_list
        row = sorted(row, key=lambda x: (x[1]), reverse=True)
        for j, (topic_num, prop_topic) in enumerate(row):
            if j == 0:
                wp = ldamodel.show_topic(topic_num)
                topic_keywords = ", ".join([word for word, prop in wp])
                sent_topics_df.append(
                    [i, int(topic_num), round(prop_topic, 4) * 100, topic_keywords]
                )
            else:
                break

    return sent_topics_df


################################# Topic Word Cloud Code #####################################

st.markdown("## Topics and Topic Related Keywords ")
st.markdown(
    """This Wordcloud representation shows the Topic Number and the Top Keywords that constitute a Topic.
    This further is used to cluster the resumes.      """
)

cols = [color for name, color in mcolors.TABLEAU_COLORS.items()]

cloud = WordCloud(
    background_color="white",
    width=2500,
    height=1800,
    max_words=10,
    colormap="tab10",
    collocations=False,
    color_func=lambda *args, **kwargs: cols[i],
    prefer_horizontal=1.0,
)

topics = lda_model.show_topics(formatted=False)

fig, axes = plt.subplots(2, 3, figsize=(10, 10), sharex=True, sharey=True)

for i, ax in enumerate(axes.flatten()):
    fig.add_subplot(ax)
    topic_words = dict(topics[i][1])
    cloud.generate_from_frequencies(topic_words, max_font_size=300)
    plt.gca().imshow(cloud)
    plt.gca().set_title("Topic " + str(i), fontdict=dict(size=16))
    plt.gca().axis("off")


plt.subplots_adjust(wspace=0, hspace=0)
plt.axis("off")
plt.margins(x=0, y=0)
plt.tight_layout()
st.pyplot(plt)

st.markdown("---")

####################### SETTING UP THE DATAFRAME FOR SUNBURST-GRAPH ############################

df_topic_sents_keywords = format_topics_sentences(ldamodel=lda_model, corpus=corpus)
df_some = pd.DataFrame(
    df_topic_sents_keywords,
    columns=["Document No", "Dominant Topic", "Topic % Contribution", "Keywords"],
)
df_some["Names"] = Ranked_resumes["Name"]

df = df_some

st.markdown("## Topic Modelling of Resumes ")
st.markdown(
    "Using LDA to divide the topics into a number of usefull topics and creating a Cluster of matching topic resumes.  "
)
fig3 = px.sunburst(
    df,
    path=["Dominant Topic", "Names"],
    values="Topic % Contribution",
    color="Dominant Topic",
    color_continuous_scale="viridis",
    width=800,
    height=800,
    title="Topic Distribution Graph",
)
st.write(fig3)


############################## RESUME PRINTING #############################
st.markdown("---")
st.markdown("## **Resume** ")
option_2 = st.selectbox("Show the Best Matching Resumes?", options=["YES", "NO"])
if option_2 == "YES":
    indx = st.slider("Which resume to display ?:", 1, Ranked_resumes.shape[0], 1)

    st.write("Displaying Resume with Rank: ", indx)

    value = Ranked_resumes.iloc[indx - 1, 2]
    st.markdown("#### The Word Cloud For the Resume")
    wordcloud = WordCloud(
        width=800,
        height=800,
        background_color="white",
        colormap="viridis",
        collocations=False,
        min_font_size=10,
    ).generate(value)

    ############################## Resume Name with Rank ##############################
    st.write(Ranked_resumes._get_value(indx - 1, "Name"))

    if st.button(
        "View {}'s Resume".format(Ranked_resumes._get_value(indx - 1, "Name"))
    ):
        webbrowser.open_new_tab(
            "C:/Users/Gini/Mini Project/Final_ResumePPV2/Data/Resume{}".format(
                Ranked_resumes._get_value(indx - 1, "Name")
            )
        )
    ###################################################################################

    plt.figure(figsize=(7, 7), facecolor=None)
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.tight_layout(pad=0)
    st.pyplot(plt)

    st.write("With a Match Score of :", Ranked_resumes.iloc[indx - 1, 6])
    fig = go.Figure(
        data=[
            go.Table(
                header=dict(
                    values=["Resume"],
                    fill_color="#234f92",
                    align="center",
                    font=dict(color="white", size=16),
                ),
                cells=dict(
                    values=[str(value)],
                    line_color="#0d2840",
                    fill_color="white",
                    font_color="#0d2840",
                    align="left",
                ),
            )
        ]
    )

    fig.update_layout(width=800, height=1200)
    st.write(fig)
    # st.text(df_sorted.iloc[indx-1, 1])
    st.markdown("---")





