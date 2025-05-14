import streamlit as st
from core.scripts import user_repository
import time
from datetime import datetime

hide_streamlit_style = """
                <style>
                div[data-testid="stToolbar"] {
                visibility: hidden;
                height: 0%;
                position: fixed;
                }
                div[data-testid="stDecoration"] {
                visibility: hidden;
                height: 0%;
                position: fixed;
                }
                div[data-testid="stStatusWidget"] {
                visibility: hidden;
                height: 0%;
                position: fixed;
                }
                #MainMenu {
                visibility: hidden;
                height: 0%;
                }
                header {
                visibility: hidden;
                height: 0%;
                }
                footer {
                visibility: hidden;
                height: 0%;
                }
                </style>
                """
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 

political_labels = {
    0: "1 - left",
    1: "2",
    2: "3 - center",
    3: "4",
    4: "5 - right",
    5: "prefer not to say"
}
demographics = {}
user_repository.set_progress(st.session_state.user_id, 6)
st.write("Below, we ask you to provide some demographic information about yourself. If you do not feel comfortable answering a question, you can leave the field empty.")
with st.form("Please provide the following information about yourself:"):
    age = st.number_input("How old are you?", min_value=0, max_value=100, key="age", placeholder=0)
    gender = st.radio("How do you describe your current gender identity?", ["Man", "Woman",
                                                                             "Non-binary", "Prefer to self-describe"],index=None, key="gender")
    
    self_gender = st.text_input("If you selected \"Prefer to self-describe\" above, please specify your gender identity")
    education = st.radio("What's your highest education level?", ["Less than high school", "high school degree/GED", "some college but no degree", 
                                                                  "Bachelor's degree (4 year)", "Associate degree (2-year)",
                                                                  "Master's degree", "Doctoral degree", "Professional degree (JD, MD)"],index=None, key="education")
    occupation = st.radio("What is your current occupation?", ["Employed", "Unemployed", "Self-employed", "Retired", "Homemaker", "Student", "Other"],index=None)
    political_party = st.segmented_control("What is your political orientation?", options=[
        political_labels[0],
        political_labels[1],
        political_labels[2],
        political_labels[3],
        political_labels[4],
    ], key="political_party")

    st.write("Please indicate how often you get news from the following sources:")
    print = st.segmented_control("Print (e.g. newspapers)", ["Not at all", "Once a week", "More than once a week", "Once a day", "More than once a day"], key="print",)
    radio = st.segmented_control("Radio", ["Not at all", "Once a week", "More than once a week", "Once a day", "More than once a day"],key="radio")
    tv = st.segmented_control("Television", ["Not at all", "Once a week", "More than once a week", "Once a day", "More than once a day"], key="tv")
    digital = st.segmented_control("Digital devices (e.g. a smartphone, computer, or tablet)", ["Not at all", "Once a week", "More than once a week", "Once a day", "More than once a day"], key="digital")

    st.write("Focusing on the digital devices, please indicate how often you get news from the following sources:")
    news_website = st.segmented_control("News websites or apps (e.g. nytimes.com or the AppleNews app)", ["Not at all", "Once a week", "More than once a week", "Once a day", "More than once a day"], key="news_website")
    social_media = st.segmented_control("Social media (e.g. Facebook, Instagram, TikTok, Youtube)", ["Not at all", "Once a week", "More than once a week", "Once a day", "More than once a day"], key="social_media")
    internet = st.segmented_control("Internet search (e.g. Google)", ["Not at all", "Once a week", "More than once a week", "Once a day", "More than once a day"], key="internet")
    podcast = st.segmented_control("Podcasts", ["Not at all", "Once a week", "More than once a week", "Once a day", "More than once a day"], key="podcast")
    
    difficulty = st.segmented_control("How difficult was this study to complete?", ["1 (very difficult)", "2", "3", "4", "5 (very easy)"],key="difficulty")
    study_description = st.text_area("Please describe in one or two sentences what this study was about, in your own opinion:", key="study_description", height=100)
    further_comments = st.text_area("If you have any further comments on the study, please feel free to provide them here:", key="further_comments", height=100)
    submitted = st.form_submit_button("Submit")
if submitted:
    demographics["age"] = age
    demographics["gender"] = self_gender if gender == "Prefer to self-describe" else gender
    demographics["education"] = education
    demographics["occupation"] = occupation
    demographics["political_party"] = political_party
    demographics["news_consumption_print"] = print
    demographics["news_consumption_radio"] = radio
    demographics["news_consumption_tv"] = tv
    demographics["news_consumption_digital"] = digital
    demographics["news_consumption_news_website"] = news_website
    demographics["news_consumption_social_media"] = social_media
    demographics["news_consumption_internet"] = internet
    demographics["news_consumption_podcast"] = podcast
    demographics["study_difficulty"] = difficulty
    demographics["study_description"] = study_description
    demographics["further_comments"] = further_comments
    demographics["experiment_start_time"] = st.session_state.experiment_start_time
    demographics["recall_start_time"] = st.session_state.recall_start_time
    demographics["recall_end_time"] = st.session_state.recall_end_time
    demographics["recognition_end_time"] = st.session_state.recognition_end_time
    demographics["truth_judgement_end_time"] = st.session_state.truth_judgement_end_time
    demographics["experiment_end_time"] = time.time()
    user_repository.update_demographics(st.session_state.user_id, demographics)
    st.switch_page("memory_experiment/pages/thank_you_page.py")