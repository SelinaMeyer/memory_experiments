import streamlit as st
from core.scripts import user_repository
import time

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

start, i = user_repository.get_item_progress("recall_start_time", st.session_state.user_id)
if not start:
    st.session_state.recall_start_time = time.time()
    user_repository.update_demographics(st.session_state.user_id, {"recall_start_time": st.session_state.recall_start_time})
else:
    st.session_state.recall_start_time = start
user_repository.set_progress(st.session_state.user_id, 3)

st.html("""<p>Now please try to remember the headlines you learned at the beginning.
                    <br>The order of the headlines does not matter. Just write them down as you remember them, using a new line for each new headline. 
                    <p>If you can, please try to remember the headline in its original form as accurately as possible - but if you can't remember the exact headline, you can also paraphrase in your own words what the headline was about. 
                    <p>You should take approximately five minutes to write down as many headlines as possible from the memorization task.""")
recall = st.text_area("Headlines you remember:", key="recall", height=300)

recall_dict = {}

if st.button("Submit"):
    if recall is None or recall == "":
        st.warning("Please write down at least one headline before submitting."
        "If you don't remember the exact wording of any headlines, try to write down as much as you remember")
    elif time.time() - st.session_state.recall_start_time < 300: # change to 300
        if "recall_submit_attempts" not in st.session_state:
            st.session_state.recall_submit_attempts = 1
            st.warning("Please take your time to write down the headlines. You have 5 minutes for this task.")
        elif st.session_state.recall_submit_attempts < 2:
            st.session_state.recall_submit_attempts += 1
            st.warning("Please take your time to write down the headlines. You have 5 minutes for this task.")
        else: 
            textsplit = recall.splitlines()
            recall_dict["recall"] = []
            for x in textsplit:
                recall_dict["recall"].append(x)
            user_repository.save_one_annotation(st.session_state.user_id, "recall", 1, recall_dict)
            st.session_state.recall_end_time = time.time()
            user_repository.update_demographics(st.session_state.user_id, {"recall_end_time": st.session_state.recall_end_time})
            st.switch_page("memory_experiment/pages/recognition_page.py")
    else:
        textsplit = recall.splitlines()
        recall_dict["recall"] = []
        for x in textsplit:
            recall_dict["recall"].append(x)
        user_repository.save_one_annotation(st.session_state.user_id, "recall", 1, recall_dict)
        st.session_state.recall_end_time = time.time()
        user_repository.update_demographics(st.session_state.user_id, {"recall_end_time": st.session_state.recall_end_time})
        st.switch_page("memory_experiment/pages/recognition_page.py")