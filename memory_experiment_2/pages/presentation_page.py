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
samples = read_json_from_file(TASK_INFO["memory_experiment_2"]["annotation_filepath"])
shuffled_keys, index = user_repository.get_item_progress("presentation_keys", st.session_state.user_id)
placeholder = st.empty()
user_repository.set_progress(st.session_state.user_id, 1)

start, i = user_repository.get_item_progress("experiment_start_time", st.session_state.user_id)

if not start:
    st.session_state.experiment_start_time = time.time()
    user_repository.update_demographics(st.session_state.user_id, {"experiment_start_time": st.session_state.experiment_start_time})

if "shuffled_keys_presentation" not in st.session_state:
    st.session_state.progress = user_repository.get_checkpoint("memory")
    if not shuffled_keys:
        print("No shuffled keys found, creating new ones")
        shuffled_keys = [key for key, value in samples.items() if value["grouping"] == st.session_state.user[3]]
        random.shuffle(shuffled_keys)
        index = 0
    st.session_state.shuffled_keys_presentation = shuffled_keys
    print("Added shuffled keys:", st.session_state.shuffled_keys_presentation)
    st.session_state.index = index
    print("current index:", st.session_state.index)

with st.empty():
    while st.session_state.index < len(st.session_state.shuffled_keys_presentation): 
        print("Progress: ", st.session_state.index)
        index = int(st.session_state.progress)
        key = st.session_state.shuffled_keys_presentation[st.session_state.index]
        st.image(f"memory_experiment_2/resources/imgs/{key}.png", width=1000)
        time.sleep(10)
        st.session_state.index += 1
        progression_data["presentation_keys"] = st.session_state.shuffled_keys_presentation
        progression_data["index"] = st.session_state.index
        print("shuffled_keys to save: ", st.session_state.shuffled_keys_presentation)
        user_repository.update_demographics(st.session_state.user_id, progression_data)
        print("In loop, presented samples: ", st.session_state.index)

st.switch_page("memory_experiment_2/pages/distractor_page.py")