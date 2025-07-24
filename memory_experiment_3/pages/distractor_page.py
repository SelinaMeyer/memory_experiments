import streamlit as st
import time
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

if st.session_state.get("distractor_timer") not in st.session_state:
        st.session_state.distractor_timer = time.time()
user_repository.set_progress(st.session_state.user_id, 2)
@st.fragment(run_every=1)
def distraction():
    if time.time() - st.session_state.get("distractor_timer") < 15:
        st.image("memory_experiment_3/resources/cat_scale.webp", width=500)
        st.segmented_control(label="scale",
            options=[1,2,3,4,5,6,7,8,9], label_visibility="hidden", key="distractor_radio")
    elif time.time() - st.session_state.get("distractor_timer") >= 15 and time.time() - st.session_state.get("distractor_timer") < 30:
        st.write("Where would you rather live for the rest of your life?")
        st.image("memory_experiment_3/resources/landscapes.png", width=500)
        st.segmented_control(label="Where would you rather live for the rest of your life?",
            options=[1,2,3,4], label_visibility="hidden", key="distractor_radio2")
    elif time.time() - st.session_state.get("distractor_timer") >= 30 and time.time() - st.session_state.get("distractor_timer") < 45:
        st.write("What do you see in the image?")
        st.image("memory_experiment_3/resources/hammerhead_shark.webp", width=500)
        st.radio(label="What do you see in the image?",
             options=["A \"hammerhead shark\"",
              "A \"humpback whale\"",
              "A \"bottlenose dolphin\""], label_visibility="hidden", index=None, key="distractor_radio3")
    elif time.time() - st.session_state.get("distractor_timer") >= 45 and time.time() - st.session_state.get("distractor_timer") < 60:
        st.write("What is your ideal night out?")
        st.image("memory_experiment_3/resources/night_out.png", width=500)
        st.segmented_control(label="What's your ideal night out?",
            options=[1,2,3,4],label_visibility="hidden", key="distractor_radio4")
    elif time.time() - st.session_state.get("distractor_timer") >= 60:
        st.switch_page("memory_experiment_3/pages/recall_page.py")

distraction()