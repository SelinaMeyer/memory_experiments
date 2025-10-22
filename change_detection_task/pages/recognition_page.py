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
st.html("""<p>Unten siehst du jetzt erneut Nachrichtenüberschriften.</p>
        <p> Manche der Überschriften hast du schon zuvor im Experiment gesehen, andere wurden verändert, wieder andere sind komplett neu.</p>
        <p> Gib an, ob du die Überschrift in genau dieser Form im Experiment schon einmal gesehen hast oder nicht.</p>""")

user_repository.set_progress(st.session_state.user_id, 4)
samples = read_json_from_file(TASK_INFO["change_detection_task"]["annotation_filepath"])
sample_response = {}
print(st.session_state)
shuffled_keys, index = user_repository.get_item_progress("recognition_keys", st.session_state.user_id)
print(shuffled_keys, index)
if "shuffled_keys_recognition" not in st.session_state:
    if not shuffled_keys:
        shuffled_keys = [key for key, value in samples.items() if st.session_state.user[3] in value["presentation_grouping"]]
        index = 0
        random.shuffle(shuffled_keys)
    st.session_state.shuffled_keys_recognition = shuffled_keys
    print("Added shuffled keys:", st.session_state.shuffled_keys_recognition)
    st.session_state.index = index

if st.session_state.index < len(st.session_state.shuffled_keys_recognition):
    print("In Fragment!")
    key = st.session_state.shuffled_keys_recognition[st.session_state.index]
    st.image(f"change_detection_task/resources/imgs/{key}.png")
    user_response = st.radio("Hast du genau diese Überschrift schon gesehen?", ["Ja, die Überschrift wurde mir am Anfang gezeigt", "Nein, diese Überschrift wurde mir nicht gezeigt/wurde verändert"], 
                            index=None, 
                            key=st.session_state.index)
    show_next = st.button("Weiter", key="show_next_button")
else:
    st.session_state.recognition_end_time = time.time()
    user_repository.update_demographics(st.session_state.user_id, {"recognition_end_time": st.session_state.recognition_end_time})
    st.switch_page("change_detection_task/pages/thank_you_page.py")

if show_next:
    if user_response is None:
        st.warning("Bitte wähle eine Antwort aus.")
    else:
        sample_response["recognized_by_user"] = True if user_response=="Ja, die Überschrift wurde mir am Anfang gezeigt" else False
        sample_response["sample_id"] = int(key)
        sample_response["seen_in_presentation"] = True if samples[key]["shown"]=="yes" else False
        sample_response["changed"] = True if samples[key]["shown"]=="changed" else False
        sample_response["headline"] = samples[key]["headline"]
        print("key:", key)
        print("response:", user_response)
        user_repository.save_one_annotation(st.session_state.user_id, "recognition", int(key), sample_response)
        if sample_response["recognized_by_user"] == sample_response["seen_in_presentation"]:
            st.html("&#9989; Das war richtig!")
            if "correct_answer_count" not in st.session_state:
                st.session_state.correct_answer_count = 1
            else:
                st.session_state.correct_answer_count += 1
        else:
            st.html("&#10060; Das war leider falsch.")
            if sample_response["seen_in_presentation"]:
                st.html(f"Diese Überschrift wurde Ihnen am Anfang gezeigt.")
            else:
                if sample_response["changed"]:
                    st.html("Diese Überschrift wurde verändert.")
                else:
                    st.html("Diese Überschrift ist neu.")
        st.html("<br>"
                "<p>Hat unsere KI richtig geantwortet?</p>"
                "<p>Die KI hat die Überschrift als "
                f"<b>{'gesehen' if samples[key]['llama_response']=="yes" else 'nicht gesehen'}</b> klassifiziert.</p>")
        if st.button("Zur nächsten Überschrift", key="load_next_recognition_sample_button"):
            st.session_state.index += 1
            progression_data["recognition_keys"] = st.session_state.shuffled_keys_recognition
            progression_data["index"] = st.session_state.index
            progression_data["correct_count"] = st.session_state.correct_answer_count if "correct_answer_count" in st.session_state else 0
            user_repository.update_demographics(st.session_state.user_id, progression_data)
            #key = st.session_state.shuffled_keys[st.session_state.index]
            #placeholder.write(samples[key]["headline"])
            print("Rerunning with new index", st.session_state.index)
            st.rerun()