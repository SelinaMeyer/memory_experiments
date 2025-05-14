import streamlit as st
import pandas as pd
import time
import random

from core.scripts.utils import read_json_from_file, TASK_INFO, skip_to_next_sample, get_amount_of_samples_for_group, handle_next_button
from core.scripts import user_repository

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
progression_data = {}
samples = read_json_from_file(TASK_INFO["memory_experiment"]["annotation_filepath"])

placeholder = st.empty()
user_repository.set_progress(st.session_state.user_id, 1)

if "experiment_start_time" not in st.session_state:
    st.session_state.experiment_start_time = time.time()

if "shuffled_keys_presentation" not in st.session_state:
    st.session_state.progress = user_repository.get_checkpoint("memory")
    already_presented = user_repository.get_item_progress("presented", st.session_state.user_id)
    if not already_presented:
        shuffled_keys = [key for key, value in samples.items() if value["grouping"] == st.session_state.user[3]]
        already_presented = []
    else: 
        shuffled_keys = [key for key, value in samples.items() if value["grouping"] == st.session_state.user[3] 
                         and key not in already_presented]
    random.shuffle(shuffled_keys)
    st.session_state.shuffled_keys_presentation = shuffled_keys
    print("Added shuffled keys:", st.session_state.shuffled_keys_presentation)
    st.session_state.index = 0

while st.session_state.index < len(st.session_state.shuffled_keys_presentation): 
    print("Progress: ", st.session_state.index)
    index = int(st.session_state.progress)
    key = st.session_state.shuffled_keys_presentation[st.session_state.index]
    placeholder.html(f"<h2>{samples[key]["headline"]}")
    time.sleep(10)
    already_presented.append(key)
    progression_data["presented"] = already_presented
    user_repository.update_demographics(st.session_state.user_id, progression_data)
    st.session_state.index += 1
    print("In loop, presented samples: ", st.session_state.index)

st.switch_page("memory_experiment/pages/distractor_page.py")