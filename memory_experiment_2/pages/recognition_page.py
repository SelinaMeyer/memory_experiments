import streamlit as st
import time
import pandas as pd
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
st.html("""<p>Below, you will again see some news headlines on the screen, one after the other. 
         <br>You might have seen some of them before during this experiment, others are new.
         <p>For each headline, please indicate whether it is a headline you have seen in the initial memorization task or a new headline you have not seen in the memorization task.""")

user_repository.set_progress(st.session_state.user_id, 4)
samples = read_json_from_file(TASK_INFO["memory_experiment_2"]["annotation_filepath"])
sample_response = {}
print(st.session_state)
shuffled_keys, index = user_repository.get_item_progress("recognition_keys", st.session_state.user_id)
print(shuffled_keys, index)
if "shuffled_keys_recognition" not in st.session_state:
    if not shuffled_keys:
        shuffled_keys = [key for key, value in samples.items() if st.session_state.user[3] in value["presentation_grouping"] and value["grouping"] != 5]
        index = 0
        random.shuffle(shuffled_keys)
    st.session_state.shuffled_keys_recognition = shuffled_keys
    print("Added shuffled keys:", st.session_state.shuffled_keys_recognition)
    st.session_state.index = index

if st.session_state.index < len(st.session_state.shuffled_keys_recognition):
    print("In Fragment!")
    key = st.session_state.shuffled_keys_recognition[st.session_state.index]
    st.image(f"memory_experiment_2/resources/imgs/{key}.png")
    user_response = st.radio("Have you seen the headline above before?", ["Yes, this was shown to me in the initial task", "No, this headline is new"], 
                            index=None, 
                            key=st.session_state.index)
    show_next = st.button("Show next", key="show_next_button")
else:
    st.session_state.recognition_end_time = time.time()
    user_repository.update_demographics(st.session_state.user_id, {"recognition_end_time": st.session_state.recognition_end_time})
    st.switch_page("memory_experiment_2/pages/truthjudgement_page.py")

if show_next:
    if user_response is None:
        st.warning("Please select an answer before proceeding.")
    else:
        sample_response["recognized_by_user"] = True if user_response=="Yes, this was shown to me in the initial task" else False
        sample_response["sample_id"] = int(key)
        sample_response["seen_in_presentation"] = True if st.session_state.user[3] == samples[key]["grouping"] else False
        sample_response["headline"] = samples[key]["headline"]
        print("key:", key)
        print("response:", user_response)
        user_repository.save_one_annotation(st.session_state.user_id, "recognition", int(key), sample_response)
        st.session_state.index += 1
        progression_data["recognition_keys"] = st.session_state.shuffled_keys_recognition
        progression_data["index"] = st.session_state.index
        user_repository.update_demographics(st.session_state.user_id, progression_data)
        #key = st.session_state.shuffled_keys[st.session_state.index]
        #placeholder.write(samples[key]["headline"])
        print("Rerunning with new index", st.session_state.index)
        st.rerun()