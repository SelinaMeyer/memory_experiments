import streamlit as st
import time

if st.session_state.get("distractor_timer") not in st.session_state:
        st.session_state.distractor_timer = time.time()

@st.fragment(run_every=1)
def distraction():
    if time.time() - st.session_state.get("distractor_timer") < 10:
        st.radio(label="Would you rather live for the rest of your life in the Arctic or in the Sahara desert?",
            options=["Arctic", "Sahara desert"], index=None, key="distractor_radio")
    elif time.time() - st.session_state.get("distractor_timer") >= 10 and time.time() - st.session_state.get("distractor_timer") < 20:
        st.radio(label="If you could only eat one food for the rest of your life, what would it be?",
            options=["Pizza", "Sushi", "Salad", "Chocolate"], index=None, key="distractor_radio1")
    elif time.time() - st.session_state.get("distractor_timer") >= 20 and time.time() - st.session_state.get("distractor_timer") < 30:
        st.radio(label="If age is only a state of mind, which category best describes your state of mind right now?",
            options=["Cheeky child", "Tormented teenager", "Mad mid-lifer", "Groovy grandparent"], index=None, key="distractor_radio2")
    elif time.time() - st.session_state.get("distractor_timer") >= 30 and time.time() - st.session_state.get("distractor_timer") < 45:
        st.radio(label="If your city were a breed of dog, which breed would it be?",
             options=["Jack Russell - small, tough, opinionated",
              "Tibetan Mastiff - or some other very rare breed",
              "German Shepherd - poised and elegant, but rather hardy",
              "Poodle - beautifully presented, but a bit of a poser",
              "Golden Retriever - warm, cuddly and great with children",
              "Pit Bull Terrier - scary, but kind deep down",
              "Labradoodle - or some other cute hybrid"], index=None, key="distractor_radio3")
    elif time.time() - st.session_state.get("distractor_timer") >= 45 and time.time() - st.session_state.get("distractor_timer") < 60:
        st.radio(label="If you could be any animal, which one would you be?",
            options=["A lion - king of the jungle",
                     "A dolphin - intelligent and playful",
                     "An eagle - free to fly wherever I want",
                     "A tortoise - slow and steady wins the race"], index=None, key="distractor_radio4")
    elif time.time() - st.session_state.get("distractor_timer") >= 60:
        st.switch_page("memory_experiment/pages/recall_page.py")

distraction()